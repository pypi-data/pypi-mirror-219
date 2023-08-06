<template></template>

<script>
import { eventBus, events } from '../../eventbus';
import Agent from '../../models/agent';
import { mapState } from 'vuex';

export default {
  name: 'Base',
  abstract: true,
  props: {
    contributorId: String,
  },
  data: function () {
    return {
      eventBus: eventBus,
      events: events,
    };
  },
  computed: {
    ...mapState(['settings', 'controlledLists']),
    contributor() {
      return Agent.query()
        .with('meta')
        .with('citation')
        .find(this.contributorId);
    },
    isValid() {
      return true;
    },
  },
  methods: {
    refresh() {
      this.$emit('validated', this.isValid);
    },
  },
  created() {
    this.refresh();
  },
  watch: {
    isValid(n) {
      this.$emit('validated', n);
    },
  },
};
</script>
