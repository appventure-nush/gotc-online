<script lang="ts">
import {defineComponent} from 'vue'
import CardHolder from "./components/CardHolder.vue";
import BigCardHolder from "./components/BigCardHolder.vue";
import PlayerSide from "./components/PlayerSide.vue";
import OpponentSide from "./components/OpponentSide.vue"
import {playerCardsStore} from "./components/PlayerCardsStore"
import {opponentFieldStore} from "./components/OpponentFieldStore";
import {userSignInStore} from "../../components/UserSignInStore";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

export default defineComponent({
  name: "GameAreaApp",
  components: {OpponentSide, PlayerSide, BigCardHolder, CardHolder},
  include:{
    CardHolder,
  },
  beforeMount() {
    // subscribing to the store makes the callback function within the $subscribe function run whenever the userStore updates
    // see more here: https://pinia.vuejs.org/core-concepts/state.html#Subscribing-to-the-state
    // we did not pass {detached:true} so this subscription automatically ends when we unmount
    userSignInStore.$subscribe(() => {
      // call game init again upon login or logout
      playerCardsStore.uuid = this.$route.params.gameid as string
      opponentFieldStore.uuid = this.$route.params.gameid as string
      fetch(`${BACKEND_URL}/game_init`, {
        method: "POST",
        body: JSON.stringify({
          username : userSignInStore.username,
          game_id: this.$route.params.gameid as string,
          login_session_key : userSignInStore.login_session_key()
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
    })
    playerCardsStore.$subscribe( (mutation, state) => { // upon a change in the store
      // update the variables when they are written to
      // please see backend classes.py for explanation of these variables
      fetch(`${BACKEND_URL}/write_storage`, {
        method: "POST",
        body: JSON.stringify({
          username : userSignInStore.username,
          game_id: this.$route.params.gameid as string,
          login_session_key : userSignInStore.login_session_key(),
          storage: {
            showDialogNormal : state.showDialogNormal,
            showDialogDefence : state.showDialogDefence,
            showOptionDefence : state.showOptionDefence,
            selectionDefence : state.selectionDefence,
            showOptionDefence2 : state.showOptionDefence,
            showOptionField : state.showOptionField,
            showDialogField : state.showDialogField,
            showDiscardPlay : state.showDiscardPlay,
            showOptionHand : state.showOptionHand,
            showDialogHand : state.showDialogHand,
            opponentHandTemp : state.opponentHandTemp,
            discardHand : state.discardHand,
            canClickEndTurn: state.canClickEndTurn,
            index : state.index,
            showForfeitButton : state.showForfeitButton,
            lastmove : state.lastmove,
            timeoutID : state.timeoutID,
            intervalID : state.intervalID,
            tickOpponentTimer : state.tickOpponentTimer
            // moveNotifier: state.moveNotifier, movenotifier is now saved in backend
            // vetoShowOpponentHand: state.vetoShowOpponentHand, needn't be saved
          }
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
    }, {deep:true}) // be recursive for lists
  },
  beforeRouteLeave() {
    // pretend this is a complete disconnect
    window.clearTimeout(playerCardsStore.timeoutID)
    window.clearInterval(playerCardsStore.intervalID)
    window.clearInterval(playerCardsStore.tickOpponentTimer)
    fetch(`${BACKEND_URL}/opponent_handle_timer`, {
      method: "POST",
      body: JSON.stringify({
        username: userSignInStore.username,
        request_username: userSignInStore.username,
        game_id: playerCardsStore.uuid,
        login_session_key: userSignInStore.login_session_key(),
        delta: (Date.now() - playerCardsStore.lastmove) / 1000
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })
  },
  created() {
    this.$watch(
        () => this.$route.params,
        (_to, _prev) => {
          playerCardsStore.uuid = this.$route.params.gameid as string
          opponentFieldStore.uuid = this.$route.params.gameid as string
          // todo use game_init backend call which returns if you are first, second, spectating or the game does not exist

          fetch(`${BACKEND_URL}/game_init`, {
            method: "POST",
            body: JSON.stringify({
              username : userSignInStore.username,
              game_id: this.$route.params.gameid as string,
              login_session_key : userSignInStore.login_session_key()
            }),
            headers: {
              "Content-type": "application/json; charset=UTF-8"
            }
          })
        }
    )
    playerCardsStore.uuid = this.$route.params.gameid as string
    opponentFieldStore.uuid = this.$route.params.gameid as string

    fetch(`${BACKEND_URL}/game_init`, {
      method: "POST",
      body: JSON.stringify({
        username : userSignInStore.username,
        game_id: this.$route.params.gameid as string,
        login_session_key : userSignInStore.login_session_key()
      }),
      headers: {
        "Content-type": "application/json; charset=UTF-8"
      }
    })
  },
})
</script>

<!--
  This GameApp App/Page is the page that will be shown when going to [url]/gamearea as specified in the vue router in main.ts
-->

<template>

  <div class="gamearea">

    <OpponentSide class="opponent-side"/>
    <player-side class="player-side"/>

    <big-card-holder/>

  </div>



</template>

<style scoped>

.gamearea{
  position: absolute;
  height: 100%;
  width: 100%;
  top: 0;
  left: 0;
  background-color: white;
  max-height: 60vw;

  font-family: "Exo 2", serif;
}

.opponent-side{
  position: absolute;
  top: 0;
  left: 0;
  height: 40%;
  width: 100%;
}

.player-side{
  position: absolute;
  bottom: 0;
  left: 0;
  height: 60%;
  width: 100%;
}



</style>