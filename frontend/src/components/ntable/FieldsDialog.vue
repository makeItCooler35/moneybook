<template>
  <b-container>
    <b-modal
      v-model="show"
      :title="infoTitle"
      :ok-disabled="buttonDisabled"
      @show="doBeforeShow"
      @ok="doUpdFields"
      ok-title="Запомнить"
      ok-variant="danger"
      cancel-title="Выйти"
    >
      <b-form-group>
        <b-form-checkbox
          v-for="option in selection.fields"
          v-model="selected"
          :key="option.key"
          :value="option.key"
          :state="boxState"
        >
          {{ option.label }}
        </b-form-checkbox>
      </b-form-group>
    </b-modal>
  </b-container>
</template>

<script>
export default {
  props: {
    value: {type: Boolean, default: false},
    httpModel: {type: String, required: true},
    currentFields: {type: Array, default: () => []},
    selection: {type: Object, default: () => {}}
  },

  data() {
    return {
      selected: []
    };
  },

  computed: {
    show: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit('input', val);
      }
    },
    infoTitle() {
      return `${this.selection.title} (выбор полей)`;
    },
    boxState() {
      return this.selected.length ? null: false;
    },
    buttonDisabled() {
      return this.boxState == null ? false : true;
    },
  },

  methods: {
    async doBeforeShow() {
      const fieldKeys = this.selection.fields.map(x => x.key);
      this.selected = [...this.currentFields.filter(x => fieldKeys.includes(x))];
    },
    async doUpdFields() {
      this.$emit('update', this.selected);
      this.show = false;
    },
  },
}
</script>