<template>
  <div>
    <b-button v-b-toggle.sidebar-1>
      <img src="@/assets/icons/house-door.svg"/>
    </b-button>
    <b-sidebar id="sidebar-1" title="Личные финансы">
      <b-list-group>
        <b-list-group-item 
          v-for="(item, key) of items"
          :key="key"
          :to="{name: item.name}"
        >
            {{item.title}}
        </b-list-group-item>
      </b-list-group>
    </b-sidebar>
  </div>
</template>

<script>

export default({
  data(){
    return{
      items:[
        {title: 'Операции', name: 'operations'},
        {title: 'Справочники', name: 'handbooks'},
        {title: 'О приложении', name: 'about'},
      ],
    };
  },
})
</script>
