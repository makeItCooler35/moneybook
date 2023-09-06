<template>
  <b-container fluid>
    <b-row>
      <b-col class="text-right">
        <b-dropdown right class="my-class">
          <template #button-content>
            <b-img v-if="!Boolean(pendingJobs.length)" :src="require('@/assets/icons/bell.svg')"/>
            <b-spinner v-else small/>
          </template>
          <b-dropdown-item v-for="(job, key) in jobs" :key="key">
            <span v-if="job.timer == null">
              &#10004;&#65039;
            </span>
            <b-spinner v-else small/>
            {{ job.startTime }} {{ job.title }}
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
    },
    pendingJobs() {
      return this.jobs.filter(x => x.timer);
    }
  },
  mounted() {
    this.$nextTick(() => {
      // нужно проверить незавершенные работы
      for(const job of this.pendingJobs) {
        this.$http.get("jobs", {params: {jobId: job.jobId}});
      }
    });
  }
}
</script>