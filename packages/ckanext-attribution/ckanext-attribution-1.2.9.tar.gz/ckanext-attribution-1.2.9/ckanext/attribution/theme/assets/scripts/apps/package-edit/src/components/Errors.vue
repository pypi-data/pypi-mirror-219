<template>
  <div class="attribution-errors-block">
    <ul>
      <li v-for="e in errors">{{ e }}</li>
    </ul>
  </div>
</template>

<script>
export default {
  name: 'Errors',
  props: ['errors'],
};
</script>
