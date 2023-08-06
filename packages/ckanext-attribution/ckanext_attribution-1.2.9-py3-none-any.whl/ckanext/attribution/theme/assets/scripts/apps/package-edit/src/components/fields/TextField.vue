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
      type="text"
      :value="value"
      :id="fieldId"
      :placeholder="placeholder"
      @input="debouncedSetValue"
      @focusout="leave"
    />
  </div>
</template>

<script>
import Field from './Field.vue';
import debounce from 'lodash.debounce';

export default {
  name: 'TextField',
  extends: Field,
  props: ['placeholder'],
  created() {
    this.debouncedSetValue = debounce(this.setValue, 500, { maxWait: 500 });
  },
  methods: {
    leave(event) {
      this.debouncedSetValue.flush();
      this.$emit('leave');
    },
  },
};
</script>
