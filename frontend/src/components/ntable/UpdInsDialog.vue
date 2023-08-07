<template>
  <b-modal
    v-model="show"
    centered
    @ok="doUpdIns"
    @hidden="doHide"
    ok-title="Сохранить"
    cancel-title="Отменить"
    cancel-variant="danger"
    :ok-disabled="!isChanged"
  >
    <b-container>
      <b-row v-for="(header, key) of fields" :key="key" class="mb-2">
        <b-col>
          {{ header.label }}
        </b-col>
        <b-col>
          <n-link-field
            v-if="header.type==='link'"
            :id="currentRow[header.bindField]"
            :value="currentRow[header.key]"
            :http-model="header.model"
            :bind-field="header.bindField"
            :bind-key="header.bindKey"
            @input="OnInputFK($event, header)"
          />
          <input
            v-else-if="header.type=='datetime'"
            v-model="currentRow[header.key]"
            type="datetime-local"
            class="w-100"
          >
          <b-input
            v-else
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
      currentRow: {}
    };
  },
  computed: {
    isChanged() {
      const exch = Object.values(this.currentRow).filter(x => !Object.values(this.startRow).includes(x));
      return Boolean(exch.length);
    },
    show: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit('input', val);
      }
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
    OnInputFK(item, header) {
      this.$set(this.currentRow, header.bindField, item.id);
      this.$set(this.currentRow, header.key, item.value);
    }
  },
  watch: {
    startRow: {
      deep: true,
      handler(newVal) {
        this.currentRow = Object.assign({}, newVal);
      }
    }
  },
}
</script>