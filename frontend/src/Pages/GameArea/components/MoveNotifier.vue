<script lang="ts">
import {defineComponent} from 'vue'
import {playerCardsStore} from "./PlayerCardsStore";

export default defineComponent({
  name: "MoveNotifier",
  setup() {
    const playerCards = playerCardsStore
    return { playerCards }
  }
})
</script>

<template>
  <div class="movenotif-component-div">
    <p class="allowlinebreaks-p">{{ playerCards.moveNotifier }}</p>
  </div>
</template>

<style scoped>

.movenotif-component-div{
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
}

.allowlinebreaks-p {
  white-space: pre-line;
}

</style>