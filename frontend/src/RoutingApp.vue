<script setup lang="ts">

import {playerCardsStore} from "./Pages/GameArea/components/PlayerCardsStore";

// this will set the initial cardsleft to the correct number as specified by the backend
playerCardsStore.resetStore()

</script>

<template>

  <!--
  The main vue component that is mounted in index.html's app div is this RoutingApp vue component.
  As one can see, there is only a single vue element in there called router-view.
  What is displayed by this router view is dictated by the vue-router assigned to this vue application by main.ts

  See main.ts for a more in depth explanation.
  -->

  <router-view/>


</template>

<style >
  @import "style.css";
</style>