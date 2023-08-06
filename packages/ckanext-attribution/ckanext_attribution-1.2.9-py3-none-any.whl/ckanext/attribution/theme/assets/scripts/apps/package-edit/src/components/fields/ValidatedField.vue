<template>
  <div class="attribution-field-validated" :class="classes">
    <label :for="fieldId">
      <slot></slot>
    </label>
    <help-tooltip v-if="showHelpText">
      <slot name="help"></slot>
    </help-tooltip>
    <input
      class="form-control"
      :class="{ 'form-control-invalid': failed }"
      type="text"
      v-model="textValue"
      :id="fieldId"
      :placeholder="placeholder"
      @input="debouncedSetValue"
      @focusout="debouncedSetValue.flush"
    />
    <i
      class="box-status-icon fas"
      :class="boxIcon"
      :title="failed"
      @click="$emit('cancel')"
    ></i>
  </div>
</template>

<script>
import TextField from './TextField.vue';
import debounce from 'lodash.debounce';

export default {
  name: 'ValidatedField',
  extends: TextField,
  props: {
    validator: Function,
  },
  data: function () {
    return {
      failed: false,
      loading: false,
      typing: false,
      textValue: null,
    };
  },
  computed: {
    boxIcon() {
      return this.failed
        ? 'fa-times'
        : this.loading
        ? 'fa-spinner fa-spin'
        : this.typing
        ? 'fa-xs fa-ellipsis-h'
        : 'fa-check';
    },
  },
  methods: {
    validate() {
      this.loading = true;
      this.failed = null;
      this.validator(this.textValue)
        .then((res) => {
          this.$emit('input', res);
          this.textValue = res;
        })
        .catch((e) => {
          this.failed = e;
          this.$emit('input', this.textValue);
        })
        .finally(() => {
          this.loading = false;
          this.$emit('validated', !this.failed);
        });
    },
  },
  created() {
    this.debouncedSetValue = debounce(this.validate, 500, { maxWait: 500 });
    this.textValue = this.value;
    this.validate();
  },
  watch: {
    value(n, o) {
      if (n && !this.loading) {
        this.textValue = n;
      }
    },
    loading(n, o) {
      if (!n) {
        if (this.value !== this.textValue && this.value) {
          this.textValue = this.value;
        }
      }
    },
  },
};
</script>
