<script setup lang="ts">

</script>

<template>
  <div class="btn-group">
    <button>HELP</button>
    <button>REPLAY</button>
    <button>LADDER</button>
    <button class="play_b">PLAY</button>
  </div>
</template>

<style scoped>

.btn-group button {
  border-radius: 0;
}

.btn-group button:not(:last-child, :first-child) {
  border-radius: 0;
}

.btn-group button:not(:last-child,) {
  border-right: none; /* Prevent double borders */
}

.btn-group button:first-child {
  border-top-left-radius: 10pt;
  border-bottom-left-radius: 10pt;
}

.btn-group button:last-child {
  border-top-right-radius: 10pt;
  border-bottom-right-radius: 10pt;
}

/* Clear floats (clearfix hack) */
.btn-group:after {
  content: "";
  clear: both;
  display: table;
}

.play_b {
  border-color: #9ed813ff !important;

  transition: border-color 0.3s !important;
}

.play_b:hover{
  border-color: aquamarine !important;
}
</style>