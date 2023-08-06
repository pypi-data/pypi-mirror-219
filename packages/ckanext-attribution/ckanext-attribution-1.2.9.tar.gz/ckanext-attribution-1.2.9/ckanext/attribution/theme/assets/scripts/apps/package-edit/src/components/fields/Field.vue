<template>
  <div :class="classes">
    <label :for="fieldId">
      <slot></slot>
    </label>
    <help-tooltip v-if="showHelpText">
      <slot name="help"></slot>
    </help-tooltip>
    <input
      class="form-control"
      :type="inputType"
      :value="value"
      :id="fieldId"
      @change="setValue"
      @focusout="leave"
    />
  </div>
</template>

<script>
import { nanoid } from 'nanoid';

export default {
  name: 'Field',
  props: ['value', 'inputType', 'cls'],
  data: function () {
    return {
      fieldId: nanoid(8),
    };
  },
  computed: {
    classes() {
      let classList = ['attribution-field'];
      if (this.cls) {
        classList = classList.concat(this.cls);
      }
      return classList;
    },
    showHelpText() {
      return !!this.$slots.help;
    },
  },
  methods: {
    setValue(event) {
      this.$emit('input', event.target.value);
    },
    leave(event) {
      this.$emit('leave');
    },
  },
};
</script>

<style scoped></style>
