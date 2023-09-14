<template>
  <div>
    <b-button v-b-toggle.sidebar-2>
      <b-img v-if="!Boolean(pendingJobs.length)" :src="require('@/assets/icons/bell.svg')"/>
      <b-spinner v-else small/>
    </b-button>
    <b-sidebar id="sidebar-2" right title="Список работ">
      <b-list-group>
        <b-list-group-item 
          v-for="(job, key) of jobs"
          :key="key"
          class="jobs"
        >
          <div>
            <span v-if="job.timer == null">
              &#10004;&#65039;
            </span>
            <b-spinner v-else small/>
          </div>
          <div>
            {{ job.title }}
            <div class="info">
              {{ job.startTime }}
            </div>
          </div>
          <div>
            <b-button
              variant="info"
              :disabled="!(job.responseType == 'blob' && job.result)"
              :href="job.result"
            >
              <b-img :src="require('@/assets/icons/clip.svg')" />
            </b-button>
            <b-button variant="danger" @click.stop="OnDeleteJob(job.jobId)">
              <b-img :src="require('@/assets/icons/trash.svg')"/>
            </b-button>
          </div>
        </b-list-group-item>
      </b-list-group>
      <template #footer>
        <b-button variant="danger" @click="OnDeleteJob(null)">
          <b-img :src="require('@/assets/icons/trash.svg')" title="Удалить все работы"/>
        </b-button>
      </template>
    </b-sidebar>
  </div>
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
        this.$http.get("jobs", {
          params: {
            jobId: job.jobId
          }
        });
      }
    });
  },
  methods: {
    OnDeleteJob(jobId) {
      this.$store.commit("DELETE_JOB", jobId);
    }
  }
}
</script>