<script lang="ts">
import {defineComponent} from 'vue'

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL

export default defineComponent({
  name: "LadderAreaApp",
  data() {
    return {
      display: [] as {}[]
    }
  },
  methods: {
    async getLadder() {
      this.display = await (await fetch(`${BACKEND_URL}/get_ladder`)).json()
    }
  },
  beforeMount() {
    this.getLadder()
  }
})
</script>

<template>
  <div class="container">
    <table class="ladder">
      <caption>
        This leaderboard shows you a list of players and their corresponding statistics.
      </caption>
      <colgroup><col></colgroup>
      <colgroup><col></colgroup>
      <colgroup span="3"></colgroup>
      <colgroup span="3"></colgroup>
      <thead>
      <tr>
        <th colspan="2" scope="colgroup">Opponent found by:</th>
        <th colspan="3" scope="colgroup">Random Opponent</th>
        <th colspan="3" scope="colgroup">Challenge User</th>
      </tr>
      <tr>
        <th scope="col">Index</th>
        <th scope="col">Username</th>
        <th scope="col">Wins</th>
        <th scope="col">Draws</th>
        <th scope="col">Losses</th>
        <th scope="col">Wins</th>
        <th scope="col">Draws</th>
        <th scope="col">Losses</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(element, index) in display">
        <th scope="row">{{index+1}}</th>
        <td>{{element["username"]}}</td>
        <td>{{element["winsrandom"]}}</td>
        <td>{{element["drawsrandom"]}}</td>
        <td>{{element["lossesrandom"]}}</td>
        <td>{{element["winschallenge"]}}</td>
        <td>{{element["drawschallenge"]}}</td>
        <td>{{element["losseschallenge"]}}</td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.container{
  position: relative;
  width: 100%;
  min-height: 100%;
  background: linear-gradient(rgba(255,255,255,.3), rgba(255,255,255,.3)), url("/src/assets/mainpage_bg.png");
  overflow: hidden;
  background-size: cover;
  background-blend-mode: lighten;
}
.ladder {
  margin: auto;
}
caption {
  caption-side: top;
}
td, th {
  padding: 3px 5px;
  text-align: center;
  border: 1px solid;
}
.rules{
  background: rgba(255,255,255,.9);
  border: 1px solid rgba(255,255,255,.6);
  max-width: 60%;
  padding: 20px;
  margin: 20px auto;
  backdrop-filter: blur(4px);
}
@media (prefers-color-scheme: dark) {
  .rules{
    color: black;
  }
}
</style>