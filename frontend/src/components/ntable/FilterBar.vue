<template>
  <div style="display: inline-block;">
    <b-button @click="show = !show">
      <b-icon-filter/>
    </b-button>
    <b-sidebar v-model="show" id="sidebar-3" right title="Фильтр" backdrop>
      <slot />
      <template #footer>
        <b-button variant="danger" @click="$emit('filter:clear')">
          Очистить
        </b-button>
        <b-button @click="OnClickApplyFilter">
          Применить
        </b-button>
      </template>
    </b-sidebar>
  </div>
</template>

<script>
export default ({
  props: {
    value: {type: Object, default: () => {}}
  },
  data() {
    return {
      commonFilter: '',
      show: false
    }
  },
  methods: {
    OnClickApplyFilter() {
      this.show = false;
      this.$emit('filter:apply');
    }
  }
})
</script>
