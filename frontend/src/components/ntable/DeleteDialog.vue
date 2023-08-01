<template>
  <b-container>
    <b-modal
      v-model="show"
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
    <b-modal
      v-model="showProgress"
      centered
      hide-footer
    >
      <span>Идет удаление {{ maxProgress }} записей</span>
      <b-progress :value="currentProgress" :max="maxProgress" show-progress animated/>
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
      maxProgress: 0,
      currentProgress: 0,
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

      let listToDelete = this.id;
      if(!Array.isArray(this.id))
          listToDelete = [this.id];

      this.maxProgress = listToDelete.length;
      for(let item of listToDelete) {
        await this.$http.delete(this.httpModel + `/${item}`);
        this.currentProgress += 1;
      }
      this.currentProgress = 0;
      this.showProgress = false;
      this.$emit('close', res);
    },
    doHide() {
      this.show = false;
      this.$emit('close');
    }
  },
}
</script>