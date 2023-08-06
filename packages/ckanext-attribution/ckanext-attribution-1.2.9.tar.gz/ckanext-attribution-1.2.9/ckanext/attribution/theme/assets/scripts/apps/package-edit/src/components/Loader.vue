<template>
  <div class="attribution-loading">
    <slot>
      <h3>Loading...</h3>
    </slot>
    <i class="fas fa-spinner fa-spin fa-2x inline-icon-right"></i>
  </div>
</template>

<script>
export default {
  name: 'Loader',
};
</script>
