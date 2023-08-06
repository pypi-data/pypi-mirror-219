<template>
  <div class="activity-edit-block">
    <Errors v-if="showErrors" :errors="errors"></Errors>
    <div class="activity-edit-fields attribution-row">
      <select-field
        v-model="edits.scheme"
        :options="Object.keys(controlledLists.activityTypes)"
        @input="getOptions(edits.scheme)"
      >
        Role scheme
        <template #help>
          Standardised role taxonomies like
          <a href="http://credit.niso.org" target="_blank">CRediT</a> and
          <a
            href="https://schema.datacite.org/meta/kernel-4/include/datacite-contributorType-v4.xsd"
            target="_blank"
            >DataCite's contributor types</a
          >
          enables more accurate attribution of work.
          <div v-if="settings.doiPlugin">
            DataCite roles will be included in the DOI metadata as "contributor
            type".
          </div>
        </template>
      </select-field>
      <select-field
        v-model="edits.activity"
        :options="activityOptions"
        :opt-value="(o) => o.name"
        :opt-label="(o) => o.name"
        @input="getAgents"
        v-if="edits.scheme"
      >
        Contribution role
      </select-field>
      <select-field
        v-model="edits.level"
        :options="controlledLists.activityLevels"
      >
        Contribution level
        <template #help>
          Optional; the status of this contributor within this particular role,
          as defined by
          <a href="http://credit.niso.org" target="_blank">CRediT</a>.
        </template>
      </select-field>
      <div class="attribution">
        <datefield v-model="edits.time" placeholder="Select date (optional)">
          Contribution date
          <template #help>
            Optional; can be used as a start date, or if the work only took
            place on a single day, etc.
          </template>
        </datefield>
      </div>
    </div>
    <div class="expand-bar" title="Expand" @click="expand = !expand">
      <i class="fas" :class="expand ? 'fa-caret-up' : 'fa-caret-down'"></i>
      <small>Advanced options</small>
      <i class="fas" :class="expand ? 'fa-caret-up' : 'fa-caret-down'"></i>
    </div>
    <template v-if="expand">
      <div class="activity-sorted-agents attribution-row">
        <div><b>Ordered contributors</b></div>
        <div class="help-icon">
          <i class="fas fa-question-circle"></i>
          <div class="help-tooltip" role="tooltip">
            Contributors that should be listed in a particular order when
            citing.
          </div>
        </div>
        <draggable
          v-model="sortedAgents"
          group="allAgents"
          @change="updateOrder"
        >
          <div
            v-for="item in sortedAgents"
            class="activity-agent"
            :class="item.id === activityId ? 'active-agent' : ''"
          >
            <i class="fas fa-arrows"></i>
            <span>{{ item.name }}</span>
            <span>{{ item.order }}</span>
          </div>
        </draggable>
      </div>
      <div class="activity-unsorted-agents attribution-row">
        <div><b>Unordered contributors</b></div>
        <div class="help-icon">
          <i class="fas fa-question-circle"></i>
          <div class="help-tooltip" role="tooltip">
            Contributors that do not have to be listed in any particular order.
            These will be listed
            <em>after</em> the ordered contributors.
          </div>
        </div>
        <draggable
          v-model="unsortedAgents"
          group="allAgents"
          @change="updateOrder"
        >
          <div
            v-for="item in unsortedAgents"
            class="activity-agent"
            :class="item.id === activityId ? 'active-agent' : ''"
          >
            <i class="fas fa-arrows"></i>
            <span>{{ item.name }}</span>
            <span>{{ item.order }}</span>
          </div>
        </draggable>
      </div>
    </template>
    <div class="attribution-save" v-if="!activity.meta.is_temporary">
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
import draggable from 'vuedraggable';
import DateField from './fields/DateField.vue';
import EditBase from './bases/EditBase.vue';
import Activity from '../models/activity';

const Errors = () => import(/* webpackChunkName: 'errors' */ './Errors.vue');

export default {
  name: 'EditActivity',
  extends: EditBase,
  props: {
    activityId: String,
  },
  components: {
    draggable,
    datefield: DateField,
    Errors,
  },
  data: function () {
    return {
      activityOptions: [],
      sortedAgents: [],
      unsortedAgents: [],
    };
  },
  computed: {
    activity() {
      return Activity.query().with('meta').with('agent').find(this.activityId);
    },
    contributor() {
      return this.activity.agent;
    },
    isValid() {
      this.errors = [];
      if (!this.edits.activity) {
        this.errors.push('Activity not provided.');
      }
      return this.edits.activity !== null;
    },
  },
  methods: {
    refresh() {
      this.getOptions(this.activity.scheme).then(() => {
        this.edits = this.activity.getCopy();
        if (this.edits.activity) {
          this.getAgents(this.edits.activity);
        }
      });
      this.$emit('validated', this.isValid);
    },
    saveEdit() {
      let ableToSave = this.isValid && this.canSave;
      this.showErrors = !ableToSave;
      if (!ableToSave) {
        return;
      }

      // save the edits for this activity first
      let promises = [
        Activity.update({ where: this.activityId, data: this.edits }).then(
          () => {
            return Activity.updateMeta(this.activityId, {
              is_dirty: true,
              is_editing: false,
            });
          },
        ),
      ];

      // then update the order for the others
      this.sortedAgents.concat(this.unsortedAgents).forEach((a) => {
        if (!a.id) {
          return;
        }
        promises.push(
          Activity.update({ where: a.id, data: { order: a.order } }).then(
            () => {
              return Activity.updateMeta(a.id, { is_dirty: true });
            },
          ),
        );
      });

      return Promise.all(promises)
        .then(() => {
          this.$emit(this.events.editsSaved);
        })
        .catch((e) => console.error(e))
        .finally(() => {
          this.stopEdit();
        });
    },
    getAgents(input) {
      this.$set(this.edits, 'activity', input);
      let allAgents = Activity.query()
        .with('agent')
        .where('activity', this.edits.activity)
        .orderBy((a) => a.order)
        .get()
        .map((a) => {
          return {
            name: a.agent.displayName,
            id: a.id,
            order: a.order,
          };
        });
      this.sortedAgents = allAgents.filter((a) => a.order !== null);
      this.unsortedAgents = allAgents.filter((a) => a.order === null);

      if (this.activity.activity !== this.edits.activity) {
        this.unsortedAgents.push({
          name: this.contributor.displayName,
          id: null,
          order: null,
        });
      }
    },
    getOptions(scheme) {
      // this needs to be returned as a promise rather than using a computed property, because
      // the options on the select field need to be changed *before* the value is changed
      return new Promise((resolve) => {
        if (!scheme) {
          this.activityOptions = [];
          resolve();
        }
        let otherActivities = this.contributor.activities
          .filter((a) => {
            return a.id !== this.activityId && a.scheme === scheme;
          })
          .map((a) => a.activity);
        this.activityOptions = this.controlledLists.activityTypes[
          scheme
        ].filter((a) => {
          return !otherActivities.includes(a.name);
        });
        resolve();
      });
    },
    updateOrder() {
      this.sortedAgents = this.sortedAgents.map((a, i) => {
        a.order = i + 1;
        if (a.id === this.activityId) {
          this.$set(this.edits, 'order', i + 1);
        }
        return a;
      });
      this.unsortedAgents = this.unsortedAgents.map((a) => {
        a.order = null;
        if (a.id === this.activityId) {
          this.$set(this.edits, 'order', null);
        }
        return a;
      });
    },
  },
  created: function () {
    this.refresh();
    this.eventBus.$on(this.events.saveActivity, (activityId) => {
      if (activityId === this.activityId) {
        this.saveEdit();
      }
    });
  },
  watch: {
    activityId() {
      this.refresh();
    },
  },
};
</script>
