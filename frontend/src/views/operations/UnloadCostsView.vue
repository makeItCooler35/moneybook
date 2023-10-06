<template>
  <b-container class="n-form">
    <b-row>
      <b-form-select v-model="selected" :options="groups" />
    </b-row>
    <b-row>
      <b-col cols="5">
        <label>Дата начала</label>
        <n-date-input v-model="startDate" />
      </b-col>
      <b-col cols="5">
        <label>Дата конца</label>
        <n-date-input v-model="endDate" />
      </b-col>
    </b-row>
    <b-row class="mt-2">
      <b-button
        variant="success"
        @click="Unload"
      >
        Напечатать
      </b-button>
    </b-row>
  </b-container>
</template>

<script>
import NDateInput from '@/components/NDateInput.vue';

export default({
  name: 'UnloadCostsView',
  components: {
    NDateInput
  },
  data() {
    return {
      httpModel: 'book',
      groups: ['Без группировок', 'Группировка по категориям'],
      selected: '',
      startDate: new Date(),
      endDate: new Date(),
    };
  },
  computed: {
    group() {
      return this.groups.indexOf(this.selected);
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.selected = this.groups[0];
    });
  },
  methods: {
    async Unload() {
      await this.$http.post(
        this.httpModel, { 
          _method: "unload_excel",
          title: 'Выгрузка расходов',
          params: {
            group: this.group
          },
        },
        {
          responseType: 'blob',
        }
      );
    }
  }
})
</script>

