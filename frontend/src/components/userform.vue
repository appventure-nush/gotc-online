<script lang="ts">

import {defineComponent} from "vue"

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

export default defineComponent({
  data(){
    return{
      userform_status_top_text: "Sign In:" as String,
      result : "waiting for input" as String,
      proposed_username : "" as String,
      curr_user : "" as String,
      activity_pinger_id : 0 as unknown as NodeJS.Timer,
    }
  },
  mounted() {
    window.document.onfocus = this.check_if_signed_in
  },
  computed:{
    userform_butt_disabled: function () {
      return this.curr_user !== ""
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
          login_session_key : localStorage.getItem("LoginSessionKey")
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
              this.curr_user = json_response["confirmed_username"]
              localStorage.setItem("LoginSessionKey",json_response["login_session_key"])
              this.refreshText(json_response)
              this.activity_pinger_id = setInterval(this.activity_ping, 20_000)
              //emit a sign in event with current user's username in detail param
              //emitted on document for ease of listening
              window.document.dispatchEvent(new CustomEvent("SignInEvent", {detail:this.curr_user}))
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
          username : this.curr_user,
          login_session_key: localStorage.getItem("LoginSessionKey"),
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
      if(this.curr_user !== "" && window.document.hasFocus()) {
        this.result = "pinging for activity..."
        // send a post request to the calculate part of the backend
        // body of post request is a json
        // first 3 parts of json are just fluff, the actual thing that matters now is the value : value part
        fetch(`${BACKEND_URL}/user_activity_ping`, {
          method: "POST",
          body: JSON.stringify({
            username: this.curr_user,
            login_session_key: localStorage.getItem("LoginSessionKey"),
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
        if(this.curr_user !== "") {
          this.result = "pinging for activity..."
          // send a post request to the calculate part of the backend
          // body of post request is a json
          // first 3 parts of json are just fluff, the actual thing that matters now is the value : value part
          fetch(`${BACKEND_URL}/activity_status_request`, {
            method: "POST",
            body: JSON.stringify({
              username: this.curr_user,
              login_session_key: localStorage.getItem("LoginSessionKey"),
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
      this.curr_user = ""
      this.userform_status_top_text = "Sign In:"
      this.result = json_response_text
      //emit sign out event to notify listeners of a sign out
      //emitted on document for ease of listening
      window.document.dispatchEvent(new CustomEvent("SignOutEvent"))
    },

    refreshText(json_response : any){
      if (json_response["login_success"]) this.userform_status_top_text = json_response["text"]
      this.result = json_response["text"]
    }

  }
})

</script>

<template>
  <p style="border: white; border-width: 5px" id = "userform_status_top">{{ userform_status_top_text }}</p>
  <input type="text" id = "username_textin" v-model.lazy="proposed_username" placeholder="enter username">&nbsp;
  <button type="submit" id = "userform_butt" :disabled="userform_butt_disabled" @click="signin_submit">sign in</button> <br>
  <button type="submit" id = "signout_butt" :disabled="!userform_butt_disabled" @click="signout_submit">sign out</button>
  <p style="border: white; border-width: 5px" id = "userform_status_bottom">{{ result }}</p>
</template>

<style scoped>
  @import "../style.css";
</style>