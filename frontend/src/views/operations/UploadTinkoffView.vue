<template>
  <b-container>
    <b-row>
      <n-file-input
        v-model="file"
        :accepted-formats="acceptedFormats"
        @start-upload="Upload"
        class="p-0"
      />
    </b-row>
    <b-row class="mt-2">
      <b-button
        variant="success"
        :disabled="!Boolean(file)"
        @click="Upload"
      >
        Загрузить
      </b-button>
    </b-row>
  </b-container>
</template>

<script>
import NFileInput from "../../components/NFileInput.vue";
export default({
  name: 'UpLoadTinkoff',
  components: {
    NFileInput
  },
  data() {
    return {
      file: null,
      httpModel: 'book',
      acceptedFormats: ['application/vnd.ms-excel']
    };
  },
  methods: {
    async Upload() {
      await this.$http.post(
        this.httpModel, 
        {_method: "upload_excel", file: this.file},
        {headers: {'Content-Type': 'multipart/form-data'}}
      );
    }
  }
})
</script>

