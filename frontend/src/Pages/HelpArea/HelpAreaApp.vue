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
</style>