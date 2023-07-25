<template>
    <b-modal
      v-model="show"
      button-size="sm"
      hide-header
      @ok="doUpdIns"
      @hidden="doHide"
      ok-title="Сохранить"
      cancel-title="Отменить"
      :ok-disabled="!isChanged"
    >
      <b-container>
        <b-row v-for="(header, key) of headers" :key="key">
          <b-col>
            {{ header.label }}
          </b-col>
          <b-col>
            <span v-if="header.type==='link'">
            </span>
            <input
              v-else-if="header.type=='datetime'"
              v-model="newRow[header.key]"
              type="datetime-local"  
            >
            <b-input v-else
              v-model="newRow[header.key]"
              :type="header.type || 'text'"
            />
          </b-col>
        </b-row>
      </b-container>
  </b-modal>
</template>

<script>
export default {
  props: {
    value: {type: Boolean, default: false},
    id: {required: true},
    httpModel: {type: String, required: true},
    fields: {type: Array, required: true},
    currentRow: {type: Object, require: true}
  },
  data() {
    return {
      show: false,
      newRow: {},
    };
  },
  computed: {
    headers() {
      return this.fields.filter(field => field.key != 'actions');
    },
    isChanged() {
      const exch = Object.values(this.newRow).filter(x => !Object.values(this.currentRow).includes(x));
      return exch.length;
    },
  },
  methods: {
    async doUpdIns() {
      let res = "";
      try {
        if(this.id) {
          res = await this.$http.patch(this.httpModel + `/${this.id}`, this.newRow);
        }
      }
      catch(err) {
        res = err;
      }
      this.show = false;
      this.$emit('close', res);
    },
    doHide() {
      this.show = false;
      this.$emit('close');
    }
  },
  watch: {
    value(newVal) {
      this.show = newVal;
    },
    currentRow: {
      deep: true,
      handler(newVal) {
        this.newRow = Object.assign({}, newVal);
      }
    }
  }
}
</script>