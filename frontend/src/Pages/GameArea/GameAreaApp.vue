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
  created() {
    this.$watch(
        () => this.$route.params,
        (_to, _prev) => {
          playerCardsStore.uuid = this.$route.params.gameid as string
          opponentFieldStore.uuid = this.$route.params.gameid as string
          // todo use game_status backend call which returns if you are playing, spectating or the game does not exist

          fetch(`${BACKEND_URL}/get_opponent_state`, {
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

          // crisis isn't showing up so we fix it
          playerCardsStore.getCrisis()
        }
    )
    playerCardsStore.uuid = this.$route.params.gameid as string
    opponentFieldStore.uuid = this.$route.params.gameid as string

    fetch(`${BACKEND_URL}/get_opponent_state`, {
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

    // crisis isn't showing up so we fix it
    playerCardsStore.getCrisis()
  },
})
</script>

<!--
  This GameApp App/Page is the page that will be shown when going to [url]/gamearea as specified in the vue router in main.ts
-->

<template>

  <div class="gamearea">

    <!-- todo: display usernames to indicate who is who -->
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
  background-color: maroon;

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