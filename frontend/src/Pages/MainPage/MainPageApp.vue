<script lang="ts">

import {defineComponent} from "vue";
import userform from "../../components/userform.vue";
import topbarbuttonbar from "./components/topbarbuttonbar.vue";
import {mainPageStore} from "./MainPageStore";
import {userSignInStore} from "../../components/UserSignInStore";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL;

export default defineComponent({
  components: {
    userform, topbarbuttonbar
  },
  data(){
    return{
      isLandscape : screen.height<=screen.width,

      got_games : false as boolean,
      getting_games_error: false as boolean,
      list_of_games : [] as string[][]
    }
  },
  computed: {
    showSignInDialog() {
      return mainPageStore.signInPrompDisplay
    },
    isMobile() {
      return Math.min(screen.width, screen.height) <= 500
    },
    showWarningBox(){
      return this.isMobile || !this.isLandscape
    }
  },
  mounted() {
    this.checkForOngoingGames()
    userSignInStore.$subscribe(()=>{
      console.log(userSignInStore.username)
      this.checkForOngoingGames()
    })
  },
  methods:{
    checkForOngoingGames(){
      // check if the user has any ongoing games and list them out
      if (userSignInStore.isSignedIn) {
        fetch(`${BACKEND_URL}/get_my_running_games`, {
          method: "POST",
          body: JSON.stringify({
            username: userSignInStore.username,
            login_session_key: userSignInStore.login_session_key()
          }),
          headers: {
            "Content-type": "application/json; charset=UTF-8"
          }
        })
            .then((response) => {
              if (!response.ok) return Promise.reject(response)
              else return response.text()
            })
            .then((json_text) => {
              this.got_games = true
              this.list_of_games = JSON.parse(json_text)["games"] as string[][]
            })

            .catch(_ => {
              this.getting_games_error = true
            });
      } else {
        this.list_of_games = []
        this.got_games = true
      }
    }
  }
})

</script>

<template>
  <div class="all_container">
    <div class="topbar">
      <p class="gotc-online-pseudologo">GOTC<br>ONLINE</p>
      <topbarbuttonbar/>
      <div class="userform-div"><userform/></div>
    </div>

    <div v-if="getting_games_error" class="my-ongoing-games">
      <h3 style="text-align: center;">Error Getting Current Games</h3>
    </div>
    <div v-else-if="!got_games" class="my-ongoing-games">
      <h3 style="text-align: center;">Searching for any ongoing games...</h3>
    </div>
    <div v-else-if="got_games && list_of_games.length==0" class="my-ongoing-games">
      <h3 style="text-align: center;">No Ongoing Games</h3>
    </div>
    <div v-else class="my-ongoing-games">
      <h3 style="margin-bottom: .5em">My Ongoing Games:</h3>
      <router-link v-for="g in list_of_games" :to="'/GameArea/'+g[0]" class="existing-game-link">Against {{g[1]}}<br>Started on {{g[2]}}</router-link>
    </div>

    <div v-if="showWarningBox" class="bottom-reminders">
      <p v-if="!isLandscape">Please rotate your device such that it is in landscape mode.</p><br v-if="!isLandscape">
      <p v-if="isMobile">You seem to be playing on a mobile device. You may need to zoom out on your browser for text to be properly sized.</p>
    </div>
  </div>
</template>

<style scoped>

.userform-div{
  display: v-bind(showSignInDialog);
  top: 10%;
  position: absolute;
  right: 5%;
  flex-direction: column;
  background: #80808080;
  justify-content: center;
  align-items: center;
  padding: 1em;
  row-gap: .5em;
  color: white;
  width: 26ch;
}

.topbar .gotc-online-pseudologo{
  text-align: center;
  color: white;
  font-size: 2.5vh;
  font-weight: 600;
  font-style: italic;
  width: 12vw;
  line-height: 1;
}


.all_container{
  background-image: url("../../assets/mainpage_bg.png");
  background-size: 100vw 100vh;
  height: 100vh;
  width: 100vw;

  font-family: "Exo 2",serif;
}

.topbar{
  height: 8vh;
  background-color: #C8553D;
  top: 0;

  display: flex;
  align-items: center;
  justify-content: space-between;

  padding-left: 10vw;
  padding-right: 10vw;
}

.bottom-reminders{
  position: absolute;
  bottom: 5%;
  right: 5%;
  left: 5%;
  background: #FFD5C2;
  color: black;
  display: flex;
  align-content: center;
  justify-content: center;
  flex-direction: column;
  padding: .5em;
  gap: 1vh;
}
.bottom-reminders > p{
  margin: 0;
  display: flex;
  justify-content: center;
  font-size: 3.5vh;
  line-height: .9;
}

.my-ongoing-games {
  position: absolute;
  top: 10vh;
  left: 5vw;
  width: 20vw;
  background: #588B8B80;
  color: white;
  display: flex;
  align-content: center;
  justify-content: center;
  flex-direction: column;
  padding: .5em;
  gap: 1vh;
  max-height: 60vh;
  overflow-y: auto;
}

.existing-game-link{
  position: relative;
  border: white 3px solid;
  color: white;
  padding: 0 .5em;
  line-height: 1.5em;
  font-size: 1.05em;
  margin: 0;
  text-overflow: ellipsis;
  overflow: clip;
  height: fit-content;
}
.existing-game-link:hover{
  border-color:  black;
  font-style: italic;
}

</style>