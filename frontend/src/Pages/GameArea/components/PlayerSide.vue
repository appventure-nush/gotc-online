<script lang="ts">
import {defineComponent} from 'vue'
import Hand from "./Hand.vue";
import Pile from "./Pile.vue";

export default defineComponent({
  name: "PlayerSide",
  components: {Hand, Pile}
})
</script>

<template>
  <div>
    <Hand class="hand"/>
    <Pile class="pile"/>
  </div>
</template>

<style scoped>

.hand{
  position: absolute;
  bottom: 0;
  left: 0;
  height: 40%;
  width: 75%;
  background-color: rgba(70,130,180,0.2);
}

.pile{
  position: absolute;
  bottom: 0;
  right: 0;
  height: 40%;
  width: 25%;
  background-color: rgba(70, 180, 130, 0.2);
}

</style>