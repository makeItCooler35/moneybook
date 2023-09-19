<template>
  <b-container>
    <b-modal
      v-model="show"
      @show="OnBeforeShow"
      @ok="doDelete"
      @hidden="doHide"
      ok-title="Удалить"
      ok-variant="danger"
      cancel-title="Отменить"
    >
      <b-container>
        <b-row>
          <b-col>
            Вы действительно хотите удалить {{ maxRecords }} записей.
          </b-col>
        </b-row>
      </b-container>
    </b-modal>
    <b-modal
      v-model="showProgress"
      hide-footer
    >
      <div class="text-center">
        <h1>Идет удаление {{ maxRecords }} записей</h1>
        <b-spinner />
      </div>
    </b-modal>
  </b-container>
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
      showProgress: false,
      maxRecords: 0,
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
      this.showProgress = true;

      if(Array.isArray(this.id)) { // массив
        await this.$http.delete(this.httpModel, {
          params: {
            id: JSON.stringify(this.id)
          }
        });
      } else {  // одиночная запись
        await this.$http.delete(this.httpModel + `/${this.id}`);
      }

      this.showProgress = false;
      this.$emit('close', res);
    },
    doHide() {
      this.show = false;
      this.$emit('close');
    },
    OnBeforeShow() {
      this.maxRecords = !Array.isArray(this.id) ? 1 : this.id.length;
    }
  },
}
</script>