<template>
  <b-container fluid>
    <b-row>
      <b-col cols="4">
        <b-list-group>
          <b-list-group-item 
            v-for="(item, key) of routes"
            :key="key"
          >
            {{item.title}}
          </b-list-group-item>
        </b-list-group>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>

export default({
  data(){
    return{
      routes:[
        {title: 'Загрузить расходы их Excel (Тинькофф)', name: 'pets'},
        {title: 'Типы животных', name: 'petTypes'},
        {title: 'О приложении', name: 'about'},
      ],
    };
  },
})
</script>
