<template>
  <b-container fluid class="mx-auto">
    <b-row>
      <b-col v-for="(item,  key) of items" :key="key" class="text-center">
        <b-button :to="{name: item.name}" variant="primary">
        <b-card
          :img-src="require('../assets/icons/books.png')"
          tag="article"
          style="width: 7rem;height: 11rem;"
          class="mb-2"
        >
        <b-card-text>
          {{ item.title }}
        </b-card-text>
        </b-card>
        </b-button>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>

export default({
  data(){
    return{
      items:[
        {title: 'Категории', name: 'categories'},
        {title: 'Счета', name: 'accounts'},
      ],
    };
  },
})
</script>
