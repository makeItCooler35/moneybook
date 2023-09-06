<template>
  <b-container id="app" fluid style="height: 90vh;">
    <b-row class="bar">
      <b-col>
        <side-bar/>
      </b-col>
      <b-col>
        <task-bar/>
      </b-col>
    </b-row>
    <b-row class="main">
      <router-view :key="$route.query?.parent"/>
    </b-row>
  </b-container>
</template>

<script>
import SideBar from './components/SideBar.vue';
import TaskBar from './components/TaskBar.vue';
export default {
  name: 'App',
  components:{
    SideBar, TaskBar
  },
}
</script>
