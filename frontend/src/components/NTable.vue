<template>
  <div class="overflow-auto">
    <h1 class="mt-3 text-center">
      {{ title }}
    </h1>
    <b-table
      id="my-table"
      :fields="fields"
      :items="items"
      :per-page="perPage"
      :current-page="currentPage"
      small
    >
      <template #cell(actions)="row">
        <b-button class="mx-2" size="sm" variant="warning" @click="OnClickUpdate(row)">
          <b-img :src="require('@/assets/icons/pencil-square.svg')"/>
        </b-button>
        <b-button size="sm" variant="danger" @click="OnClickDelete(row)">
          <b-img :src="require('@/assets/icons/trash.svg')"/>
        </b-button>
      </template>
    </b-table>
    <b-pagination
      v-model="currentPage"
      :total-rows="totalRows"
      :per-page="perPage"
      aria-controls="my-table"
    />
    <delete-dialog
      :value="showDeleteDialog"
      :http-model="httpModel"
      :id="currentId"
      @close="OnDeleteClose"
    />
    <upd-ins-dialog
      :value="showUpdInsDialog"
      :http-model="httpModel"
      :id="currentId"
      :fields="fields"
      :current-row="currentRow"
      @close="OnUpdInsClose"
    />
  </div>
</template>

<script>
import DeleteDialog from './ntable/DeleteDialog.vue';
import UpdInsDialog from './ntable/UpdInsDialog.vue';
  export default {
  components: { DeleteDialog, UpdInsDialog },
    props: {
      httpModel: {type: String, required: true},
    },
    data() {
      return {
        showDeleteDialog: false,
        showUpdInsDialog: false,
        currentRow: {},
        currentId: null,
        title: '',
        perPage: 25,
        currentPage: 1,
        totalRows: 0,
        items: [],
        fields: [],
      }
    },
    created() {
      this.fetchData();
    },
    methods: {
      async fetchData() {
        const res = (await this.$http.get(
        this.httpModel, {
          params: {
            pagination: {
              perPage: this.perPage,
              page: this.currentPage
            }
          }
        })
        ).data;
        this.prepareData(res);
        const selection = (await import(`../selections/${this.httpModel}`)).default;
        this.title = selection.title;
        this.fields = selection.fields.slice(0);
        this.fields.push({
          key: 'actions',
          label: ''
        });
      },
      prepareData(data) {
        this.items = [];
        const rows = data.rows;
        const fields = data.fields;
        for(const row of rows) {
          let item = {};
          for(const num in fields) {
            const field = fields[num];
            item[field] = row[num];
          }
          this.items.push(item);
        }
        this.totalRows = data.pagination.count_rows;
      },
      _initModal(modalVar, row) {
        this[modalVar] = true;
        this.currentRow = row.item;
        this.currentId = row.item.id;
      },
      OnClickUpdate(row) {
        this._initModal('showUpdInsDialog', row);
      },
      OnClickDelete(row) {
        this._initModal('showDeleteDialog', row);
      },
      _destroyModal(modalVar) {
        this[modalVar] = false;
        this.currentRow = {};
        this.currentId = null;
        this.fetchData();
      },
      OnUpdInsClose() {
        this._destroyModal('showUpdInsDialog');
      },
      OnDeleteClose() {
        this._destroyModal('showDeleteDialog');
      }
    },
  }
</script>