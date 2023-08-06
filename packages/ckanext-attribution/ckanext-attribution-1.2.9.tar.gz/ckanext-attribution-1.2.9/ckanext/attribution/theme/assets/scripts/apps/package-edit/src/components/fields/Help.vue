<template>
  <div
    class="help-icon"
    @mouseover="showBox = true"
    @mouseout="showBox = false"
  >
    <i class="fas fa-question-circle"></i>
    <div
      class="help-tooltip"
      role="tooltip"
      v-if="showBox"
      @mouseover="showBox = true"
      @mouseout="showBox = false"
    >
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Help',
  data: function () {
    return {
      showBox: false,
    };
  },
};
</script>
