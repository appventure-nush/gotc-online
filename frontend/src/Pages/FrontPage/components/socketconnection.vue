<template>
  <p>Connected state (will receive dynamic updates): {{ connected }}</p>
  <p>Number of logged in users: {{ numlogin }}</p>
</template>

<script lang="ts">

import { defineComponent } from "vue"
import { state } from "../../../socket"

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

export default defineComponent({
  computed:{
    connected() {
      return state.connected
    }
  },
  data() {
    return {
      numlogin: undefined as Number
    }
  },
  async mounted() {
    this.numlogin = await fetch(`${BACKEND_URL}/get_number_logged_in`)
        .then((response) => response.json())
        .then((data) => parseInt(data))
  }
})
</script>

<style scoped>

</style>