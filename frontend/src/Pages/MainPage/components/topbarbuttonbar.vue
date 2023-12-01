<script setup lang="ts">

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
    <router-link to="/GameArea" v-slot="{href, route, navigate}" class="nav play">
      <div class="navdiv">PLAY</div>
    </router-link>




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


</style>