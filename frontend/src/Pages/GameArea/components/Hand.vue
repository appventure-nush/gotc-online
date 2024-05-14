<script lang="ts">
import {defineComponent} from 'vue'
import CardHolder from "./CardHolder.vue";
import {playerCardsStore} from "./PlayerCardsStore";
import {userSignInStore} from "../../../components/UserSignInStore";

export default defineComponent({
  name: "Hand",
  components: {CardHolder},
  setup(){
    //this imports the playerCardsStore, allowing us to use the variables stored within
    const playerCards = playerCardsStore
    const userStore = userSignInStore
    return { playerCards, userStore }
  },
  beforeMount() {
    // subscribing to the store makes the callback function within the $subscribe function run whenever the userStore updates
    // see more here: https://pinia.vuejs.org/core-concepts/state.html#Subscribing-to-the-state
    // we did not pass {detached:true} so this subssctiption automatically ends when we unmount
    // next time we can also check if a game's going on after checking if the user's signed in
    this.userStore.$subscribe(() => {
      if(this.userStore.isSignedIn) this.playerCards.getHand()
    })
  },
  data(){
    return{

    }
  },
  computed:{
    showOpponentHand() {
      return (playerCardsStore.showOptionHand || playerCardsStore.showDialogHand) && !playerCardsStore.vetoShowOpponentHand
    }
  }
})
</script>

<!--
  This is the component that displays up to 7 cards in the player's hand

  Uses v-for to horizontally stack cardholders
  The hand itself is stored in the playerCards Store's handlist
  player logic can be attached to the CardHolder's playButtonFunc later
--->

<template>
  <div class="hand-component-div">
    <CardHolder v-for="(card,index) in playerCards.opponentHandTemp"
                v-if="showOpponentHand"
                :card-name="card['name']"
                :key="card['name']+index"
                :play-button-func="()=>{
                  playerCards.playHand(playerCards.index, index)
                  playerCards.showOptionHand = false
                }"
                :enable-play="playerCards.showOptionHand"
                :rename-play="'Discard'"
                class="handcard"
    />
    <CardHolder v-for="(card,index) in playerCards.handList"
                v-else
                :card-name="card['name']"
                :key="card['name']+index"
                :play-button-func="()=>{
                  if (playerCards.discardHand) {
                    playerCards.discardCardFromHand(index)
                  } else {
                    playerCards.vetoShowOpponentHand = false
                    if (card['requiresDialogNormal']) {
                      playerCards.showDialogNormal = true // dont forget to reset all dialogs
                      playerCards.showOptionDefence = false
                      playerCards.showDialogDefence = false
                      playerCards.showOptionField = false
                      playerCards.showDialogField = false
                      playerCards.showDialogHand = false
                      playerCards.showOptionHand = false
                      playerCards.index = index
                      playerCards.moveNotifier = 'Pick an option.'+card['warn']
                    } else if (card['requiresOptionDefence']) {
                      playerCards.showDialogNormal = false // dont forget to reset all dialogs
                      playerCards.showOptionField = false
                      playerCards.showDialogField = false
                      playerCards.showDialogHand = false
                      playerCards.showOptionHand = false
                      playerCards.index = index
                      if ((card['warn'] == '\nWarning: Opponent has >1 community support. This card will have no effect.')
                        || card['warn'] == '\nWarning: Opponent has no defence cards to select. This card will have no effect.') {
                        playerCards.showDialogDefence = true
                        playerCards.showOptionDefence = false
                      } else {
                        playerCards.showDialogDefence = false
                        playerCards.showOptionDefence = true
                      }
                      playerCards.moveNotifier = 'Pick 2 defence cards.'+card['warn']
                    } else if (card['requiresOptionField']) {
                      playerCards.showDialogNormal = false
                      playerCards.showOptionDefence = false
                      playerCards.showDialogDefence = false
                      playerCards.showDialogHand = false
                      playerCards.showOptionHand = false
                      playerCards.index = index
                      if (card['warn'] == '') {
                        playerCards.showDialogField = false
                        playerCards.showOptionField = true
                      } else {
                        playerCards.showOptionField = false
                        playerCards.showDialogField = true
                      }
                      playerCards.moveNotifier = 'Pick 1 field card.'+card['warn']
                    } else if (card['requiresDialogHand']) {
                      playerCards.getOpponentHand()
                      playerCards.showDialogNormal = false
                      playerCards.showOptionDefence = false
                      playerCards.showDialogDefence = false
                      playerCards.showOptionField = false
                      playerCards.showDialogField = false
                      playerCards.showDialogHand = true
                      playerCards.showOptionHand = false
                      playerCards.index = index
                      playerCards.moveNotifier = 'Click Confirm when done viewing opponent\'s hand.'
                    } else if (card['requiresOptionHand']) {
                      playerCards.getOpponentHand()
                      playerCards.showDialogNormal = false
                      playerCards.showOptionDefence = false
                      playerCards.showDialogDefence = false
                      playerCards.showOptionField = false
                      playerCards.showDialogField = false
                      playerCards.index = index
                      if (card['warn'] == '') {
                        playerCards.showDialogHand = false
                        playerCards.showOptionHand = true
                      } else {
                        playerCards.vetoShowOpponentHand = true
                        playerCards.showOptionHand = false
                        playerCards.showDialogHand = true
                      }
                      playerCards.moveNotifier = 'Pick a card from opponent\'s hand.'+card['warn']
                    } else {
                      playerCards.showDialogNormal = false // no stray dialogs
                      playerCards.showOptionDefence = false
                      playerCards.showDialogDefence = false
                      playerCards.showOptionField = false
                      playerCards.showDialogField = false
                      playerCards.showDialogHand = false
                      playerCards.showOptionHand = false
                      playerCards.playHand(index)
                      playerCards.index = -1 // just in case
                    }
                    playerCards.showDiscardPlay = false
                    playerCards.showOptionDefence2 = false
                    playerCards.selectionDefence = []
                  }
                }"
                :enable-play="(card['enablePlay'] || playerCards.discardHand) && playerCards.canClickEndTurn"
                :rename-play="playerCards.discardHand ? 'Discard' : 'Play'"
                class="handcard"
    />
  </div>

</template>

<style scoped>

.hand-component-div {
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
}

.handcard{
  position: relative;
  margin-left: .5%;
  margin-right: .5%;
  height: 80%;
  aspect-ratio: 2/3;
  display: inline-block;
}


</style>