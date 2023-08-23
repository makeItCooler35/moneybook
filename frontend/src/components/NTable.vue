<template>
  <b-container fluid>
    <b-row align-v="center">
      <b-col>
        <b-button
          :disabled="!currentParent"
          title="Подняться по иерархии"
          @click="OnReduceHierarchy"
        >
          &lt;
        </b-button>
      </b-col>
      <b-col>
        <h1>
          {{ title }}
        </h1>
      </b-col>
      <b-col>
        <b-container fluid>
          <b-row>
            <b-col v-if="!isMoving" cols="10">
              <b-button
                v-if="!noMove && isSelectable"
                title="Переместить"
                :disabled="!Boolean(selected.length)"
                @click="isMoving = true"
              >
                Переместить
              </b-button>
            </b-col>
            <b-col v-else cols="10">
              <b-row>
                <b-col>
                  <b-button @click="OnClickEmitMove">
                    Переместить
                  </b-button>
                </b-col>
                <b-col>
                  <b-button variant="danger" @click="isMoving = false">
                    Отмена
                  </b-button>
                </b-col>
              </b-row>
            </b-col>
            <b-col class="right">
              <b-dropdown right>
                <b-dropdown-item @click="showFieldsDialog = true">Поля</b-dropdown-item>
                <b-dropdown-item @click="fetchData">Обновить</b-dropdown-item>
              </b-dropdown>
            </b-col>
          </b-row>
        </b-container>
      </b-col>
    </b-row>
    <b-row>
      <b-table
        :fields="fields"
        :items="items"
        :per-page="perPage"
        :busy="isBusy"
        :select-mode="selectMode"
        show-empty
        small
        label-sort-desc=""
        label-sort-asc=""
        label-sort-clear=""
        no-local-sorting
        no-select-on-click
        @sort-changed="OnSortChanged"
      >
        <template #head(selected) v-if="!isMoving">
          <b-button variant="outline-dark" @click="OnClickToAllSelect">
            <span :class="isAllSelected ? `text-dark` : `text-white`">
              &check;
            </span>
          </b-button>
        </template>
        <template #head(actions)>
          <b-container v-if="!isMoving" fluid>
            <b-button v-if="!noCreate" class="mx-1" title="Создать" @click="InitModal('showUpdInsDialog')">
              +
            </b-button>
            <b-button v-if="!noCreateFolder" class="mx-1" title="Создать папку" @click="InitModal('showUpdInsDialog', {}, true)">
              <b-img :src="require('@/assets/icons/folder.png')"/>
            </b-button>
          </b-container>
        </template>
        <template #cell(selected)="{item}" v-if="!isMoving">
          <b-button variant="outline-dark" @click="OnClickToSelect(item)">
            <span :class="selected.includes(item.id) ? `text-dark` : `text-white`">
              &check;
            </span>
          </b-button>
        </template>
        <template #cell()="{item, value, field}">
          <span v-if="item.is_folder">
            <span v-if="!selfFields.map(x => x.key).indexOf(field.key)">
              <b-img
                :src="require('@/assets/icons/folder.png')"
                @click="OnClickFolder(item)"
                class="pointer"
              />
              {{ item?.[folderName] ?? '' }}
            </span>
          </span>
          <span v-else>
            {{ value }}
          </span>
        </template>
        <template #cell(actions)="{item}" v-if="!isMoving">
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
        <template #empty>
          <h1>Произошла ошибка либо данных нет</h1>
        </template>
      </b-table>
    </b-row>
    <b-row class="mt-auto text-center border-bottom justify-content-end p-1">
      <b-col xl="5" sm="6" class="d-flex flex-row" align-content="center">
        <b-form-input
          v-model="currentPage"
          type="number"
          min="1"
          :max="totalPages"
          :state="isValidCurrentPage"
          @change="OnChangeCurrentPage"
          class="b-form-component"
        />
        <label class="mx-2 my-auto">
          страница из {{ totalPages }}
        </label>
      </b-col>
      <b-col xl="5" sm="6">
        <b-form-select
          v-model="perPage"
          :options="perPageOptions"
          @change="OnChangePerPage"
          class="b-form-component"
        />
        <label class="mx-2 my-auto">
          записей
          ({{Math.min(totalRows, this.items.length)}} из {{ totalRows }})
        </label>
      </b-col>
    </b-row>
    <!-- МОДАЛЬНЫЕ ОКНА-->
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
      :fields="selfFields"
      :start-row="currentRow"
      @close="DestroyModal"
    />
    <fields-dialog
      v-model="showFieldsDialog"
      :currentFields="selfFields.map(x => x.key)"
      :selection="selection"
      :httpModel="httpModel"
      @update="OnUpdateStorageFields"
    />
  </b-container>
</template>

<script>
import DeleteDialog from './ntable/DeleteDialog.vue';
import UpdInsDialog from './ntable/UpdInsDialog.vue';
import FieldsDialog from './ntable/FieldsDialog.vue';

export default {
  components: { DeleteDialog, UpdInsDialog, FieldsDialog },

  props: {
    httpModel: {type: String, required: true},

    /*возможность crud-операций на выборке*/
    noActions: {type: Boolean, default: false},
    noDelete: {type: Boolean, default: false},
    noUpdate: {type: Boolean, default: false},
    noCreate: {type: Boolean, default: false}, //не касается папок
    noCreateFolder: {type: Boolean, default: false},

    noMove: {type: Boolean, default: false}, //запрет переносить элементы

    /*работа с отметкой галочкой элементов выборки*/
    selectMode: {type: String, default: 'multi'},
    noSelectFolder: {type: Boolean, default: false},
    defaultIdSelected: {type: [Number, null], default: undefined},
  },

  data() {
    return {
      /*ПАГИНАЦИЯ*/
      perPage: this.$store.state.perPage ?? 10,
      perPageOptions: [10, 25, 50, 100],
      currentPage: 1,
      totalRows: 0,
      totalPages: 1,

      /*АКТИВАЦИЯ МОДАЛЬНЫХ ОКОН*/
      showDeleteDialog: false,
      showUpdInsDialog: false,
      showFieldsDialog: false,
      
      /*ТЕКУЩИЙ ЭЛЕМЕНТ И ИД ДЛЯ УДАЛЕНИЯ ЛИБО ОБНОВЛЕНИЯ*/
      currentRow: {},
      currentId: null,
      
      /*ОСНОВНЫЕ ЭЛЕМЕНТЫ ВЫБОРКИ*/
      items: [],
      title: '', //название выборки
      folderName: null,
      fields: [],

      selection: {}, // из .js

      selected: [], // выделенные элементы
      sorting: {}, // сортировка

      currentParent: undefined,

      isMoving: false, //режим перемещения
      isBusy: true, //ожидание ответа от бэка и заполнение данных
      firstCreated: true // первое отображение
    }
  },

  computed: {
    isAllSelected() {
      return [this.perPage, this.totalRows].includes(this.selected.length) && this.selected.length;
    },
    isValidCurrentPage() {
      if(1 <= this.currentPage && this.currentPage <= this.totalPages) {
        return null;
      } else { 
        return false;
      }
    },
    isSelectable() {
      if(['multi', 'single'].includes(this.selectMode)) {
        return true;
      }
      return false;
    },
    selfFields() {
      return this.fields.filter(x => x?.self ?? true);
    }
  },

  async created() {
    await this.fetchData(); //сначала подгружаем выборку
    this.autoSelectRow(); //затем выделяем дефолтный элемент
    this.firstCreated = false;
  },
  
  methods: {
    async fetchData() {
      //обращение к бэку, заполнение данных
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
              startId: this.firstCreated ? this.defaultIdSelected : undefined,
              parent: this.currentParent
            }
          })
        ).data;

      this.items = [...this.prepareData(res.rows, res.fields)];

      this.totalRows = res.service.count_rows;
      this.totalPages = res.service.count_pages;

      this.currentPage = res.service.page;

      // смотрим описание выборки
      this.selection = (await import(`../selections/${this.httpModel}`)).default;

      // смотрим в хранилище
      const selectionStore = this.$store.getters.getSelection(this.httpModel);

      // оставляем только то, что нужно пользователю
      let selectionFields = [...this.selection.fields];
      if(Object.keys(selectionStore).length) {
        selectionFields = this.selection.fields.filter(x => selectionStore.includes(x.key));
      }

      this.title = this.selection.title;
      this.folderName = this.selection.folderName ?? null;
      this.fields = [...selectionFields];

      // отметка галочкой
      if(this.isSelectable)
      {
        this.fields.unshift({
          key: 'selected',
          label: '',
          self: false
        });
      }

      // удаление и обновление
      if(!this.noActions)
      {
        this.fields.push({
          key: 'actions',
          label: '',
          self: false
        });
      }

      /* выравниваем поля по центру и указываем сортировку */
      for(const item of this.fields) {
        item.class = item.class ?? 'text-center';
        item.sortable = item.self ?? true;
      }
    } catch(err) {
      this.items = [];
      this.allFields = [];
      this.fields = [];
    } finally {
      this.isBusy = false;
    }
  },

    prepareData(rows, fields) {
      // собираем массив для b-table
      let arr = [];
      for(const row of rows) {
        let item = {};
        for(const [num, field] of Object.entries(fields)) {
          item[field] = row[num];
        }
        arr.push(item);
      }
      return arr;
    },

    InitModal(modalVar, item = {}, folder = false) {
      // инициализация модальных окон crud
      this[modalVar] = true;
      this.currentRow = {...item, is_folder: item.is_folder ?? folder};

      let selectedId = [];
      if(modalVar == 'showDeleteDialog') {
        selectedId = this.selected;
      }

      this.currentId = selectedId.length ? selectedId : this.currentRow.id;
    },

    DestroyModal(result) {
      // завершение модальных окон crud
      this.currentRow = {};
      this.currentId = null;
  
      if(result !== undefined) {
        this.fetchData();
      }
    },

    OnSortChanged(event) {
      /*ПОЛЬЗОВАТЕЛЬ КЛИКНУЛ НА ПОЛЕ В ШАПКЕ ВЫБОРКИ*/
      this.sorting = {
        sortBy: event.sortBy,
        sortDesc: event.sortDesc
      };
 
      this.fetchData();
    },

    autoSelectRow() {
      // значение по умолчанию (актуально сейча для нлинкфилд)
      if(this.defaultIdSelected) {
        const target = this.items.find(x => x.id == this.defaultIdSelected);
        this.selected = [target.id];
        this.currentParent = target.parent;
      }
    },

    OnClickToAllSelect() {
      // ПОЛЬЗОВАТЕЛЬ НАЖАЛ НА КНОПКУ ВЫБОРА/ОТМЕНЫ ВЫБОРА ВСЕХ ЗАПИСЕЙ ВЫБОРКИ
      // для режима single неактуально
      if(this.selectMode == 'multi') {
        if(this.isAllSelected) {
          this.selected = [];
        } else {
          this.selected = this.items.map(x => x.id);
        }
      }
    },

    OnClickToSelect(item) {
      // ПОЛЬЗОВАТЕЛЬ ВЫБИРАЕТ/ОТМЕНЯЕТ ЕДИНИЧНУЮ ЗАПИСЬ
      if(this.noSelectFolder && item.is_folder) {
        // стоит запрет на выбор папок
        return false;
      }

      const index = this.selected.indexOf(item.id);
      if(index > -1) {
        this.selected.splice(index, 1); // запись была выбрана -> удаляем
      } else {
        if(this.selectMode == 'single') {
          this.selected = []; // одна запись мб выбрана
        }

        this.selected.push(item.id); // добавляем новую запись
      }

      if(this.defaultIdSelected !== undefined) {
        const elem = this.items.find(x => x.id == item.id);
        this.$emit('update:fk', elem);
      }
    },

    OnClickFolder(item) {
      // ПОЛЬЗОВАТЕЛЬ НАЖАЛ НА ПАПКУ (падаем по иерархии)
      this.currentParent = item.id;
      this.currentPage = 1;
      this.fetchData();
    },

    async OnReduceHierarchy() {
      // ПОЛЬЗОВАТЕЛЬ НАЖАЛ НА КНОПКУ НАЗАД ПО ИЕРАРХИИ (возвращаемся по иерархии)
      const res = (await this.$http.get(`${this.httpModel}/${this.currentParent}`)).data;
      const item = this.prepareData(res.rows, res.fields)[0];
      this.currentParent = item.parent;
      this.currentPage = 1;
      this.fetchData();
    },

    async OnChangePerPage() {
      // ПОЛЬЗОВАТЕЛЬ МЕНЯЕТ КОЛИЧЕСТВО ЗАПИСЕЙ НА СТРАНИЦЕ
      await this.fetchData();

      this.$store.commit('CHANGE_PER_PAGE', this.perPage); //сохраняем в хранилище
    },

    OnChangeCurrentPage() {
      // ПОЛЬЗОВАТЕЛЬ МЕНЯЕТ ТЕКУЩУЮ СТРАНИЦУ
      if(this.isValidCurrentPage == null) {
        this.fetchData();
      }
    },

    async OnClickEmitMove() {
      // ПОЛЬЗОВАТЕЛЬ ПЕРЕМЕЩАЕТ ЗАПИСИ МЕЖДУ ПАПКАМИ
      await this.$http.post(`${this.httpModel}/${Number(this.currentParent)}`, {
        _method: 'move',
        items: this.selected,
      });

      this.isMoving = false;
      this.selected = [];
      this.fetchData();
    },

    OnUpdateStorageFields(fields) {
      // ПОЛЬЗОВАТЕЛЬ МЕНЯЕТ ПОЛЯ ВЫБОРКИ
      this.$store.commit("CHANGE_SELECTION", {name: this.httpModel, fields});
      this.fetchData();
    }
  },
}
</script>