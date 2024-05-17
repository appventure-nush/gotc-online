<script lang="ts">

import {defineComponent} from "vue"
import {userSignInStore} from "./UserSignInStore";
import {playerCardsStore} from "../Pages/GameArea/components/PlayerCardsStore";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

// NOTE: Use the userStore from this commit onwards
// the SignInEvent and SignOutEvents are DEPRECATED

export default defineComponent({
  data(){
    return{
      userform_status_top_text: "Sign In:" as String,
      result : "waiting for input" as String,
      proposed_username : "" as String,
      activity_pinger_id : 0 as unknown as NodeJS.Timer,
      userStore : userSignInStore, // NOTE: USE THE USERSTORE AND NOT THE SIGN IN/OUT EVENTS FROM THIS COMMIT ON
      playerStore : playerCardsStore,
    }
  },
  mounted() {
    window.document.onfocus = this.check_if_signed_in
    if(this.userform_butt_disabled){
      this.result = "Signed In as " + this.userStore.username
    }
  },
  setup(){
  },
  computed:{
    userform_butt_disabled: function () {
      return this.userStore.isSignedIn
    },
  },
  methods:{
    signin_submit(_event : Event){
      if (this.proposed_username === "") {
        // prevent username from being blank string
        // as blank string is used to detect if signed in
        this.result = "Blank usernames are not allowed. Not signed in."
        return
      }
      this.result = "Sending sign in request..."
      fetch(`${BACKEND_URL}/sign_in`, {
        method: "POST",
        body: JSON.stringify({
          proposed_username : this.proposed_username,
          login_session_key : this.userStore.login_session_key()
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
          // this results in a response promise that promises some sort of response
          // will be received from where the post was sent to


          .then((response) => {
            if(!response.ok) return Promise.reject(response)
            else return response.text()
          })
          .then((json_text) => {
            let json_response = JSON.parse(json_text)
            if(json_response["login_success"] === true) {
              // this.curr_user = json_response["confirmed_username"]
              this.userStore.username = json_response["confirmed_username"]
              this.userStore.setLoginSessionKey(json_response["login_session_key"])
              // localStorage.setItem("LoginSessionKey",json_response["login_session_key"])
              // console.log(localStorage.getItem("LoginSessionKey"))
              // console.log(userSignInStore.login_session_key())
              this.refreshText(json_response)
              this.activity_pinger_id = setInterval(this.activity_ping, 20_000)
              // emit a sign in event with current user's username in detail param
              // emitted on document for ease of listening
              // DEPRECATE, USE THE USER STORE
              window.document.dispatchEvent(new CustomEvent("SignInEvent", {detail:this.userStore.username}))
            }
            else {
              this.refreshText(json_response)
            }
          })

          .catch(error => {
            this.result = error.toString()
          });
    },

    signout_submit(_e : Event){
      this.result = "Sending sign out request..."
      fetch(`${BACKEND_URL}/sign_out`, {
        method: "POST",
        body: JSON.stringify({
          username : this.userStore.username,
          login_session_key: this.userStore.login_session_key(),
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
          // this results in a response promise that promises some sort of response
          // will be received from where the post was sent to


          .then((response) => {
            if(!response.ok) return Promise.reject(response)
            else return response.text()
          })
          .then((json_text) => {
            let json_response = JSON.parse(json_text)
            if(json_response["signout_success"] === true) {
              this.signout(json_response["text"])
            }
          })

          .catch(error => {
            this.result = error.toString()
          });
    },

    activity_ping(){
      if(this.userStore.isSignedIn && window.document.hasFocus()) {
        this.result = "pinging for activity..."
        // send a post request to the calculate part of the backend
        // body of post request is a json
        // first 3 parts of json are just fluff, the actual thing that matters now is the value : value part
        fetch(`${BACKEND_URL}/user_activity_ping`, {
          method: "POST",
          body: JSON.stringify({
            username: this.userStore.username,
            login_session_key: this.userStore.login_session_key(),
          }),
          headers: {
            "Content-type": "application/json; charset=UTF-8"
          }
        })
            // this results in a response promise that promises some sort of response
            // will be received from where the post was sent to


            .then((response) => {
              if (!response.ok) return Promise.reject(response)
              else return response.text()
            })
            .then((json_text) => {
              let json_response = JSON.parse(json_text)
              if (json_response["still_active"] === true) {
                this.result = json_response["text"]
              } else {
                this.signout(json_response["text"])
              }
            })

            .catch(error => {
              this.result = error.toString()
            });
      }
    },

    check_if_signed_in(){
      {
        if(this.userStore.isSignedIn) {
          this.result = "pinging for activity..."
          // send a post request to the calculate part of the backend
          // body of post request is a json
          // first 3 parts of json are just fluff, the actual thing that matters now is the value : value part
          fetch(`${BACKEND_URL}/activity_status_request`, {
            method: "POST",
            body: JSON.stringify({
              username: this.userStore.username,
              login_session_key: this.userStore.login_session_key(),
            }),
            headers: {
              "Content-type": "application/json; charset=UTF-8"
            }
          })
              // this results in a response promise that promises some sort of response
              // will be received from where the post was sent to


              .then((response) => {
                if (!response.ok) return Promise.reject(response)
                else return response.text()
              })
              .then((json_text) => {
                let json_response = JSON.parse(json_text)
                if (json_response["still_active"] === true) {
                  this.result = json_response["text"]
                } else {
                  this.signout(json_response["text"])
                }
              })

              .catch(error => {
                this.result = error.toString()
              });
        }
      }
    },

    signout(json_response_text : String){
      clearInterval(this.activity_pinger_id)
      this.userStore.username = ""
      this.userStore.username = ""
      this.userform_status_top_text = "Sign In:"
      this.result = json_response_text
      // reset the PlayerCardsStore
      this.playerStore.resetStore()

      // DEPRECATED: use the UserSignInStore instead!
      // emit sign out event to notify listeners of a sign out
      // emitted on document for ease of listening
      window.document.dispatchEvent(new CustomEvent("SignOutEvent"))
    },

    refreshText(json_response : any){
      if (json_response["login_success"]) this.userform_status_top_text = json_response["text"]
      this.result = json_response["text"]
    },

    async leaving(event: BeforeUnloadEvent) {
      event.preventDefault()
      await fetch(`${BACKEND_URL}/disconnect`, {
        method: "POST",
        body: JSON.stringify({
          username: this.userStore.username,
          login_session_key: localStorage.getItem("LoginSessionKey")
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
          .then((response) => {
            if(!response.ok) return Promise.reject(response)
            else return response.text()
          })
          .then((json_text) => {
            let json_response = JSON.parse(json_text)
            if(json_response["signout_success"] === true) {
              this.signout(json_response["text"])
            }
          })

          .catch(error => {
            this.result = error.toString()
          })
    }
  },
  created() {
    window.addEventListener("beforeunload", this.leaving);
  },
})

</script>

<template>
  <p class="userform-status top" id="userform_status_top">{{ userform_status_top_text }}</p>
  <input class="userform-input" type="text" id = "username_textin" v-model.lazy="proposed_username" placeholder="enter username">
  <button type="submit" id = "userform_butt" :disabled="userform_butt_disabled" @click="signin_submit">sign in</button>
  <button type="submit" id = "signout_butt" :disabled="!userform_butt_disabled" @click="signout_submit">sign out</button>
  <p class="userform-status bottom" id="userform_status_bottom">{{ result }}</p>
</template>

<style scoped>

  .userform-status{
    color: white;
  }

  .top{
    font-size: 1.3em;
    margin: .1em 0;
  }

  .userform-input{
    font-size: 1em;
  }

  button{
    font-size: 1.2em;
    padding: .25em .5em !important;
  }

  .bottom{
    font-size: 1.1em;
    margin: .1em 0;
  }

</style>