<template>
  <b-container>
    <b-file
      v-model="file"
      :state="Boolean(file)"
      :placeholder="placeholder"
      :accept="acceptedFormats.join(',')"
      @input="OnChange"
    />
  </b-container>
</template>

<script>

export default({
  name: 'NFileInput',
  props: {
    acceptedFormats: {type: Array, default: () => []},
    value: {required: true}
  },
  data(){
    return{
      placeholder: 'Выберите файл',
    };
  },
  computed: {
    file: {
      get() {
        return this.value;
      },
      set(val) {
        this.$emit('input', val);
      }
    }
  },
  methods: {
    OnChange(item) {
      if(!(this.acceptedFormats.includes(item.type))) {
        this.file = null;
        this.placeholder = 'Неверный формат';
      }
      else {
        this.placeholder = item.name;
      }
    },
  }
})
</script>