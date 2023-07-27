<template>
  <b-modal
    v-model="show"
    button-size="sm"
    hide-header
    centered
    @ok="doDelete"
    @hidden="doHide"
    ok-title="Удалить"
    ok-variant="danger"
    cancel-title="Отменить"
  >
    <b-container>
      <b-row>
        <b-col>
          Вы уверены?
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
    httpModel: {type: String, required: true}
  },
  data() {
    return {
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
    }
  },
  methods: {
    async doDelete() {
      let res = null;
      try {
        res = await this.$http.delete(this.httpModel + `/${this['id']}`);
      }
      catch(err) {
        res = err.response.statusText;
      }
      this.$emit('close', res);
    },
    doHide() {
      this.show = false;
      this.$emit('close');
    }
  },
}
</script>