<script lang="ts">
import {defineComponent} from 'vue'
import {playerCardsStore} from "./PlayerCardsStore";

export default defineComponent({
  name: "MoveNotifier",
  setup() {
    const playerCards = playerCardsStore
    return { playerCards }
  },
  computed:{
    dialogNormal(){
      return playerCardsStore.showDialogNormal ? "flex": "none"
    }
  }
})
</script>

<template>
  <div class="movenotif-component-div">
    <p class="allowlinebreaks-p">{{ playerCards.moveNotifier }}</p>
    <div class="dial">
      <button @click="() => {playerCards.showDialogNormal = false
      playerCards.playHand(playerCards.index, -1)}">Draw 2</button>
      <!-- todo only 1 card in discard should not display a dialog-->
      <button @click="() => {
       playerCards.showDialogNormal = false
       if (playerCards.discardDeck.length != 0) {
        playerCards.showDiscardPlay = true
        playerCards.moveNotifier = 'Now select a card from the discard to restore.'
       } else {
         playerCards.playHand(playerCards.index)
       }}">Select from discard</button>
      <button @click="playerCards.showDialogNormal = false">Cancel</button>
    </div>
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

.dial{
  display: v-bind(dialogNormal);
  top: 10%;
  position: absolute;
  right: 5%;
  flex-direction: row;
  background: #80808080;
  justify-content: center;
  align-items: center;
  padding: 1em;
  row-gap: .5em;
}

</style>