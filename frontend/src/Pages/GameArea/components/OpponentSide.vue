<script lang="ts">
import {defineComponent} from 'vue'
import OpponentField from "./OpponentField.vue";
import MoveNotifier from "./MoveNotifier.vue";

export default defineComponent({
  name: "OpponentSide",
  components: {MoveNotifier, OpponentField}
})
</script>

<template>
  <div>
    <OpponentField class="oppfield"/>
    <MoveNotifier class="movenotif"/>
  </div>
</template>

<style scoped>

.oppfield{
  position: absolute;
  top: 0;
  left: 0;
  height: 70%;
  width: 100%;
  background-color: rgba(175, 52, 52, 0.5);
}

.movenotif{
  position: absolute;
  bottom: 0;
  left: 0;
  height: 30%;
  width: 100%;
  background-color: rgba(85, 180, 70, 0.6);
}

</style>