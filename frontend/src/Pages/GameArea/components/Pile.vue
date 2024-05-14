<script lang="ts">
import {defineComponent} from 'vue'
import CardHolder from "./CardHolder.vue";
import {playerCardsStore} from "./PlayerCardsStore";
import {userSignInStore} from "../../../components/UserSignInStore";
import StackedCardHolder from "./StackedCardHolder.vue";

export default defineComponent({
  name: "Pile",
  components: {StackedCardHolder, CardHolder},
  setup(){
    const playerCards = playerCardsStore
    const userStore = userSignInStore
    return { playerCards, userStore }
  },
  beforeMount() {
    // subscribing to the store makes the callback function within the $subscribe function run whenever the userStore updates
    // see more here: https://pinia.vuejs.org/core-concepts/state.html#Subscribing-to-the-state
    // we did not pass {detached:true} so this subssctiption automatically ends when we unmount
    // next time we can also check if a game's going on after checking if the user's signed in
    this.userStore.$subscribe( () => {
      if (this.userStore.isSignedIn) {
        this.playerCards.getDiscard()
        this.playerCards.getCardsLeft()
      }
    })
  },
  data(){
    return{
      drawHover : false as boolean, // variable to store if mouse hovering over draw pile
      discHover : false as boolean, // variable to store if mouse hovering over discard pile
    }
  },
  computed:{
    drawRemainderOpacity : function () {
      // the opacity of the overlay
      return this.drawHover ? 1 : 0
    }
  },
  methods:{
    drawDeck(){
      // draw a card from the deck if signed in
      if(userSignInStore.username !== "") playerCardsStore.drawDeck()
    }
  }
})
</script>

<!--
  This is the component that displays the player's draw and discard piles

  discard pile just shows latest discarded card. details button is active to enlarge top card on discard pile
  discarded cards are read from the discard deck list in the player card store

  draw pile is perpetually showing the back card art with a counter of how many cards are left being read from the player cards store
  draw pile is NOT to be stored locally but fetched from the server to prevent cheating i guess
  see the server's card functions in the backend file
--->

<template>

  <div class="pile-component-div">

    <div class="pile-component-card-wrapper" v-on:mouseover="drawHover=true" v-on:mouseout="drawHover=false">
      <CardHolder card-name="back-black" class="pile-component-card" rename-play="End Turn" :enable-details="false"
                  :play-button-func="playerCards.passTurn"
                  :enable-play="playerCards.canClickEndTurn && !playerCards.discardHand && !playerCards.showOptionHand && !playerCards.showDialogHand"/>
      <!-- todo make end turn more visible -->
      <p v-if="userStore.isSignedIn" class="draw-remainder">{{ playerCards.cardsLeft }} Left</p>
      <p v-else class="draw-remainder sign-in-reminder">Not Signed In</p>
    </div>

    <div class="pile-component-card-wrapper" v-on:mouseover="discHover=true" v-on:mouseout="discHover=false">
      <StackedCardHolder class="pile-component-card discardpile"
                         :cards="playerCards.discardDeck.length > 0 ? playerCards.discardDeck : ['discard-placeholder']"
                         :enable-play="playerCards.showDiscardPlay && playerCards.canClickEndTurn"
                         :play-button-func="(key) => {return () => {
                           playerCards.showDiscardPlay = false
                           playerCards.playHand(playerCards.index, key)
                         }}"
                         :rename-play="'Restore'"/>
    </div>


  </div>

</template>

<style scoped>

.pile-component-div{
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
}

.pile-component-card-wrapper{
  position: relative;
  height: 80%;
  aspect-ratio: 2/3;
  display: inline-block;
}
.pile-component-card-wrapper>.discardpile{
  position: absolute;
  width: 100%;
  height: 100%;
}

.draw-remainder {
  position: absolute;
  height: 20%;
  width: 80%;
  left: 10%;
  text-align: center;
  padding: 0;
  top: 20%;
  display: block;
  opacity: v-bind(drawRemainderOpacity);
  transition: all .2s;
  pointer-events: none;
  background-color: rgba(0,0,0,0.7);
  line-height: 200%;
}
.sign-in-reminder {
  background-color: rgba(178,34,34,0.7) !important;
  font-size: .95vw;
  white-space: nowrap;
}

</style>