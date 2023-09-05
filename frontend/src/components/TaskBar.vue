<template>
  <b-container fluid>
    <b-row>
      <b-col class="text-right">
        <b-dropdown right>
          <template #button-content>
            <b-img :src="require('@/assets/icons/bell.svg')"/>
          </template>
          <b-dropdown-item v-for="(job, key) in jobs" :key="key">
            <span v-if="job.status == 'SUCCESS'">
              &#10004;&#65039;
            </span>
            <b-spinner v-else small/>
            {{ job.title }}
          </b-dropdown-item>
        </b-dropdown>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  computed: {
    jobs() {
      return this.$store.getters.getJobs;
    }
  },
  mounted() {
    this.$nextTick(() => {
      // нужно проверить незавершенные работы
      const pendingJobs = Object.entries(this.jobs).filter(x => x[1].timer).map(x => x[0]);
      for(const jobId of pendingJobs) {
        this.$http.get("jobs", {params: {jobId}});
      }
    });
  }
}
</script>