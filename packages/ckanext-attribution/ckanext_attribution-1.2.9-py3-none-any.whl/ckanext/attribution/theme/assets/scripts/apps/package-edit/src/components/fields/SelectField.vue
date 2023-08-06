<template>
  <div :class="classes">
    <label :for="fieldId">
      <slot></slot>
    </label>
    <help-tooltip v-if="showHelpText">
      <slot name="help"></slot>
    </help-tooltip>
    <select
      class="form-control form-select"
      :value="value"
      :id="fieldId"
      @change="setValue"
    >
      <option v-for="opt in options" :value="optValue(opt)">
        {{ optLabel(opt) }}
      </option>
    </select>
  </div>
</template>

<script>
import Field from './Field.vue';

export default {
  name: 'SelectField',
  extends: Field,
  props: {
    options: {},
    optValue: { default: () => (o) => o },
    optLabel: { default: () => (o) => o },
  },
};
</script>
