<script lang="ts">
import {defineComponent} from 'vue'
import {mainPageStore} from "../MainPage/MainPageStore";
import {userSignInStore} from "../../components/UserSignInStore";
import {playerCardsStore} from "../GameArea/components/PlayerCardsStore";
const BACKEND_URL = import.meta.env.VITE_BACKEND_URL


export default defineComponent({
  name: "CreateAccountApp",
  components: {},
  data(){
      return{
        creating : true as boolean,

        proposed_username : "" as string,
        proposed_password : "" as string,
        proposed_password2 : "" as string,

        response_recieved : false as boolean,
        result : "" as String,
        signin_result : "" as String,
        successful : false as boolean,
    }
  },
  methods:{
    createacc_submit(_event : Event){
      this.creating = false
      this.result = "Creating Account..."
      fetch(`${BACKEND_URL}/create_account`, {
        method: "POST",
        body: JSON.stringify({
          proposed_username : this.proposed_username,
          proposed_password : this.proposed_password
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
              if(json_response["account_creation_success"] === true) {
                // might put sign in code here later
                this.result = json_response["text"]
                this.successful = true
                this.signin()
              }
              else {
                this.result = json_response["text"]
                this.signin_result = ""
                this.successful = false
              }
            })
            .catch(error => {
              this.result = error.toString()
            });
    },

    signin(){
      this.signin_result = "Sending sign in request..."
      fetch(`${BACKEND_URL}/sign_in`, {
        method: "POST",
        body: JSON.stringify({
          proposed_username : this.proposed_username,
          proposed_password : this.proposed_password,
          login_session_key : userSignInStore.login_session_key()
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
              userSignInStore.username = json_response["confirmed_username"]
              userSignInStore.setLoginSessionKey(json_response["login_session_key"])
              userSignInStore.activity_pinger_id = setInterval(this.activity_ping, 20_000)
              this.signin_result = json_response["text"]
              mainPageStore.showSignInPrompt = false
            }
            else {
              this.signin_result = json_response["text"]
            }
          })
          .finally(()=>{
              this.response_recieved = true
              //reset this variable for security maybe
              this.proposed_password = ""
              this.proposed_password2 = ""
            }
          )
          .catch(error => {
            this.signin_result = error.toString()
          });
    },

    activity_ping(){
      if(userSignInStore.isSignedIn && window.document.hasFocus()) {
        // send a post request to the calculate part of the backend
        // body of post request is a json
        // first 3 parts of json are just fluff, the actual thing that matters now is the value : value part
        fetch(`${BACKEND_URL}/user_activity_ping`, {
          method: "POST",
          body: JSON.stringify({
            username: userSignInStore.username,
            login_session_key: userSignInStore.login_session_key(),
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
              let json_response = JSON.parse(json_text)
              if (json_response["still_active"] === true) {
                //this.result = json_response["text"]
              } else {
                // sign out routine (inline this time)
                clearInterval(userSignInStore.activity_pinger_id)
                userSignInStore.username = ""
                // reset the PlayerCardsStore
                playerCardsStore.resetStore()
              }
            })

            .catch(_ => {
              //this.result = error.toString()
            });
      }
    },
  }
})
</script>

<template>
  <h1>GOTC<br>Online</h1>
  <div v-if="creating" class="profile-creation">
    <h2 class="userform-status top" id="userform_status_top">Create a new profile</h2>
    <p>Username</p>
    <input type="text" v-model.lazy="proposed_username" placeholder="enter username">
    <p>Password</p>
    <input type="password" v-model.lazy="proposed_password" placeholder="enter password">
    <p>Confirm Password</p>
    <input type="password" v-model.lazy="proposed_password2" placeholder="enter password again">
    <p v-if="proposed_password!==proposed_password2" style="background-color: red; color: white">Passwords are not the same.</p>
    <button type="submit" id="userform_butt" @click="createacc_submit" :disabled="proposed_password!==proposed_password2">Create Profile</button>
    <router-link to="/" class="mainpage-link">Back to Homepage</router-link>
  </div>
  <div v-else  class="profile-creation">
    <p style="font-size: 1.2em">
      {{result}}
    </p>
    <p v-if="successful" style="font-size: 1.1em">
      {{signin_result}}
    </p>
    <button v-if="response_recieved && !successful" @click="()=>{creating=true; successful=false; response_recieved=false}">Back to Account Creation</button>
    <router-link v-if="response_recieved" to="/" class="mainpage-link">Back to Homepage</router-link>
  </div>
</template>

<style>
  body{
    background-color: #588B8B;
  }
</style>
<style scoped>

.profile-creation{
  display: flex;
  flex-direction: column;
  margin: auto;
  width: 40ch;
  max-width: 100vw;
  font-size: 14pt;
  padding: 2em;
  background-color: #C8553D;
  color: black;
}
h1{
  position: absolute;
  top: 1em;
  left: 1.5em;
  font-style: italic;
  margin: 0;
  color: white;
  text-align: center;
  font-size: 3vh;
}
h2{
  text-align: center;
}
p{
  margin: .5em 0;
  font-size: 1.1em;
}
button{
  position: relative;
  margin: 1em 0;
  font-size: 1em;
  background-color: black;
  color: white;
}
button:hover{
  font-style: italic;
  border-color: #f28f3b;
  transition: .2s;
}
.mainpage-link{
  font-size: 1em;
  text-align: center;
  line-height: 2;
  background-color: black;
  color: white;
  padding: .1em .5em;
  border-radius: .5em;
  border: transparent 2px solid;
}
.mainpage-link:hover{
  font-style: italic;
  border: #f28f3b 2px solid;
  transition: .2s;
}
input{
  font-size: 1em;
}
@media (prefers-color-scheme: light) {

}



</style>