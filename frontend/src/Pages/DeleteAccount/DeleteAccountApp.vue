<script lang="ts">
import {defineComponent} from 'vue'
import {userSignInStore} from "../../components/UserSignInStore";
import {playerCardsStore} from "../GameArea/components/PlayerCardsStore";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

export default defineComponent({
  name: "DeleteAccountApp",
  computed: {
    userSignInStore() {
      return userSignInStore
    },
  },
  data(){
    return{
      deleting : true as boolean,
      proposed_password : "" as string,
      proposed_password2 : "" as string,

      response_recieved : false as boolean,
      result_text : "" as string,
      wrong_password : false as boolean,
      successful : false as boolean,
    }
  },
  methods:{
    deleteacc_submit(_event : Event){
      this.deleting = false
      fetch(`${BACKEND_URL}/delete_account`, {
        method: "POST",
        body: JSON.stringify({
          username : userSignInStore.username,
          password : this.proposed_password,
          login_session_key: userSignInStore.login_session_key(),
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
          if(json_response["account_deletion_success"] === true) {
            // sign out routine (inline this time)
            clearInterval(userSignInStore.activity_pinger_id)
            userSignInStore.username = ""
            // reset the PlayerCardsStore
            playerCardsStore.resetStore()
          }
          this.result_text = json_response["text"]
          this.successful = json_response["account_deletion_success"]
          this.wrong_password = json_response["wrong_password"]
        })
        .finally(()=>{
          this.response_recieved = true
          this.proposed_password = ""
          this.proposed_password2 = ""
        })
        .catch(error => {
          this.result_text = "An error occurred when deleting your account."
          console.log(error.toString())
        });
    }
  },
})
</script>

<template>
  <h1>GOTC<br>Online</h1>
  <div v-if="!deleting" class="form">
    <p>{{result_text}}</p>
    <button v-if="wrong_password && response_recieved" @click="()=>{deleting=true; successful=false; response_recieved=false}">Back to Account Deletion</button>
    <router-link v-if="response_recieved" to="/" class="mainpage-link">Back to Homepage</router-link>
  </div>
  <div v-else-if="!userSignInStore.isSignedIn" class="form">
    <h2 class="userform-status top" id="userform_status_top">You are not signed in.</h2>
    <p>Please sign into the account you wish to delete before proceeding.</p>
    <router-link to="/" class="mainpage-link">Back to Homepage</router-link>
  </div>
  <div v-else class="form">
    <h2 class="userform-status top" id="userform_status_top">Create a new profile</h2>
    <p style="margin-bottom: 0">Continuing will delete user <i>{{userSignInStore.username}}</i>.<br>Please enter your password 2 times to continue.</p>
    <p>Password</p>
    <input type="password" v-model.lazy="proposed_password" placeholder="enter password">
    <p>Confirm Password</p>
    <input type="password" v-model.lazy="proposed_password2" placeholder="enter password again">
    <p v-if="proposed_password!==proposed_password2" style="background-color: red; color: white">Passwords are not the same.</p>
    <button type="submit" id="userform_butt" @click="deleteacc_submit" :disabled="proposed_password!==proposed_password2" class="delete-confirmation">I wish to DELETE my account PERMANENTLY</button>
    <router-link to="/" class="mainpage-link">Cancel</router-link>
  </div>

</template>

<style>
body{
  background-color: #588B8B;
}
</style>
<style scoped>

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

.form{
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

h2 {
  text-align: center;
  margin: .5em auto ;
}
p{
  margin: 1em 0;
  font-size: 1.1em;
}

button{
  position: relative;
  margin: 1em 0;
  font-size: 1em;
  background-color: black;
  color: white;
  height: 2.5em;
  padding: 0;
}
button:hover{
  font-style: italic;
  border-color: #f28f3b;
  transition: .2s;
}

.delete-confirmation{
  background-color: #000000;
  color: red;
  font-weight: 600;
}

input{
  font-size: 1em;
}

.mainpage-link{
  font-size: 1em;
  text-align: center;
  line-height: 2;
  background-color: black;
  color: white;
  height: 2.5em;
  padding: 0;
  align-content: center;
  border-radius: .5em;
  border: transparent 2px solid;
}
.mainpage-link:hover{
  font-style: italic;
  border: #f28f3b 2px solid;
  transition: .2s;
}

</style>