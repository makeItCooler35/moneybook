<template>
  <b-container fluid>
    <b-row>
      <b-col cols="3" class="px-0">
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
        {title: 'Загрузить расходы из Excel (Тинькофф)', name: 'uploadtinkoff'},
        {title: 'Выгрузить расходы в Excel', name: 'unloadcosts'}
      ],
    };
  },
})
</script>
