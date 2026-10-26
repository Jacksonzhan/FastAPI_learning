<template>
  <svg aria-hidden="true" class="scg-icon">
    <use :href="iconName" :fill="color" />
  </svg>
</template>

<script setup>
import {computed} from "vue";

const props = defineProps({
  iconClass: {
    type: String,
    required: true
  },
  color: {
    type: String,
    default: ''
  }
})

//生成插件要求的完整图标引用ID
const iconName = computed(() => `#icon-${props.iconClass}`)
</script>

<style scoped>
.scg-icon {
  font-size: 25px;
  width: 1em;
  height: 1em;
  position: relative;
  fill: currentColor;
  vertical-align: -2px;
}
</style>
