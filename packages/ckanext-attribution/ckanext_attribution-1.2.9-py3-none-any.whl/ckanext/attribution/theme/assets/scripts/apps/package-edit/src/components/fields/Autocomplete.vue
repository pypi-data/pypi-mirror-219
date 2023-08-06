<template>
  <div
    class="autocomplete"
    :class="hasLabel ? 'autocomplete-label' : 'autocomplete-no-label'"
  >
    <label :for="'autocomplete-text-' + itemId" v-if="hasLabel">{{
      label
    }}</label>
    <input
      class="autocomplete-text form-control"
      type="text"
      @input="debounced"
      :id="'autocomplete-text-' + itemId"
      autocomplete="off"
      v-model="textInput"
      @focusin="showOptions"
      placeholder="Type to search"
    />
    <div
      class="autocomplete-options"
      :id="'autocomplete-list-' + itemId"
      v-if="optionsShown && textInput"
    >
      <template v-for="(optBlock, optTitle) in optionBlocks">
        <div
          class="autocomplete-option autocomplete-block-title"
          v-if="optBlock.length > 0 && optTitle !== 'default'"
        >
          {{ optTitle }}
        </div>
        <div
          v-for="opt in optBlock"
          @click="optionChange(opt)"
          class="autocomplete-option"
        >
          {{ opt.label }}
        </div>
      </template>
      <div
        class="autocomplete-option autocomplete-block-title"
        v-if="optionCount === 0 && !typing && !loading"
      >
        <slot>No results found</slot>
      </div>
      <div
        class="autocomplete-option null-option"
        @click="optionChange({ label: null, value: null })"
      >
        -- cancel --
      </div>
    </div>
    <span
      class="expand-bar"
      @click="hideOptions"
      v-if="optionsShown && textInput"
    >
      <i class="fas fa-caret-up"></i>
    </span>
    <i
      class="box-status-icon fas"
      :class="boxIcon"
      :title="failed"
      @click="$emit('cancel')"
    ></i>
  </div>
</template>

<script>
import debounce from 'lodash.debounce';

export default {
  name: 'Autocomplete',
  props: {
    options: [Array, Object],
    value: [String, Object],
    itemId: String,
    label: String,
    delay: { type: Number, default: 200 },
    loading: Boolean,
    failed: [Error, Object],
  },
  data: function () {
    return {
      textInput: null,
      optionsShown: false,
      typing: false,
    };
  },
  computed: {
    hasLabel() {
      return this.label && this.label !== '';
    },
    optionBlocks() {
      if (Array.isArray(this.options)) {
        return {
          default: this.options,
        };
      } else {
        let defaultFirst = {};
        Object.entries(this.options)
          .sort((a, b) => {
            return a[0] === 'default' ? -1 : b[0] === 'default' ? 1 : 0;
          })
          .forEach((a) => {
            defaultFirst[a[0]] = a[1];
          });
        return defaultFirst;
      }
    },
    optionCount() {
      return Object.values(this.optionBlocks).reduce((total, currentValue) => {
        return total + currentValue.length;
      }, 0);
    },
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
    showOptions() {
      this.textChange();
      this.optionsShown = true;
    },
    hideOptions() {
      setTimeout(() => {
        this.optionsShown = false;
      }, 200);
    },
    textChange() {
      this.$emit('typing', this.textInput);
      this.typing = false;
    },
    optionChange(opt) {
      this.optionsShown = false;
      this.textInput = opt.label;
      this.$emit('input', opt.value);
    },
    debounced() {
      this.typing = true;
      this._debounced();
    },
  },
  created() {
    this._debounced = debounce(this.textChange, this.delay, {
      maxWait: this.delay,
    });
    if (this.value) {
      let matchingOptions = this.options.filter((o) => o.value === this.value);
      if (matchingOptions.length > 0) {
        this.textInput = matchingOptions[0].label;
      }
    }
    this.$parent.$on('custom-option', this.optionChange);
  },
  watch: {
    value() {
      if (!this.value) {
        this.textInput = null;
      }
    },
  },
};
</script>
