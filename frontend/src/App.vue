<template>
  <b-container id="app" fluid style="height: 100vh;">
    <b-row>
      <side-bar/>
    </b-row>
    <b-row style="height: 90%;">
      <router-view :key="$route.query?.parent"/>
    </b-row>
  </b-container>
</template>

<script>
import SideBar from './components/SideBar.vue';
export default {
  name: 'App',
  components:{
    SideBar,
  },
}
</script>
