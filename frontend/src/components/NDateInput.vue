<template>
  <b-form-datepicker
    v-model="userDate"
    :date-format-options="{ year: 'numeric', month: '2-digit', day: '2-digit' }"
    size="sm"
    label-no-date-selected
    reset-button
  />
</template>

<script>

export default({
  name: 'NDateInput',
  props: {
    value: {required: true}
  },
  computed: {
    userDate: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit('input', val);
      }
    }
  },
})
</script>
