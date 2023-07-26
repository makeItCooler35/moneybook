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
        <b-row v-for="(header, key) of headers" :key="key" class="mb-1">
          <b-col>
            {{ header.label }}
          </b-col>
          <b-col>
            <n-link-field
              v-if="header.type==='link'"
              :http-model="header.model"
              :start-value="currentRow[header.key]"
              :start-id="currentRow[header.bindField]"
              :bind-field="header.bindField"
              :bind-key="header.bindKey"
              @update:fk="OnUpdateFK"
            />
            <input
              v-else-if="header.type=='datetime'"
              v-model="currentRow[header.key]"
              type="datetime-local"  
            >
            <b-input v-else
              v-model="currentRow[header.key]"
              :type="header.type || 'text'"
            />
          </b-col>
        </b-row>
      </b-container>
  </b-modal>
</template>

<script>
import NLinkField from '../NLinkField.vue';
export default {
  components: {
    NLinkField
  },
  props: {
    value: {type: Boolean, default: false},
    id: {required: true},
    httpModel: {type: String, required: true},
    fields: {type: Array, required: true},
    startRow: {type: Object, require: true}
  },
  data() {
    return {
      show: false,
      currentRow: {},
    };
  },
  computed: {
    headers() {
      return this.fields.filter(field => field.label || '' != '');
    },
    isChanged() {
      const exch = Object.values(this.currentRow).filter(x => !Object.values(this.startRow).includes(x));
      return Boolean(exch.length);
    },
  },
  methods: {
    async doUpdIns() {
      let res = "";
      try {
        if(this.id) {
          res = await this.$http.patch(this.httpModel + `/${this.id}`, this.currentRow);
        }
        else {
          res = await this.$http.post(this.httpModel, this.currentRow);
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
    },
    OnUpdateFK(item) {
      this.$set(this.currentRow, `${item.bindField}`, item.currentId);
    }
  },
  watch: {
    value(newVal) {
      this.show = newVal;
    },
    startRow: {
      deep: true,
      handler(newVal) {
        this.currentRow = Object.assign({}, newVal);
      }
    }
  },
}
</script>