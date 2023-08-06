<template>
  <div
    class="agent-activity"
    :class="[
      { 'is-deleted': activity.meta.to_delete },
      'activity-scheme-' + activity.scheme,
    ]"
  >
    <div
      @click="toggleEdit"
      class="clickable-text"
      :class="{ clicked: activity.meta.is_editing }"
    >
      <span>{{ activity.activity }}</span>
      <span v-if="activity.order"> (#{{ activity.order }})</span>
    </div>
    <i
      class="fas fa-sm fa-minus-circle"
      @click="toggleActivity(activityId)"
    ></i>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import Activity from '../models/activity';

export default {
  name: 'ShowActivity',
  props: ['activityId'],
  data: function () {
    return {};
  },
  computed: {
    activity() {
      return Activity.query().with('meta').find(this.activityId);
    },
  },
  methods: {
    ...mapActions(['toggleActivity']),
    toggleEdit() {
      if (this.activity.meta.to_delete) {
        this.toggleActivity(this.activityId);
      }
      this.$emit('toggle-edit');
    },
  },
};
</script>
