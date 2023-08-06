<template>
  <div class="contribution-block" :class="{ cited: contributor.citeable }">
    <div class="citation-ordering">
      <template v-if="contributor.citeable">
        <i
          class="fas fa-angle-up fa-lg btn-1"
          :class="{ 'btn-disabled': contributor.citation.order === 1 }"
          @click="moveCitation(-1)"
        ></i>
        <span title="Cited author" class="btn-2">{{
          contributor.citation.order
        }}</span>
        <i
          class="fas fa-angle-down fa-lg btn-3"
          :class="{ 'btn-disabled': lastCited }"
          @click="moveCitation(1)"
        ></i>
        <i
          class="fas fa-minus btn-4"
          title="Remove from citation"
          @click="toggleCitation"
        ></i>
      </template>
      <template v-if="!contributor.citeable">
        <i
          class="fas fa-plus btn-2"
          title="Include in citation"
          @click="toggleCitation"
        ></i>
      </template>
    </div>
    <div :class="{ 'agent-dirty': contributor.meta.is_dirty }">
      <ShowAgent
        :contributor-id="contributorId"
        v-if="!contributor.meta.is_editing"
      />
      <EditAgent
        :contributor-id="contributorId"
        v-if="contributor.meta.is_editing"
      />
      <div class="agent-activities">
        <ShowActivity
          v-for="activity in contributor.activities"
          :key="activity.id"
          :activity-id="activity.id"
          v-on:toggle-edit="toggleActivityEdit(activity.id)"
        />
        <span @click="newActivity" class="icon-btn">
          <i
            class="fas fa-lg"
            :class="activityCreating ? 'fa-times-circle' : 'fa-plus-circle'"
          ></i>
        </span>
      </div>
      <EditActivity
        v-if="activityEditing"
        :activity-id="activityEditing"
        @done="stopEdit"
      />
    </div>
  </div>
</template>

<script>
const ShowAgent = () =>
  import(/* webpackChunkName: 'show-agent' */ './ShowAgent.vue');
const ShowActivity = () =>
  import(/* webpackChunkName: 'show-activity' */ './ShowActivity.vue');
const EditAgent = () =>
  import(/* webpackChunkName: 'edit-agent' */ './EditAgent.vue');
const EditActivity = () =>
  import(/* webpackChunkName: 'edit-activity' */ './EditActivity.vue');
import { mapState } from 'vuex';
import Base from './bases/Base.vue';
import { Activity, Agent, Citation } from '../models/main';

export default {
  name: 'ContributionBlock',
  extends: Base,
  components: {
    EditAgent,
    EditActivity,
    ShowActivity,
    ShowAgent,
  },
  data: function () {
    return {
      activityEditing: null,
    };
  },
  computed: {
    ...mapState(['settings', 'controlledLists']),
    activityCreating() {
      return this.activityEditing
        ? Activity.query().with('meta').find(this.activityEditing).meta.is_new
        : false;
    },
    lastCited() {
      if (this.contributor.citeable) {
        return (
          Agent.query()
            .where('isActive', true)
            .where('citeable', true)
            .count() === this.contributor.citation.order
        );
      }
    },
  },
  methods: {
    toggleActivityEdit(activityId) {
      if (activityId && this.activityEditing !== activityId) {
        this.activityEditing = activityId;
      } else {
        this.activityEditing = null;
      }
    },
    stopEdit() {
      this.activityEditing = null;
    },
    newActivity() {
      if (this.activityCreating) {
        Activity.delete(this.activityEditing);
        this.activityEditing = null;
      } else {
        Activity.insert({
          data: {
            agent_id: this.contributorId,
            package_id: this.settings.packageId,
            meta: {
              is_new: true,
            },
          },
        }).then((records) => {
          this.activityEditing = records.activities[0].id;
        });
      }
    },
    moveCitation(by) {
      let contributorId = this.contributor.citation.id;
      let currentPosition = this.contributor.citation.order;
      let newPosition = currentPosition + by;
      if (newPosition < 1 || (this.lastCited && by === 1)) {
        return;
      }
      Citation.update({
        where: (c) => c.order === newPosition,
        data: {
          order: currentPosition,
        },
      })
        .then((records) => {
          return Citation.updateMeta(records[0].id, { is_dirty: true });
        })
        .then(() => {
          return Citation.update({
            where: contributorId,
            data: {
              order: newPosition,
            },
          });
        })
        .then((record) => {
          return Citation.updateMeta(record.id, { is_dirty: true });
        });
    },
    toggleCitation() {
      if (this.contributor.citeable) {
        let currentPosition = this.contributor.citation.order;
        Citation.update({
          where: (c) => c.order > currentPosition,
          data(c) {
            c.order -= 1;
          },
        }).then((records) => {
          records.forEach((r) => {
            Citation.updateMeta(r.id, { is_dirty: true });
          });
        });
        Citation.updateMeta(this.contributor.citation.id, {
          to_delete: true,
        });
      } else {
        let citationCount = Agent.query()
          .where('isActive', true)
          .where('citeable', true)
          .count();
        if (this.contributor.citation) {
          Citation.update({
            where: this.contributor.citation.id,
            data: {
              order: citationCount + 1,
            },
          });
          Citation.updateMeta(this.contributor.citation.id, {
            to_delete: false,
          });
        } else {
          Citation.insert({
            data: {
              activity: '[citation]',
              scheme: 'internal',
              agent_id: this.contributorId,
              package_id: this.settings.packageId,
              order: citationCount + 1,
              meta: { is_new: true },
            },
          });
        }
      }
    },
  },
  watch: {
    activityEditing(newId, oldId) {
      if (oldId) {
        Activity.updateMeta(oldId, { is_editing: false }).catch(() => {});
      }
      if (newId) {
        Activity.updateMeta(newId, { is_editing: true }).catch(() => {});
      }
    },
  },
};
</script>
