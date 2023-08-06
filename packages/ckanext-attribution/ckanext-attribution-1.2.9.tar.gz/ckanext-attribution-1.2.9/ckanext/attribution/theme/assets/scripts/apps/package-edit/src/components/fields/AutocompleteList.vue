<template>
  <div
    class="autocomplete"
    :class="hasLabel ? 'autocomplete-label' : 'autocomplete-no-label'"
  >
    <label :for="'autocomplete-text-list-' + itemId" v-if="hasLabel">{{
      label
    }}</label>
    <input
      class="autocomplete-text form-control"
      type="text"
      @input="debounced"
      :id="'autocomplete-text-list-' + itemId"
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
    <div class="autocomplete-list-items">
      <div v-for="item in valueList">
        <span>{{ item.label }}</span>
        <i class="fas fa-times" @click="removeItem(item)"></i>
      </div>
    </div>
    <i
      class="box-status-icon fas"
      :class="loading ? 'fa-spinner fa-spin' : 'fa-check'"
    ></i>
  </div>
</template>

<script>
import Autocomplete from './Autocomplete.vue';

export default {
  name: 'AutocompleteList',
  extends: Autocomplete,
  props: {
    value: Array,
  },
  data: function () {
    return {
      valueList: [],
    };
  },
  methods: {
    optionChange(opt) {
      this.optionsShown = false;
      this.textInput = null;
      if (!opt.value) {
        return;
      }
      this.valueList.push(opt);
      this.$emit('input', this.valueList);
    },
    removeItem(item) {
      this.valueList = this.valueList.filter((v) => v.value !== item.value);
      this.$emit('input', this.valueList);
    },
  },
  created() {
    this.valueList = [...this.value];
  },
};
</script>

<style scoped></style>
