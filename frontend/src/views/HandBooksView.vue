<template>
  <b-container fluid class="mx-auto">
    <b-row>
      <b-col v-for="(item,  key) of items" :key="key" class="text-center">
        <b-button :to="{name: item.name}">
          <b-card
            :img-src="require('../assets/icons/books.png')"
            style="min-width: min-content;height: 11rem;"
            class="mb-2"
          >
            <b-card-text class="text-dark">
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
