<template>
  <b-container id="app" fluid style="height: 90vh;">
    <div class="bar">
      <div>
        <side-bar/>
      </div>
      <div>
        <task-bar/>
      </div>
    </div>
    <div class="main">
      <router-view :key="$route.query?.parent"/>
    </div>
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
