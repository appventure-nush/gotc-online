<script lang="ts">
import {defineComponent} from 'vue'

export default defineComponent({
  name: "HelpAreaApp"
})
</script>

<template>
  <div class="container">
    <div class="rules">
      <h2>GOTC-online</h2>
      <hr style="border-top: 1px solid rgb(204, 204, 204);">
      <h3>About GOTC-online</h3>
      "Guardians of the City II" (GOTC) is a Total Defence strategy card game designed to help youths develop a deeper understanding of Singapore's security threats and the part we play in keeping Singapore safe and secure.<br>
      The card game presents different security threats as crises and illustrates how the six pillars of Total Defence can be applied to respond to and recover from the crises.<br>
      More information is available at <a href="https://www.mindef.gov.sg/oms/imindef/mindef_websites/topics/totaldefence/resources-guardians-of-the-city.html">https://www.mindef.gov.sg/oms/imindef/mindef_websites/topics/totaldefence/resources-guardians-of-the-city.html</a>.<br><br>
      GOTC-online is an online version of GOTC, allowing for online play with friends and saving of replays.
      <hr style="border-top: 1px solid rgb(204, 204, 204);">
      <h3>How to play</h3>
      The objective is to remove your Crisis card, by displaying the required defences shown on the card.<br>
      Each player picks 1 random Crisis card. If both players have the same Crisis card, shuffle and repick again.<br>
      The first player will draw 4 cards, while the other player will draw 5 cards.<br><br>
      During each turn, the player will draw 1 card from the Draw Pile and may play 1 card from their hand.<br>
      Read the text from the card and follow the instructions on the card accordingly. Some cards may have additional effects activated only when you have enough Community Support, or your opponent does not have enough Community Support.<br>
      At the end of each turn, players can only hold a maximum of 7 cards in their hand. If you have more than 7 cards at the end of your turn, you must discard additional cards until you have 7 cards.<br><br>
      You win when you display all the required defences on your Crisis card.<br>
      If no one has won when the timer has run out or a player has run out of cards to draw, players will continue playing in order until the turn goes back to the first player. The first player does not play again, because the game ends.<br>
      Then, the player that displayed the most required defence cards wins, not counting duplicates.<br>
    </div>
  </div>
</template>

<style scoped>
.container{
  position: relative;
  width: 100%;
  min-height: 100%;
  background:  linear-gradient(rgba(255,255,255,.3), rgba(255,255,255,.3)), url("/src/assets/mainpage_bg.png");
  overflow: hidden;
  background-size: cover;
  background-blend-mode: lighten;
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