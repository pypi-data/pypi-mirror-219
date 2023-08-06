<template></template>

<script>
import Base from './Base.vue';
import { nanoid } from 'nanoid';

export default {
  name: 'EditBase',
  extends: Base,
  abstract: true,
  props: {
    canSave: {
      default: () => true,
    },
  },
  data: function () {
    return {
      edits: {},
      errors: [],
      showErrors: false,
      loading: {},
      expand: false,
      valid: {},
    };
  },
  computed: {
    idGen() {
      return [nanoid(8)];
    },
  },
  methods: {
    saveEdit() {
      if (!this.isValid) {
        this.errors.push(['Not valid']);
      }
    },
    stopEdit() {
      this.$emit(this.events.editsDone);
    },
  },
  watch: {
    errors(n, o) {
      if (n.length === 0) {
        this.showErrors = false;
      }
    },
  },
};
</script>
