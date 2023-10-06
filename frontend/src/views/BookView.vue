<template>
  <n-table
    http-model="book"
    no-create-folder
    no-move
  >
    <template #filter="{fltr}">
      <b-form class="n-form d-flex flex-column">
        <b-row>
          <b-col cols="3">
            <label>Сумма</label>
          </b-col>
          <b-col>
            <b-form-input
              v-model="fltr.sum"
              type="number"
              :state="fltr.sum === '' ? false : null"
              class="text-right"
            />
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="5">
            <label>С</label>
            <n-date-input v-model="fltr.dateStart" />
          </b-col>
          <b-col cols="5">
            <label>По</label>
            <n-date-input v-model="fltr.dateEnd" />
          </b-col>
        </b-row>
        <b-row>
          <b-col cols="3">
            <label>Категория</label>
          </b-col>
          <b-col>
            <n-link-field
              http-model="categories"
              v-model="fltr.categoryId"
              :text="categoryName"
              @input="OnInputFK($event, fltr)"
            />
          </b-col>
        </b-row>
      </b-form>
    </template>
  </n-table>
</template>

<script>
import NDateInput from '@/components/NDateInput.vue';
import NLinkField from '@/components/NLinkField.vue';

export default {
  name: 'BookView',
  components: {
    NDateInput, NLinkField
  },
  data() {
    return {
      categoryName: ''
    }
  },
  methods: {
    OnInputFK(event, fltr) {
      fltr.categoryId = event.id;
      this.categoryName = event.value;
    }
  }
}
</script>
