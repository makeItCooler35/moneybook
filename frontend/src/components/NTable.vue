<template>
  <b-container fluid class="d-flex flex-column">
    <b-row align-v="end">
      <b-button
        class="m-1"
        style="max-height: 50%;width: max-content;"
        :disabled="!currentParent"
        title="Подняться по иерархии"
        @click="OnReduceHierarchy"
      >
        &lt;
      </b-button>
      <h1 class="mx-auto">
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
        no-select-on-click
        @sort-changed="OnSortChanged"
      >
        <template #head(selected) v-if="!moveMode">
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
          <b-container v-if="!moveMode" fluid>
            <b-button v-if="!noCreate" class="mx-1" title="Создать" @click="InitModal('showUpdInsDialog')">
              +
            </b-button>
            <b-button v-if="!noCreateFolder" class="mx-1" title="Создать папку">
              <b-img :src="require('@/assets/icons/folder.png')"/>
            </b-button>
            <b-button
              v-if="!noMove && selectable"
              class="mx-1"
              title="Переместить"
              :disabled="!Boolean(selected.length)"
              @click="moveMode = true"
            >
              m
            </b-button>
          </b-container>
          <b-container v-else fluid>
            <b-button class="mx-1" @click="OnClickEmitMove">
              Переместить сюда
            </b-button>
            <b-button variant="danger" @click="moveMode = false">
              Отмена
            </b-button>
          </b-container>
        </template>
        <template #cell(selected)="{item}" v-if="!moveMode">
          <b-button variant="outline-dark" @click="OnClickToSelect(item)">
            <span
              aria-hidden="true"
              :class="selected.indexOf(item.id) > -1 ? `text-dark` : `text-white`"
            >
              &check;
            </span>
          </b-button>
        </template>
        <template #cell()="{item, value, field}">
          <span v-if="item.is_folder">
            <span v-if="!selfFields.indexOf(field.key)">
              <b-img
                style="cursor: pointer;"
                :src="require('@/assets/icons/folder.png')"
                @click="OnClickFolder(item)"
              />
              {{ item?.[folderName] ?? '' }}
            </span>
          </span>
          <span v-else>
            {{ value }}
          </span>
        </template>
        <template #cell(actions)="{item}" v-if="!moveMode">
          <b-button
            v-if="!noUpdate"
            class="mx-1"
            variant="warning"
            @click="InitModal('showUpdInsDialog', item)"
          >
            <b-img :src="require('@/assets/icons/pencil-square.svg')"/>
          </b-button>
          <b-button
            v-if="!noDelete"
            variant="danger"
            @click="InitModal('showDeleteDialog', item)"
          >
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
      noDelete: {type: Boolean, default: false},
      noUpdate: {type: Boolean, default: false},
      noCreate: {type: Boolean, default: false},
      noCreateFolder: {type: Boolean, default: false},
      noMove: {type: Boolean, default: false},
      selectable: {type: Boolean, default: false},
      selectMode: {type:  String, default: 'multi'},
      noSelectFolder: {type: Boolean, default: false},
      defaultIdSelected: {type: [Number, null], default: undefined},
      isModal: {type: Boolean, default: true}
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
        selfFields: [],
        folderName: null,
        selected: [],
        sorting: {},
        isBusy: true,
        firstMounted: true,
        currentParent: this.isModal ? 0 : this.$route.query?.parent,
        moveMode: false,
      }
    },
    computed: {
      isAllSelected() {
        return [this.perPage, this.totalRows].indexOf(this.selected.length) > -1;
      },
      stateCurrentPage() {
        if(1 <= this.currentPage && this.currentPage <= this.totalPages) {
          return null;
        } else { 
          return false;
        }
      },
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
                sorting: JSON.stringify(this.sorting),
                startId: this.firstMounted ? this.defaultIdSelected : 0,
                parent: this.currentParent
              }
            })
          ).data;
          this.items = [];
          this.items = this.prepareData(res);

          this.totalRows = res.pagination.count_rows;
          this.totalPages = res.pagination.count_pages;
          if(this.firstMounted) {
            this.currentPage = res.pagination.page;
          }
          this.firstMounted = false;
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
            selection.folderName = null;
          }

          this.title = selection.title;
          this.folderName = selection.folderName ?? null;
          this.fields = selection.fields.slice(0);
          this.selfFields = this.fields.map(x => x.key);
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
        let arr = [];
        const rows = data.rows;
        const fields = data.fields;
        for(const index in rows) {
          const row = rows[index];
          let item = {};
          for(const num in fields) {
            const field = fields[num];
            item[field] = row[num];
          }
          arr.push(item);
        }
        return arr;
      },
      InitModal(modalVar, item = {}) {
        this[modalVar] = true;
        this.currentRow = item;

        let selectedId = [];
        if(modalVar == 'showDeleteDialog')
          selectedId = this.selected;
  
        this.currentId = selectedId.length ? selectedId : this.currentRow.id;
      },
      DestroyModal(result) {
        this.currentRow = {};
        this.currentId = null;
        if(result !== undefined)
          this.fetchData();
      },
      OnSortChanged(event) {
        this.sorting = {
          sortBy: event.sortBy,
          sortDesc: event.sortDesc
        };
        this.fetchData();
      },
      autoSelectRow() {
        if(this.defaultIdSelected) {
          const target = this.items.find(x => x.id == this.defaultIdSelected);
          this.selected = [target?.id];
          this.currentParent = target?.parent ?? 0;
        }
      },
      onClickToAllSelect() {
        if(this.selectMode == 'multi') {
          if(this.isAllSelected) {
            this.selected = [];
          } else {
            this.selected = this.items.map(x => x.id);
          }
        }
      },
      OnClickToSelect(item) {
        if(this.noSelectFolder && item.is_folder) {
          return false;
        }

        const index = this.selected.indexOf(item.id);
        if(index > -1) {
          this.selected.splice(index, 1);
        } else {
          if(this.selectMode == 'single') {
            this.selected = [];
          }

          this.selected.push(item.id);
        }

        if(this.defaultIdSelected !== undefined) {
          const elem = this.items.find(x => x.id == item.id);
          this.$emit('update:fk', elem);
        }
      },
      OnClickFolder(item) {
        this.currentParent = item.id;
        if(!this.isModal) {
          this.$router.push({query: {parent: this.currentParent}});
        } else {
          this.fetchData();
        }
      },
      async OnReduceHierarchy() {
        const res = (await this.$http.get(`${this.httpModel}/${this.currentParent}`)).data;
        const item = this.prepareData(res)[0];
        this.currentParent = item.parent ?? 0;
        if(!this.isModal) {
          if(this.parent) {
            this.$router.push({query: {parent: this.currentParent}});
          } else {
            this.$router.push({query: {}});
          }
        } else {
          this.fetchData();
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
      },
      async OnClickEmitMove() {
        try {
          this.$http.post(`${this.httpModel}/${this.currentParent}`, {
          _method: 'move',
          items: this.selected,
        }).data;
        } catch(err) {
          console.log(err);
        }
        this.moveMode = false;
        this.selected = [];
        this.fetchData();
      },
    },
  }
</script>