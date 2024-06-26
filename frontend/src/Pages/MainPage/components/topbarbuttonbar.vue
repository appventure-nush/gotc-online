<script lang="ts">
import {defineComponent} from "vue";
import {userSignInStore} from "../../../components/UserSignInStore";
import {mainPageStore} from "../MainPageStore";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

export default defineComponent( {
  data() {
    return {
      userStore : userSignInStore,
      mainPageStore: mainPageStore
    }
  },
  computed:{
    signInPromptButtonText : function(){
      return this.userStore.isSignedIn ? this.userStore.username : "Sign In"
    }
  },
  methods: {
    toggleSignInPrompt(){
      mainPageStore.showSignInPrompt=!mainPageStore.showSignInPrompt
    },
    enableshow() {
      if (this.userStore.isSignedIn) { // logged in
        (document.getElementById("playdialog") as HTMLDialogElement).showModal()
      } else {
        alert("Sign in first.")
      }
    },
    disableshow() {
      (document.getElementById("playdialog") as HTMLDialogElement).close()
    },
    async requestmatch() {
      if ((document.getElementById("input2") as HTMLInputElement).reportValidity()) {
        let x = await fetch(`${BACKEND_URL}/request_match`, {
          method: "POST",
          body: JSON.stringify({
            username: this.userStore.username,
            login_session_key: localStorage.getItem("LoginSessionKey"),
            requested_username: (document.getElementById("input") as HTMLInputElement).value,
            // convert to int on backend
            proposed_time: (document.getElementById("input2") as HTMLInputElement).value
          }),
          headers: {
            "Content-type": "application/json; charset=UTF-8"
          }
        })
            .then((response) => response.json())
        if (x["status"] == "Opponent not logged in") {
          alert("Opponent is not logged in.")
        } else {
          (document.getElementById("playdialog") as HTMLDialogElement).close();
          (document.getElementById("connectingdialog") as HTMLDialogElement).show()
        }
      }
    },
    async randomopponent() {
      let x = await fetch(`${BACKEND_URL}/random_opponent`, {
        method: "POST",
        body: JSON.stringify({
          username: this.userStore.username,
          login_session_key: localStorage.getItem("LoginSessionKey")
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
          .then((response) => response.json())
      if (x["status"] == "Added to queue") {
        (document.getElementById("playdialog") as HTMLDialogElement).close();
        (document.getElementById("connectingdialog") as HTMLDialogElement).show()
      } else {
        this.$router.push("/GameArea/"+x["id"])
      }
    }
  }
})

</script>

<template>
  <div class="btn-group">
    <router-link to="/HelpArea" class="nav help">
      <div class="navdiv">HELP</div>
    </router-link>
    <router-link to="/" class="nav replay">
      <div class="navdiv">REPLAY</div>
    </router-link>
    <router-link to="/LadderArea" class="nav ladder">
      <div class="navdiv">LADDER</div>
    </router-link>
    <!-- <router-link to="/GameArea" v-slot="{href, route, navigate}" class="nav play"> -->
    <a class="nav play" id="play" @click="enableshow()"> <!-- since we dont want to use the router immediately -->
      <div class="navdiv">PLAY</div>
      <dialog id="playdialog" class="playdialog">
        <form>
          <header style="background-color:#000;color:#fff;">
            <button formmethod="dialog" @click="disableshow()" class="close-button topright">X</button>
          </header>
          <div class="enclosedialog">
            <div class="center">
              <button class="enclosedialog" @click="randomopponent()" type='button'>Random Opponent (10min per side)</button>
              <button class="enclosedialog" @click="$router.push('/GameArea/default')">VS Computer (WIP)</button>
            </div>
            <br>
            <div class="center dialogtext">OR<br></div>
            <div class="dialogtext">Send play request to</div>
            <br>
            <div class="center"><input id="input"/><button class="enclosedialog" @click="requestmatch()" type='button'>Send</button></div>
            <div class="dialogtext">Time (1-60min per side):</div>
            <br>
            <!-- the regex allows integers from 1 to 60 as input -->
            <div class="center"><input id="input2" type="number" min="1" max="60" pattern="([1-9]|[1-5]\d|60)" value="10"/></div>
          </div>
        </form>
      </dialog>

    </a>
    <dialog id="connectingdialog" onblur="close()">
      <div class="dialogtext">Finding opponent...<br>You may close this dialog but do not refresh the page</div>
    </dialog>
    <!-- </router-link> -->

  </div>

  <a @click="toggleSignInPrompt" class="sign-in-option">
    <div v-if="userStore.isSignedIn"
         class="signed-in-text">
      Signed In as:<br>
      {{userStore.username}}
    </div>
    <div v-else
         class="signed-out-text">
      Sign In
    </div>
  </a>

</template>

<style scoped>

.nav{
  display: inline-block;
  font-size: 3.5vh;
  border-left: 1px white solid;
  border-right: 1px white solid;
  color: white;
  height: 6vh;
  width: 5em;
  text-align: center;
}

.navdiv{
  display: flex;
  justify-content: center;
  align-items: center;
  height: inherit;
}

.help:hover{
  background: radial-gradient(circle, #C8553D 0%, #C8553D 50%, #F28F3B 100%);
}

.replay:hover{
  background: radial-gradient(circle, #C8553D 0%, #C8553D 50%, #F28F3B 100%);
}

.ladder:hover{
  background: radial-gradient(circle, #C8553D 0%, #C8553D 50%, #F28F3B 100%);
}

.playdialog{
  background-color: #588B8B;
  color: black;
}

.playdialog button{
  background-color: #F28F3B;
  color: black;
}
.playdialog button:hover{
  border-color: #C8553D;
}

.play{
  font-weight: 700;
}
.play:hover{
  background: radial-gradient(circle, #C8553D 0%, #C8553D 50%, #F28F3B 100%);
}

.center{
  left: 50%;
}

@media (prefers-color-scheme: dark) {
  dialog[open] {
    color: black;
  }
  .dialogtext {
    color: white;
  }
}


.enclosedialog {
  font-size: 11pt;
}
.enclosedialog button {
  margin: 0 .5em;
}

.close-button {
  border: none;
  /* width: 25pt; */
  /* height: 25pt; */
  padding: 0;
  font-weight: bold;
  font-size: .9em;
  aspect-ratio: 1;
  height: 1.2em;
}

.topright {
  position: absolute;
  right: 0;
  top: 0
}

dialog[open]::backdrop {
  background: linear-gradient( rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5) );
}

.sign-in-option{
  display: flex;
  font-size: 3.5vh;
  color: white;
  height: 2em;
  width: 10vw;
  text-align: center;
  justify-content: center;
  line-height: 1;
}
.sign-in-option:hover{
  background: radial-gradient(circle, #C8553D 0%, #C8553D 50%, #F28F3B 100%);
}

.sign-in-option .signed-in-text{
  position: relative;top: 0;font-size: .8em;padding: .1em 0;overflow: hidden; text-overflow: ellipsis;
}
.sign-in-option .signed-out-text{
  position: relative;height: inherit; display: flex; justify-content: center; align-items: center
}


</style>