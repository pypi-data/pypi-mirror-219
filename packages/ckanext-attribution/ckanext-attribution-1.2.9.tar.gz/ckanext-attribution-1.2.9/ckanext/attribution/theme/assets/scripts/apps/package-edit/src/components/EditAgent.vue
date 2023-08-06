<template>
  <div
    class="agent-edit-block agent-detail"
    :class="'agent-' + edits.agent_type.toLowerCase()"
  >
    <Errors v-if="showErrors" :errors="errors"></Errors>
    <div class="agent-header">
      <AgentTypeField v-model="edits.agent_type" />
      <span class="display-name">
        <em>{{ displayName }}</em>
      </span>
      <div class="edit-icons">
        <span
          class="edit-icon"
          title="Download contributor details from external source"
          v-if="edits.external_id"
          @click="syncAgent"
        >
          <i
            class="fas"
            :class="
              loading.externalId
                ? 'fa-spinner fa-spin'
                : 'fa-arrow-alt-circle-down'
            "
          ></i>
        </span>
        <span
          class="edit-icon"
          title="Remove this contributor"
          v-if="!contributor.meta.is_temporary"
          @click="eventBus.$emit(events.removeContributor, contributorId)"
        >
          <i class="fas fa-minus-circle"></i>
        </span>
      </div>
    </div>
    <div class="agent-id-edit attribution-row">
      <select-field
        v-model="edits.external_id_scheme"
        :options="Object.entries(controlledLists.agentIdSchemes)"
        :opt-label="(o) => o[1].label"
        :opt-value="(o) => o[0]"
        :class="['wrap-small']"
      >
        External ID scheme
      </select-field>
      <ValidatedField
        v-model="edits.external_id"
        :validator="validateExternalId"
        ref="externalId"
        :placeholder="
          controlledLists.agentIdSchemes[edits.external_id_scheme].label
        "
        :class="['wrap-small']"
        @validated="(x) => $set(valid, 'externalId', x)"
      >
        <i
          :class="
            controlledLists.agentIdSchemes[edits.external_id_scheme].fa_icon
          "
        ></i>
        {{ controlledLists.agentIdSchemes[edits.external_id_scheme].label }}
      </ValidatedField>
    </div>
    <div class="expand-bar" title="Expand" @click="expand = !expand">
      <i class="fas" :class="expand ? 'fa-caret-up' : 'fa-caret-down'"></i>
      <small>Show all edit options</small>
      <i class="fas" :class="expand ? 'fa-caret-up' : 'fa-caret-down'"></i>
    </div>
    <template v-if="expand">
      <div class="agent-name-edit attribution-row">
        <template v-if="edits.agent_type === 'person'">
          <text-field
            v-model="edits.family_name"
            :cls="['wrap-small']"
            @leave="checkDuplicates"
          >
            Family name
          </text-field>
          <text-field
            v-model="edits.given_names"
            :cls="['wrap-small']"
            @leave="checkDuplicates"
          >
            Given name(s)
          </text-field>
          <div class="attribution-field one-line" v-for="fieldId in idGen">
            <label :for="fieldId"> Given names first </label>
            <input
              :id="fieldId"
              type="checkbox"
              v-model="edits.given_names_first"
            />
          </div>
          <help-tooltip>
            Does this person's culture or language typically place given or
            family names first? (this does not affect sorting)
          </help-tooltip>
        </template>
        <template v-if="edits.agent_type !== 'person'">
          <text-field v-model="edits.name" @leave="checkDuplicates">
            Name
          </text-field>
          <text-field v-model="edits.location" @leave="checkDuplicates">
            Location
          </text-field>
        </template>
        <div v-if="probableDuplicates.length > 0" style="grid-column: span 2">
          <small>
            <b
              >Please ensure this contributor is not duplicating any of these
              existing contributors:</b
            >
          </small>
          <div class="flex">
            <span v-for="d in probableDuplicates" style="margin-right: 5px">{{
              d.label
            }}</span>
          </div>
        </div>
      </div>
      <div
        class="agent-user-edit attribution-row"
        v-if="edits.agent_type === 'person'"
      >
        <autocomplete-field
          v-model="edits.user_id"
          @typing="updateUserOptions"
          :options="userOptions"
          label="Linked user account"
          :item-id="'agent-user-' + contributorId"
          v-if="!edits.user_id"
        >
        </autocomplete-field>
        <div class="attribution-field user-display" v-if="user">
          <label>Linked user account</label>
          <a :href="'/user/' + edits.user_id" target="_blank">
            {{ user }}
          </a>
          <i class="fas fa-times" @click="edits.user_id = null"></i>
        </div>
        <help-tooltip>
          If this contributor has a user account registered on this site,
          associate it here
        </help-tooltip>
      </div>
      <div
        class="agent-affiliations-edit attribution-row"
        v-if="edits.agent_type === 'person'"
      >
        <autocomplete-list
          v-model="affiliations"
          @typing="updateAffiliationOptions"
          :options="affiliationOptions"
          label="Add affiliation"
          :item-id="'agent-affiliation-' + contributorId"
        >
        </autocomplete-list>
        <help-tooltip>
          <!-- TODO: make agent edit page and add link here -->
          For affiliations that are associated with <em>this package only</em>.
          Only includes contributors that have already been added to this page.
        </help-tooltip>
      </div>
    </template>
    <div class="attribution-save" v-if="!contributor.meta.is_temporary">
      <span
        class="btn"
        :class="isValid ? 'btn-primary' : 'btn-disabled'"
        @click="saveEdit"
      >
        <i class="fas fa-save"></i>
        Save changes
      </span>
      <span class="btn btn-primary" @click="stopEdit">
        <i class="fas fa-times"></i>
        Cancel
      </span>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import { get, post } from '../api';
import EditBase from './bases/EditBase.vue';
import { Affiliation, Agent } from '../models/main';
import AgentTypeField from './fields/AgentTypeField.vue';
import ValidatedField from './fields/ValidatedField.vue';

const Errors = () => import(/* webpackChunkName: 'errors' */ './Errors.vue');

export default {
  name: 'EditAgent',
  extends: EditBase,
  components: {
    AgentTypeField,
    ValidatedField,
    Errors,
  },
  data: function () {
    return {
      affiliations: [],
      userOptions: [],
      affiliationOptions: [],
      user: null,
      probableDuplicates: [],
    };
  },
  computed: {
    contributor() {
      return Agent.query()
        .with('meta')
        .with('affiliations.other_agent')
        .with('affiliations.meta')
        .find(this.contributorId);
    },
    displayName() {
      if (this.edits.agent_type !== 'person') {
        return this.edits.name;
      }
      if (this.edits.given_names_first) {
        return [this.edits.given_names, this.edits.family_name].join(' ');
      } else {
        return [this.edits.family_name, this.edits.given_names].join(' ');
      }
    },
    isValid() {
      this.errors = [];
      let nameValid = false;
      let isEmpty = (v) => v === null || v === undefined || v.trim() === '';
      if (this.edits.agent_type !== 'person') {
        nameValid = !isEmpty(this.edits.name);
        if (!nameValid) {
          this.errors.push('Name not provided.');
        }
      } else {
        let familyName = !isEmpty(this.edits.family_name);
        if (!familyName) {
          this.errors.push('Family name not provided.');
        }
        let givenNames = !isEmpty(this.edits.given_names);
        if (!givenNames) {
          this.errors.push('Given names not provided.');
        }
        nameValid = givenNames && familyName;
      }
      let externalIdValid =
        this.valid.externalId || isEmpty(this.edits.external_id);
      let schemeLabel;
      if (!externalIdValid) {
        try {
          schemeLabel =
            this.controlledLists.agentIdSchemes[this.edits.external_id_scheme]
              .label;
        } catch (e) {
          schemeLabel = this.edits.external_id_scheme;
        }
        this.errors.push(`${schemeLabel} is not valid.`);
      }
      return nameValid && externalIdValid;
    },
  },
  methods: {
    ...mapActions(['removeContributor']),
    checkDuplicates() {
      if (!this.isValid) {
        this.$set(this, 'probableDuplicates', []);
        return;
      }
      get('agent_list', { q: this.displayName, mode: 'duplicates' }).then(
        (agents) => {
          this.$set(
            this,
            'probableDuplicates',
            agents
              .map((agent) => {
                let label = agent.display_name;
                if (agent.external_id) {
                  label += ` (${agent.external_id})`;
                }
                return {
                  label: label,
                  value: agent,
                };
              })
              .filter((agent) => {
                if (!this.contributorId) return true;
                return this.contributorId !== agent.value.id;
              }),
          );
        },
      );
    },
    refresh() {
      this.edits = this.contributor.getCopy();
      this.affiliations = this.contributor.affiliations
        .filter((a) => !a.meta.to_delete)
        .map((a) => {
          return {
            label: a.other_agent.displayName,
            value: a.other_agent_id,
            record: a.other_agent,
          };
        });
      // set some defaults
      if (!this.edits.agent_type && !this.edits.external_id_scheme) {
        this.$set(
          this.edits,
          'agent_type',
          Object.keys(this.controlledLists.agentTypes)[0],
        );
      }
      if (!this.edits.agent_type && this.edits.external_id_scheme) {
        let hasAsDefault = Object.entries(
          this.controlledLists.agentTypes,
        ).filter((t) => t[1].default === this.edits.external_id_scheme);
        if (hasAsDefault.length > 0) {
          this.$set(this.edits, 'agent_type', hasAsDefault[0][0]);
        }
      }
      if (!this.edits.external_id_scheme) {
        this.$set(
          this.edits,
          'external_id_scheme',
          this.controlledLists.agentTypes[this.edits.agent_type].default_scheme,
        );
      }
      if (this.edits.given_names_first === undefined) {
        // TODO: do i need this?
        this.$set(this.edits, 'given_names_first', true);
      }

      // get user info
      if (this.edits.user_id) {
        get('user_show', { id: this.edits.user_id }).then((d) => {
          this.user = d.display_name;
        });
      }
      this.$emit('validated', this.isValid);
    },
    saveEdit() {
      let ableToSave = this.isValid && this.canSave;
      this.showErrors = !ableToSave;
      if (!ableToSave) {
        return;
      }

      let promises = [];

      if (this.settings.canEdit && !this.contributor.meta.is_new) {
        Object.entries(this.edits).every((e) => {
          if (this.contributor[e[0]] !== e[1]) {
            promises.push(
              Agent.updateMeta(this.contributorId, { is_dirty: true }),
            );
            return false;
          } else {
            return true;
          }
        });
      }

      // add new affiliations
      let newAffiliations = this.affiliations
        .filter((a) => {
          return (
            this.contributor.affiliations.findIndex(
              (e) => e.other_agent_id === a.value,
            ) === -1
          );
        })
        .map((a) => {
          let body = {
            agent_id: this.contributorId,
            other_agent_id: a.value,
            package_id: this.settings.packageId,
            meta: {
              is_new: true,
              is_temporary: this.contributor.is_temporary,
            },
          };

          if (!Agent.query().where('id', a.value).exists()) {
            a.record.meta = { is_new: true };
            promises.push(Agent.insert({ data: a.record }));
          }

          return body;
        });
      promises.push(Affiliation.insert({ data: newAffiliations }));

      // mark any deleted ones as 'to_delete'
      this.contributor.affiliations
        .filter((a) => {
          return (
            this.affiliations.findIndex((e) => e.value === a.other_agent_id) ===
            -1
          );
        })
        .forEach((a) => {
          promises.push(Affiliation.updateMeta(a.id, { to_delete: true }));
        });

      promises.push(
        Agent.update({
          where: this.contributorId,
          data: this.edits,
        }),
      );

      return Promise.all(promises)
        .then(() => {
          this.$emit(this.events.editsSaved);
        })
        .catch((e) => console.error(e))
        .finally(() => {
          this.stopEdit();
        });
    },
    stopEdit() {
      Agent.updateMeta(this.contributorId, { is_editing: false }).then(() => {
        this.$emit(this.events.editsDone);
      });
    },
    syncAgent() {
      this.loading.externalId = true;
      get('agent_external_read', {
        external_id: this.edits.external_id,
        external_id_scheme: this.edits.external_id_scheme,
      })
        .then((res) => {
          Object.entries(res).forEach((x) => {
            this.edits[x[0]] = x[1];
          });
        })
        .finally(() => {
          this.loading.externalId = false;
        });
    },
    updateAffiliationOptions: function (input) {
      let q = Agent.query()
        .where('isActive', true)
        .where((a) => a.id !== this.contributorId)
        .where(
          (a) => this.affiliations.findIndex((v) => v.value === a.id) === -1,
        );
      if (input && input !== '') {
        q = q.where((a) => {
          let inpt = input.toLowerCase();
          let matchFamily = a.family_name
            ? a.family_name.toLowerCase().startsWith(inpt)
            : false;
          let matchGiven = a.given_names
            ? a.given_names.toLowerCase().startsWith(inpt)
            : false;
          let matchName = a.name
            ? a.name.toLowerCase().startsWith(inpt)
            : false;
          return matchFamily || matchGiven || matchName;
        });
      }
      this.affiliationOptions = q.get().map((opt) => {
        return {
          label: opt.displayName,
          value: opt.id,
          record: opt,
        };
      });
    },
    updateUserOptions(input) {
      if (input === '' || input === null) {
        this.userOptions = [];
        return;
      }
      get('user_list', { q: input }).then((users) => {
        this.userOptions = users.map((user) => {
          return { label: user.display_name, value: user.id };
        });
      });
    },
    validateExternalId(input) {
      if (!input) {
        return new Promise((resolve) => {
          resolve(null);
        });
      }
      return post(
        'validate_external_id',
        {
          external_id: input,
          external_id_scheme: this.edits.external_id_scheme,
        },
        'validateExternalId',
      ).then((res) => {
        if (res.id) {
          return res.id;
        } else {
          throw new Error(res.error || 'Not valid');
        }
      });
    },
  },
  created: function () {
    this.refresh();
    this.expand = !this.isValid;
    this.eventBus.$on(this.events.saveAgent, (agentId) => {
      if (agentId === this.contributorId) {
        this.saveEdit();
      }
    });
  },
  watch: {
    'edits.user_id': function () {
      if (this.edits.user_id) {
        get('user_show', { id: this.edits.user_id }).then((d) => {
          this.user = d.display_name;
        });
      } else {
        this.user = null;
      }
    },
  },
};
</script>
