import Vue from 'vue';
import Vuex from 'vuex';
import { get } from '../api';
import { Activity, Affiliation, Agent, Citation, Meta } from '../models/main';
import VuexORM from '@vuex-orm/core';

Vue.use(Vuex);

const database = new VuexORM.Database();
database.register(Agent);
database.register(Affiliation);
database.register(Activity);
database.register(Meta);
database.register(Citation);

const store = new Vuex.Store({
  plugins: [VuexORM.install(database)],
  state: {
    settings: {
      packageId: null,
      canEdit: false,
      doiPlugin: false,
    },
    packageDetail: {},
    controlledLists: {
      agentTypes: {},
      activityTypes: {},
      activityLevels: [],
      agentIdSchemes: {},
    },
    results: {
      offset: 0,
      total: 0,
      citedTotal: 0,
      pageSize: 10,
      allAgents: [],
      loading: false,
    },
  },
  getters: {
    agentTypeIcon: (state) => (agentType) => {
      let typeDetails = state.controlledLists.agentTypes[agentType];
      return typeDetails ? typeDetails.fa_icon : 'fas fa-asterisk';
    },
    agentIdIcon: (state) => (idScheme) => {
      let schemeDetails = state.controlledLists.agentIdSchemes[idScheme];
      return schemeDetails ? schemeDetails.fa_icon : 'fas fa-link';
    },
    serialisedContent: () => {
      let serialise = (model) =>
        model
          .query()
          .with('meta')
          .all()
          .map((x) => x.$toJson());
      return JSON.stringify({
        agents: serialise(Agent),
        activities: serialise(Activity),
        affiliations: serialise(Affiliation),
        citations: serialise(Citation),
      });
    },
    currentPageCitedSelector: () => {
      return () =>
        Agent.query()
          .with('meta')
          .where('isActive', true)
          .where('citeable', true)
          .whereHas('meta', (q) => {
            q.where('is_temporary', false);
          });
    },
    currentPageUncitedSelector: () => {
      return () =>
        Agent.query()
          .with('meta')
          .where('isActive', true)
          .where('citeable', false)
          .whereHas('meta', (q) => {
            q.where('is_temporary', false);
          });
    },
    citedTotal: (state, getters) => {
      return (
        getters
          .currentPageCitedSelector()
          .whereHas('meta', (q) => {
            q.where('is_new', true);
          })
          .count() + state.results.citedTotal
      );
    },
  },
  mutations: {
    updateSettings(state, payload) {
      Vue.set(state.settings, 'packageId', payload.packageId);
      Vue.set(state.settings, 'canEdit', payload.canEdit);
      Vue.set(state.settings, 'doiPlugin', payload.doiPlugin);
    },
  },
  actions: {
    initialise(context) {
      return context
        .dispatch('initLists')
        .then(() => context.dispatch('getContributions'));
    },
    getContributions(context) {
      if (
        !context.state.settings.packageId ||
        context.state.settings.packageId === ''
      ) {
        return;
      }
      Vue.set(context.state.results, 'loading', true);

      let editedItems = Meta.query()
        .withAllRecursive()
        .where('is_dirty', true)
        .orWhere('is_new', true)
        .orWhere('to_delete', true)
        .get();

      return get('package_contributions_show', {
        id: context.state.settings.packageId,
        limit: context.state.results.pageSize,
        offset: context.state.results.offset,
      })
        .then((res) => {
          if (res === undefined) {
            return;
          }
          Vue.set(context.state.results, 'offset', res.offset);
          Vue.set(context.state.results, 'pageSize', res.page_size);
          Vue.set(context.state.results, 'total', res.total);
          Vue.set(context.state.results, 'citedTotal', res.cited_total);
          Vue.set(context.state.results, 'allAgents', res.all_agents);

          let agentIds = res.contributions.map((r) => r.agent.id);
          // there seems to be some kind of bug in .create() where it will sometimes
          // create everything and then delete it - manually clearing first then
          // using .insert() instead avoids that
          Meta.query()
            .with('item')
            .where('is_temporary', false)
            .all()
            .forEach((m) => {
              m.item.$delete();
              m.$delete();
            });

          Agent.insert({
            data: res.contributions.map((r) => {
              let agent = r.agent;
              agent.affiliations = r.affiliations.map((a) => {
                a.db_id = a.id;
                a.id = null;
                if (!agentIds.includes(a.other_agent.id)) {
                  a.other_agent.meta = { is_hidden: true };
                }
                return a;
              });
              agent._activities = r.activities
                .filter((a) => a.activity !== '[citation]')
                .map((a) => {
                  if (!a.package_id) {
                    a.package_id = context.state.settings.packageId;
                  }
                  return a;
                });
              agent._citation = r.activities
                .filter((a) => a.activity === '[citation]')
                .map((a) => {
                  if (!a.package_id) {
                    a.package_id = context.state.settings.packageId;
                  }
                  return a;
                })
                .slice(-1)[0];
              return agent;
            }),
          })
            .then(() => {
              // add the previously edited items but hide them
              let updates = [];
              editedItems.forEach((itemMeta) => {
                let factory = this.$db().model(itemMeta.item_type);
                let item = itemMeta.item;
                delete itemMeta.item;
                delete itemMeta.id;
                delete itemMeta.$id;
                if (factory.query().where('id', itemMeta.item_id).exists()) {
                  updates.push(
                    factory.update({ data: item }).then(() => {
                      itemMeta.is_hidden = false;
                      itemMeta.is_saved_edit = false;
                      return factory.updateMeta(item.id, itemMeta);
                    }),
                  );
                } else {
                  itemMeta.is_hidden = true;
                  itemMeta.is_saved_edit = true;
                  // if the meta isn't deleted first, it creates two copies (idk why)
                  delete item.meta;
                  updates.push(
                    factory.insert({ data: item }).then(() => {
                      factory.updateMeta(item.id, itemMeta);
                    }),
                  );
                }
              });
              return Promise.all(updates);
            })
            .then(() => {
              // check if the new items should be shown (has to be done after loading everything)
              let res = context.state.results; // this is annoying to type out every time
              let isLastPage = res.offset + res.pageSize >= res.total;
              let isLastCitedPage =
                res.offset + res.pageSize >= res.citedTotal >= res.offset;

              return Agent.query()
                .withAllRecursive()
                .whereHas('meta', (q) => {
                  q.where('is_new', true);
                })
                .all()
                .forEach((a) => {
                  let uncitedOnLastPage = !a.citation.order && isLastPage;
                  let isInRange =
                    a.citation.order &&
                    res.offset <= a.citation.order &&
                    a.citation.order <= res.offset + res.pageSize;
                  let higherThanTotalAtEnd =
                    a.citation.order &&
                    a.citation.order < context.state.results.citedTotal &&
                    isLastCitedPage;
                  let show =
                    uncitedOnLastPage || isInRange || higherThanTotalAtEnd;
                  Agent.updateMeta(a.id, {
                    is_hidden: !show,
                    is_saved_edit: !show,
                  });
                  a.activities.forEach((ac) => {
                    Activity.updateMeta(ac.id, {
                      is_hidden: !show,
                      is_saved_edit: !show,
                    });
                  });
                });
            });
        })
        .finally(() => {
          Vue.set(context.state.results, 'loading', false);
        });
    },
    changeOffset(context, newOffset) {
      console.log(newOffset);
      if (newOffset < context.state.results.total && newOffset >= 0) {
        Vue.set(context.state.results, 'offset', newOffset);
        context.dispatch('getContributions');
      }
    },
    getPackage(context) {
      if (
        !context.state.settings.packageId ||
        context.state.settings.packageId === ''
      ) {
        return;
      }
      return get('package_show', { id: context.state.settings.packageId }).then(
        (res) => {
          context.state.packageDetail = res;
        },
      );
    },
    initLists(context) {
      return get('attribution_controlled_lists').then((res) => {
        Vue.set(context.state.controlledLists, 'agentTypes', res.agent_types);
        Vue.set(
          context.state.controlledLists,
          'activityTypes',
          res.contribution_activity_types,
        );
        Vue.set(
          context.state.controlledLists,
          'activityLevels',
          res.contribution_activity_levels,
        );
        Vue.set(
          context.state.controlledLists,
          'agentIdSchemes',
          res.agent_external_id_schemes,
        );
      });
    },
    removeContributor(context, contributorId) {
      // mark for deletion rather than deleting instantly
      let promises = [];
      promises.push(
        Agent.updateMeta(contributorId, {
          is_hidden: true,
          to_delete: true,
        }),
      );
      let agent = Agent.query().with('_activities').find(contributorId);
      agent.activities.forEach((a) => {
        promises.push(Activity.updateMeta(a.id, { to_delete: true }));
      });
      Promise.all(promises).then(() => {
        if (agent.citation) {
          Citation.query()
            .whereHas('agent', (q) => {
              q.where('isActive', true);
            })
            .orderBy('order')
            .get()
            .forEach((c, i) => {
              Citation.update({ where: c.id, data: { order: i + 1 } });
            });
        }
      });
    },
    syncAgent(context, contributorId) {
      // download details from external source
      Agent.updateMeta(contributorId, { syncing: true });
      return get('agent_external_read', { agent_id: contributorId, diff: true })
        .then((res) => {
          Agent.update({ where: contributorId, data: res });
          Agent.updateMeta(contributorId, { is_dirty: true });
        })
        .finally(() => Agent.updateMeta(contributorId, { syncing: false }));
    },
    toggleActivity(context, activityId) {
      let activity = Activity.query().with('meta').find(activityId);
      Activity.updateMeta(activityId, { to_delete: !activity.meta.to_delete });
    },
    purgeTemporary(context) {
      Meta.query()
        .where('is_temporary', true)
        .with('item')
        .get()
        .forEach((m) => {
          m.item.$delete();
        });
    },
  },
});

export default store;
