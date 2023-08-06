<template>
  <div class="agent-type-edit" :class="classes">
    <span v-for="(info, name) in options" class="agent-type-option">
      <input
        type="radio"
        :value="name"
        @change="setValue"
        :id="optionId(name)"
        :checked="value === name"
      />
      <label :for="optionId(name)" :title="name">
        <i :class="info.fa_icon"></i>
      </label>
    </span>
  </div>
</template>

<script>
import Field from './Field.vue';
import { mapState } from 'vuex';

export default {
  name: 'AgentTypeField',
  extends: Field,
  computed: {
    ...mapState(['controlledLists']),
    options() {
      return this.controlledLists.agentTypes;
    },
  },
  methods: {
    optionId(name) {
      return 'agent-type-option-' + name + this.fieldId;
    },
  },
};
</script>
