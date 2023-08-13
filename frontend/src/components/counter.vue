<script lang="ts">
import { defineComponent} from "vue"

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

export default defineComponent({
  data(){
    return{
      count : 0 as number,
      username : "" as String,
    }
  },
  mounted() {
    document.addEventListener("SignInEvent", this.onSignInEvent)
    document.addEventListener("SignOutEvent", this.onSignOutEvent)
  },
  computed:{
    disable_count: function (){
      return this.username === ""
    }
  },
  methods:{

    advanceCounter(){
      this.count++

      fetch(`${BACKEND_URL}/set_counter`, {
        method: "POST",
        body: JSON.stringify({
          username: this.username,
          value : this.count
        }),
        headers: {
          "Content-type": "application/json; charset=UTF-8"
        }
      })
    },

    async onSignInEvent(SIEvent : { detail: string; }){
      this.username = SIEvent.detail

      this.count =
          await fetch(`${BACKEND_URL}/get_counter`, {
            method: "POST",
            body: JSON.stringify({
              username: this.username
            }),
            headers: {
              "Content-type": "application/json; charset=UTF-8"
            }
          })
              .then((response) => response.json())
              .then((data) => parseInt(data))

    },

    onSignOutEvent(){
      this.username = ""
    }


  }
})
</script>

<template>
  <button v-if="!disable_count" type="button" @click="advanceCounter" :disabled="disable_count">count is {{ count }}</button>
  <button v-if="disable_count" type="button" :disabled="disable_count">Sign in first.</button>
</template>

<style scoped>

</style>