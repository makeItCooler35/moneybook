<template>
  <b-container class="m-0 p-0">
    <b-button
      @click="toShow = true"
      variant="success"
      class="link-button"
    >
      <b-row>
        <b-col cols="2" />
        <b-col>
          {{ title }}
        </b-col>
        <b-col cols="2">
          <b-button @click.stop="OnClear">
            x
          </b-button>
        </b-col>
      </b-row>
    </b-button>
    <b-modal
      v-model="toShow"
      size="lg"
      @ok="OnEmit"
      @cancel="OnHide"
      ok-title="Выбрать"
      ok-variant="danger"
      cancel-title="Выйти"
      :ok-disabled="!isChanged"
    >
      <b-container class="w-100 h-100 m-0">
        <b-row>
          <b-col>
            <n-table2
              :http-model="httpModel"
              :default-id-selected="currentId"
              select-mode="single"
              no-actions
              :no-select-folder="noSelectFolder"
              no-move
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
    value: {type: Number, default: null},
    text: {default: ''},
    bindKey: {type: String, default: 'name'},
    noSelectFolder: {type: Boolean, default: false}
  },
  computed: {
    title() {
      return this.currentText || "Установите связь";
    },
    isChanged() {
      return this.value != this.currentId;
    }
  },
  data() {
    return {
      toShow: false,
      currentId: this.value,
      currentText: this.text,
    };
  },
  methods: {
    OnEmit() {
      this.$emit('input', {id: this.currentId, value: this.currentText});
    },
    OnHide() {
      this.currentId = this.value;
      this.currentText = this.text;
    },
    OnUpdateFK(item) {
      this.currentId = item.id;
      this.currentText = item[this.bindKey];
    },
    OnClear() {
      this.currentId = null;
      this.currentText = '';

      this.OnEmit();
    }
  },
  watch: {
    value(newVal) {
      this.currentId = newVal;

      if(newVal == null) {
        this.currentText = '';
      }
    }
  }
}
</script>
