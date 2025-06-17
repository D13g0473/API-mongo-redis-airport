<template>
  <q-layout view="lHh Lpr lFf">

    <q-drawer
      v-model="leftDrawerOpen"
      show-if-above
      bordered
    >
    <q-list>
  <q-item-label header>
    Enlaces
  </q-item-label>

  <template v-for="link in linksList" :key="link.title">
    <q-item
      v-if="link.to"
      clickable
      tag="router-link"
      :to="link.to"
    >
      <q-item-section avatar>
        <q-icon :name="link.icon" />
      </q-item-section>
      <q-item-section>
        <q-item-label>{{ link.title }}</q-item-label>
        <q-item-label caption>{{ link.caption }}</q-item-label>
      </q-item-section>
    </q-item>

    <q-item
      v-else
      clickable
      tag="a"
      :href="link.href"
      target="_blank"
    >
      <q-item-section avatar>
        <q-icon :name="link.icon" />
      </q-item-section>
      <q-item-section>
        <q-item-label>{{ link.title }}</q-item-label>
        <q-item-label caption>{{ link.caption }}</q-item-label>
      </q-item-section>
    </q-item>
  </template>
</q-list>

    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { ref } from 'vue'

const linksList = [
  {
    title: 'Mapa',
    caption: 'ver mapa de aeropuertos',
    icon: 'map',
    to: '/' 
  },
  {
    title: 'Top 10 pupulares',
    caption: 'Ver top aeropuertos populares',
    icon: 'star',
    to: '/popular' 
  }
]


const leftDrawerOpen = ref(false)


// function toggleLeftDrawer () {
//   leftDrawerOpen.value = !leftDrawerOpen.value
// }
</script>
