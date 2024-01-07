<script lang="ts">
import {defineComponent} from "vue";

export default defineComponent( {
  methods: {
    enableshow() {
      document.getElementById("playdialog").showModal()
    },
    disableshow() {
      document.getElementById("playdialog").close()
    }
  }
})

</script>

<template>
  <div class="btn-group">
    <router-link to="/HelpArea" v-slot="{href, route, navigate}" class="nav help">
      <div class="navdiv">HELP</div>
    </router-link>
    <router-link to="/" v-slot="{href, route, navigate}" class="nav replay">
      <div class="navdiv">REPLAY</div>
    </router-link>
    <router-link to="/" v-slot="{href, route, navigate}" class="nav ladder">
      <div class="navdiv">LADDER</div>
    </router-link>
    <!-- <router-link to="/GameArea" v-slot="{href, route, navigate}" class="nav play"> -->
    <a class="nav play" id="play" @click="this.enableshow()"> <!-- since we dont want to use the router immediately -->
      <div class="navdiv">PLAY</div>
      <dialog id="playdialog">
        <form>
          <header style="background-color:#000;color:#fff;">
            <button formmethod="dialog" @click="this.disableshow()" class="close-button topright">&times;</button>
          </header>
          <div class="enclosedialog">
            <div class="center">
              <button class="enclosedialog" @click="">Random Opponent</button>
              <button class="enclosedialog" @click="$router.push('/GameArea')">VS Computer</button>
            </div>
            <div class="center">OR<br></div>
            Send play request to <br>
            <div class="center"><input/><button class="enclosedialog">Send</button></div>
          </div>
        </form>
      </dialog>
    </a>
    <!-- </router-link> -->


  </div>
</template>

<style scoped>

.nav{
  display: inline-block;
  font-size: 20pt;
  border-left: 1px white solid;
  border-right: 1px white solid;
  height: 1.2em;
  width: 5em;
  text-align: center;
}

.navdiv{
  display: inline-block;
  vertical-align: middle;
}

.help{
  color: white;
}
.help:hover{
  color: #31c3ff;
}

.replay{
  color: white;
}
.replay:hover{
  color: #31c3ff;
}

.ladder{
  color: white;
}
.ladder:hover{
  color: #31c3ff;
}

.play{
  color: greenyellow;
}
.play:hover{
  color: mediumspringgreen;
}

.center{
  left: 50%;
}

@media (prefers-color-scheme: dark) {
  dialog[open] {
    color: black;
  }
}

.enclosedialog {
  font-size: 11pt;
}

.close-button {
  border: none;
  width: 25pt;
  height: 25pt;
  //background-color: #ff0000;
}

.topright {
  position: absolute;
  right: 0;
  top: 0
}

dialog[open]::backdrop {
  background: linear-gradient( rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5) );
}

</style>