<template>
  <b-container>
    <b-row>
      <b-form-select v-model="selected" :options="groups" />
      <b-container fluid class="p-0 mt-3">
        <label>Дата начала</label>
        <b-form-datepicker v-model="startDate" />
        <label>Дата конца</label>
        <b-form-datepicker v-model="endDate" />
      </b-container>
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
export default({
  name: 'UnloadCostsView',
  components: {
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

