<script lang="ts">
import {defineComponent} from 'vue'
import {playerCardsStore} from "./PlayerCardsStore";

export default defineComponent({
  name: "MoveNotifier",
  setup() {
    const playerCards = playerCardsStore
    return { playerCards }
  },
  computed:{ // use "display" css property to show dialogs based on variables
    dialogNormal() {
      return playerCardsStore.showDialogNormal ? "flex": "none"
    },
    dialogDefence() {
      return playerCardsStore.showDialogDefence ? "flex": "none"
    },
    dialogField() {
      return playerCardsStore.showDialogField ? "flex": "none"
    },
    dialogHand() {
      return playerCardsStore.showDialogHand ? "flex": "none"
    },
    dialogForfeit() {
      return playerCardsStore.showForfeit ? "flex": "none"
    }
  }
})
</script>

<template>
  <div class="movenotif-component-div">
    <p class="movenotif-p">{{ playerCards.moveNotifier }}</p>
    <!-- the confirmation/selection dialogs are displayed here -->
    <!-- todo only 1 choice should not display a dialog-->
    <div class="dial dialognormal">
      <button @click="() => {playerCards.showDialogNormal = false
      playerCards.playHand(playerCards.index, -1)}">Draw 2</button>
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
    <div class="dial dialogdefence">
      <button @click="() => {playerCards.showDialogDefence = false
      playerCards.playHand(playerCards.index)}">Confirm</button>
      <button @click="playerCards.showDialogDefence = false">Cancel</button>
    </div>
    <div class="dial dialogfield">
      <button @click="() => {playerCards.showDialogField = false
      playerCards.playHand(playerCards.index)}">Confirm</button>
      <button @click="playerCards.showDialogField = false">Cancel</button>
    </div>
    <div class="dial dialoghand">
      <button @click="() => {playerCards.showDialogHand = false
      playerCards.playHand(playerCards.index)}">Confirm</button>
    </div>
    <div class="dial dialogforfeit">
      <button @click="playerCards.forfeitGame()">Forfeit (irreversible!)</button>
      <button @click="playerCards.showForfeit = false">Cancel</button>
    </div>
  </div>
</template>

<style scoped>

.movenotif-component-div{
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
}

.movenotif-p {
  white-space: pre-line;
  text-align: center;
}

.dial{
  position: relative;
  flex-direction: row;
  background: #80808080;
  justify-content: center;
  align-items: center;
  padding: .5em;
  gap: .5em;
}

.dialognormal {
  display: v-bind(dialogNormal);
}

.dialogdefence {
  display: v-bind(dialogDefence);
}

.dialogfield {
  display: v-bind(dialogField);
}

.dialoghand {
  display: v-bind(dialogHand);
}

.dialogforfeit {
  display: v-bind(dialogForfeit);
}

</style>