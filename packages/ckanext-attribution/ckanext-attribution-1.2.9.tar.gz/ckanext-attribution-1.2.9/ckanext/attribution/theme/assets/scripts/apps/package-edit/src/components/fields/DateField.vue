<template>
  <div :class="classes">
    <label :for="fieldId">
      <slot></slot>
    </label>
    <help-tooltip v-if="showHelpText">
      <slot name="help"></slot>
    </help-tooltip>
    <input
      type="date"
      class="form-control"
      :value="dateOnly"
      :id="fieldId"
      :placeholder="placeholder"
      @change="setValue"
    />
  </div>
</template>

<script>
import Field from './Field.vue';

export default {
  name: 'DateField',
  extends: Field,
  props: ['placeholder'],
  computed: {
    dateOnly() {
      if (!this.value) {
        return;
      }
      try {
        let inputDate = new Date(this.value);
        return inputDate.toISOString().split('T')[0];
      } catch (e) {
        return this.value;
      }
    },
  },
};
</script>
