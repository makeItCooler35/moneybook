<template>
  <b-container fluid class="d-flex flex-column">
    <b-row align-h="center">
      <h1>
        {{ title }}
      </h1>
    </b-row>
    <b-row>
      <b-table
        ref="mainTable"
        :fields="fields"
        :items="items"
        :per-page="perPage"
        :busy="isBusy"
        :select-mode="selectMode"
        small
        selectable
        label-sort-desc=""
        label-sort-asc=""
        label-sort-clear=""
        no-local-sorting
        @row-selected="onRowSelected"
        @sort-changed="onSortChanged"
      >
        <template #head(selected)>
          <b-button variant="outline-dark" @click="onClickToAllSelect">
            <span
              aria-hidden="true"
              :class="isAllSelected ? `text-dark` : `text-white`"
            >
              &check;
            </span>
          </b-button>
        </template>
        <template #head(actions)>
          <b-button variant="primary" @click="InitModal('showUpdInsDialog')">
            +
          </b-button>
        </template>
        <template #cell(selected)="{ rowSelected }">
            <span v-if="rowSelected" aria-hidden="true">&check;</span>
            <span v-else aria-hidden="true">&nbsp;</span>
        </template>
        <template #cell(actions)="row">
          <b-button class="mx-2" size="sm" variant="warning" @click="InitModal('showUpdInsDialog', row)">
            <b-img :src="require('@/assets/icons/pencil-square.svg')"/>
          </b-button>
          <b-button size="sm" variant="danger" @click="InitModal('showDeleteDialog', row)">
            <b-img :src="require('@/assets/icons/trash.svg')"/>
          </b-button>
        </template>
        <template #table-busy>
          <div class="text-center text-dark my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </b-row>
    <b-row class="mt-auto text-center border-bottom justify-content-end p-1">
      <b-col xl="4" sm="6" class="d-flex flex-row" align-content="center">
        <b-form-input
          v-model="currentPage"
          type="number"
          min="1"
          :max="totalPages"
          class="text-center"
          :state="stateCurrentPage"
          @change="OnChangeCurrentPage"
          style="width: max-content;"
        />
        <label class="mx-2 my-auto">
          страница из {{ totalPages }}
        </label>
      </b-col>
      <b-col xl="4" sm="6">
        <b-form-select
          v-model="perPage"
          :options="perPageOptions"
          class="text-center"
          @change="OnChangePerPage"
          style="width: max-content;"
        />
        <label class="mx-2 my-auto">
          записей
          ({{ totalRows > this.items.length ? this.items.length : totalRows}} из {{ totalRows }})
        </label>
      </b-col>
    </b-row>
    <delete-dialog
      v-model="showDeleteDialog"
      :http-model="httpModel"
      :id="currentId"
      @close="DestroyModal"
    />
    <upd-ins-dialog
      v-model="showUpdInsDialog"
      :http-model="httpModel"
      :id="currentId"
      :fields="fields"
      :start-row="currentRow"
      @close="DestroyModal"
    />
  </b-container>
</template>

<script>
import DeleteDialog from './ntable/DeleteDialog.vue';
import UpdInsDialog from './ntable/UpdInsDialog.vue';
  export default {
  components: { DeleteDialog, UpdInsDialog },
    props: {
      httpModel: {type: String, required: true},
      noActions: {type: Boolean, default: false},
      selectable: {type: Boolean, default: false},
      selectMode: {type:  String, default: 'multi'},
      defaultRowSelected: {type: [Number, null], default: undefined},
    },
    data() {
      return {
        showDeleteDialog: false,
        showUpdInsDialog: false,
        currentRow: {},
        currentId: null,
        title: '',
        perPage: 10,
        perPageOptions: [10, 25, 50, 100],
        currentPage: 1,
        totalRows: 0,
        totalPages: 1,
        items: [],
        fields: [],
        selected: [],
        sorting: {},
        isBusy: true,
      }
    },
    computed: {
      isAllSelected() {
        return [this.perPage, this.totalRows].indexOf(this.selected.length) > -1;
      },
      stateCurrentPage() {
        if(1 <= this.currentPage && this.currentPage <= this.totalPages)
          return null;
        else 
          return false;
      }
    },
    async created() {
      await this.fetchData();
      this.autoSelectRow();
    },
    methods: {
      async fetchData() {
        let res = null;
        this.isBusy = true;
        try {
          res = (await this.$http.get(
            this.httpModel, {
              params: {
                pagination: {
                  perPage: this.perPage,
                  page: this.currentPage
                },
                sorting: JSON.stringify(this.sorting)
              }
            })
          ).data;
          this.prepareData(res);
        }
        catch(err) {
          console.log(err);
        }

        if(!this.fields.length) {
          let selection = null;
          try {
            selection = (await import(`../selections/${this.httpModel}`)).default;
          }
          catch(err) {
            selection.title = "";
            selection.fields = res && res.fields ? res.fields.slice(0) : {};
          }

          this.title = selection.title;
          this.fields = selection.fields.slice(0);
        }

        if(this.selectable)
        {
          this.fields.unshift({
            key: 'selected',
            label: '',
            sortable: false
          });
        }

        if(!this.noActions)
        {
          this.fields.push({
            key: 'actions',
            label: '',
            sortable: false
          });
        }

        /* делаем по умолчанию все поля сортируемыми, и выравниваем по центру,
          если не указано иное */
        for(const item of this.fields) {
          item.class = item.class ?? 'text-center';
          item.sortable = item.sortable ?? true;
        }

        this.isBusy = false;
      },
      prepareData(data) {
        this.items = [];
        const rows = data.rows;
        const fields = data.fields;
        for(const index in rows) {
          const row = rows[index];
          let item = {};
          for(const num in fields) {
            const field = fields[num];
            item[field] = row[num];
          }
          this.$set(this.items, index, item);
        }
        this.totalRows = data.pagination.count_rows;
        this.totalPages = data.pagination.count_pages;
      },
      InitModal(modalVar, row = {}) {
        this[modalVar] = true;
        this.currentRow = row.item ?? {};
        this.currentId = this.currentRow.id;
      },
      DestroyModal(result) {
        this.currentRow = {};
        this.currentId = null;
        if(result !== undefined)
          this.fetchData();
      },
      onRowSelected(items) {
        this.selected = items;
        if(this.defaultRowSelected !== undefined) {
          this.$emit('update:fk', this.selected);
        }
      },
      onSortChanged(event) {
        this.sorting = {
          sortBy: event.sortBy,
          sortDesc: event.sortDesc
        };
        this.fetchData();
      },
      autoSelectRow() {
        if(this.defaultRowSelected)
        {
          for(let index in this.items) {
            if(this.items[index].id == this.defaultRowSelected) {
              this.$refs.mainTable.selectRow(+index);
              break;
            }
          }
        }
      },
      onClickToAllSelect() {
        if(this.selectMode == 'multi') {
          if(this.isAllSelected) {
            this.$refs.mainTable.clearSelected();
          }
          else {
            this.$refs.mainTable.selectAllRows();
          }
        }
      },
      async OnChangePerPage() {
        await this.fetchData();
        if(this.stateCurrentPage === false)
          this.currentPage = 1;
      },
      OnChangeCurrentPage() {
        if(this.stateCurrentPage == null) {
          this.fetchData();
        }
      }
    },
  }
</script>