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
      selectable
      :select-mode="selectMode"
      @row-selected="onRowSelected"
      ref="mainTable"
    >
      <template #head(selected)>
        <b-button variant="outline-primary" @click="onClickToAllSelect">
          <span
            aria-hidden="true"
            :class="isAllSelected ? `text-primary` : `text-white`"
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
    </b-table>
    <b-pagination
      v-model="currentPage"
      :total-rows="totalRows"
      :per-page="perPage"
      aria-controls="my-table"
    />
    <delete-dialog
      v-model="showDeleteDialog"
      :http-model="httpModel"
      :id="currentId"
      @close="DestroyModal('showDeleteDialog')"
    />
    <upd-ins-dialog
      v-model="showUpdInsDialog"
      :http-model="httpModel"
      :id="currentId"
      :fields="fields"
      :start-row="currentRow"
      @close="DestroyModal('showUpdInsDialog')"
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
        perPage: 25,
        currentPage: 1,
        totalRows: 0,
        items: [],
        fields: [],
        selected: [],
      }
    },
    computed: {
      isAllSelected() {
        return [this.perPage, this.totalRows].indexOf(this.selected.length) > -1;
      }
    },
    async created() {
      await this.fetchData();
      this.autoSelectRow();
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

        let selection = {};
        try {
          selection = (await import(`../selections/${this.httpModel}`)).default;
        }
        catch(err) {
          selection.title = "";
          selection.fields = res.fields.slice(0);
        }

        this.title = selection.title;
        this.fields = selection.fields.slice(0);
        
        if(this.selectable)
        {
          this.fields.unshift({
            key: 'selected',
            label: ''
          });
        }

        if(!this.noActions)
        {
          this.fields.push({
            key: 'actions',
            label: ''
          });
        }
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
      InitModal(modalVar, row = {}) {
        this[modalVar] = true;
        this.currentRow = row.item ?? {};
        this.currentId = this.currentRow.id;
      },
      DestroyModal(modalVar) {
        this[modalVar] = false;
        this.currentRow = {};
        this.currentId = null;
        this.fetchData();
      },
      onRowSelected(items) {
        this.selected = items;
        if(this.defaultRowSelected !== undefined) {
          this.$emit('update:fk', this.selected);
        }
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
      }
    },
  }
</script>