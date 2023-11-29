<script lang="ts">
import {defineComponent} from 'vue'
import Userform from "../../../components/userform.vue";

export default defineComponent({
  name: "UtilBar",
  components:{Userform}
})
</script>

<template>
  <div class="utilbar-component-div" >
    <div class="userform-temp">
      <userform />
      <router-link to="/MainPage" v-slot="{href, route, navigate}" class="back-temp">
        Back to MainPage
      </router-link>
    </div>

  </div>
</template>

<style scoped>

.utilbar-component-div{
  display: inline-flex;
  align-items: center;
  justify-content: space-evenly;
}

.utilbar-component-div>.userform-temp{
  border: green 2px solid;
  display: inline-flex;
  height: 85%;
  width: 75%;
  justify-content: space-evenly;
  align-items: center;
}

:deep(button){
  height: 80%;
  padding-top: .5%;
  padding-bottom: .5%;
}

.back-temp{
  position: relative;
  border: steelblue 2px solid;
  color: #03145b;
  padding: .3% 1%;
}

</style>