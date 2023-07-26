<template>
  <b-container class="m-0 p-0">
    <b-button @click="toShow = true" variant="success">
      {{ retVal }}
    </b-button>
    <b-modal
      v-model="toShow"
      button-size="sm"
      hide-header
      @ok="makeEmit"
      ok-title="Выбрать"
      ok-variant="danger"
      cancel-title="Выйти"
      :ok-disabled="!isChanged"
    >
      <b-container class="mw-100 m-0">
        <b-row>
          <b-col>
            <n-table2
              :http-model="httpModel"
              no-actions
              selectable
              select-mode="single"
              :default-row-selected="currentId"
              @update:fk="OnUpdateFK"
            />
          </b-col>
        </b-row>
      </b-container>
    </b-modal>
  </b-container>
</template>

<script>
export default {
  name: 'NLinkField',
  props: {
    httpModel: {type: String, required: true},
    show: {type: Boolean, default: false},
    startValue: {default: ''},
    startId: {type: Number, default: null},
    bindKey: {type: String, default: 'name'},
    bindField: {type: String, required: true}
  },
  computed: {
    retVal() {
      return (this.value ?? this.currentValue) || "Установите связь";
    },
    isChanged() {
      return this.startId != this.currentId;
    }
  },
  data() {
    return {
      toShow: false,
      currentValue: null,
      currentId: null,
    };
  },
  methods: {
    makeEmit() {
      this.$emit("update:fk", {currentId: this.currentId, bindField: this.bindField});
    },
    OnUpdateFK(item) {
      this.currentId = item[0].id;
      this.currentValue = item[0][this.bindKey];
    },
  },
  mounted() {
    this.currentId = this.startId;
    this.currentValue = this.startValue;
  },
}
</script>
