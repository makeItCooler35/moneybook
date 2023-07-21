<template>
  <div id="app">
    <b-container fluid class="mb-2 mt-2">
      <b-row>
        <side-bar/>
      </b-row>
      <b-row>
        <router-view/>
      </b-row>
    </b-container>
  </div>
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
