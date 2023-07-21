<template>
  <b-container fluid>
    <b-row>
      <b-col cols="3">
        <b-list-group>
          <b-list-group-item 
            v-for="(item, key) of items"
            :key="key"
            :to="{name: item.name}"
            variant="primary"
          >
          {{ item.title }}
          </b-list-group-item>
        </b-list-group>
      </b-col>
      <b-col>
        <router-view />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>

export default({
  data(){
    return{
      items:[
        {title: 'Загрузить расходы их Excel (Тинькофф)', name: 'uploadtinkoff'},
      ],
    };
  },
})
</script>
