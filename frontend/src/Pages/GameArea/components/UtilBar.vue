<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "UtilBar"
})
</script>

<template>
  <div class="utilbar-component-div" >
    <p>UTIL/TOOLBAR</p>
  </div>
</template>

<style scoped>

.utilbar-component-div{
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
  background-color: rgb(128,128,128,0.75);
}

</style>