<template>
  <l-map
    ref="mapRef"
    style="height: 90vh; width: 100vw"
    :zoom="2"
    :center="[0, 0]"
  >
    <l-tile-layer
      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      attribution="&copy; OpenStreetMap contributors"
    />
  </l-map>
    <q-page-sticky position="bottom-right" :offset="[5, 5]">
            <q-btn fab icon="add" color="positive" @click="createAirport()" />
    </q-page-sticky>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import {
  LMap,
  LTileLayer,
} from '@vue-leaflet/vue-leaflet'
import L from 'leaflet'
import 'leaflet.markercluster'
import { api } from 'src/boot/axios'
import { Dialog } from 'quasar'
import FormAirport from 'src/components/FormAirport.vue'
import DeleteFormAriport from 'src/components/DeleteFormAriport.vue'
import Swal from 'sweetalert2'
import NearbyForm from 'src/components/NearbyForm.vue'
// import { Dialog } from 'quasar'

const mapRef = ref(null)
const airports = ref([])

const createAirport = () => {
  // Aquí puedes implementar la lógica para crear un nuevo aeropuerto
  Dialog.create({
    title: 'Crear Aeropuerto',
    component: FormAirport,
    componentProps: {
      typeForm: 1 // 1 para crear, 2 para editar, 3 para ver
    },
    persistent: true,
    ok: {
      label: 'Crear',
      color: 'primary'
    },
    cancel: {
      label: 'Cancelar',
      color: 'negative'
    }
  }).onOk(() => loadAirportsAndRenderMarkers())
}

// onMounted(async () => {
//   const { data } = await api.get('/airports')
//   airports.value = data

//   // Esperar a que se monte el mapa
//   setTimeout(() => {
//     const map = mapRef.value?.leafletObject
//     if (!map) return

//     const cluster = L.markerClusterGroup()

//     airports.value.forEach(a => {
//       if (!a.lat || !a.lng) return

//       const marker = L.marker([a.lat, a.lng])

//       marker.on('click', async () => {
//         try {
//           console.log('icao:', a.icao)
//           console.log('iata_faa:', a.iata_faa)
//           const id = a.iata_faa?.trim() || a.icao?.trim()
          
//           if (!id) return
          
//           const { data } = await api.get(`/airports/${ encodeURIComponent(id)}`)
//           console.log(data);
//           if (!data) {
//             marker.bindPopup("No se encontraron datos del aeropuerto").openPopup()
//             return
//           }
//           const content = `
//             <b>${data.name}</b><br/>
//             ${data.city}<br/>
//             Código: ${data.iata_faa || data.icao}<br/>
//             <button id="edit-airport-${a.iata_faa || a.icao}" class="btn">Editar</button>
//             <button id="Nearby-airport-${a.iata_faa || a.icao}" class="btn">Cercanos</button>
//             <button id="delete-airport-${a.iata_faa || a.icao}" class="btn">Borrar</button>

//           `
//           marker.bindPopup(content).openPopup()
//           // marker.on('popupopen', () => {
//           const btn = document.getElementById(`edit-airport-${a.iata_faa || a.icao}`)
//             if (btn) {
//               btn.addEventListener('click', () => {
//                 // Aquí podés abrir un modal o lanzar alguna lógica de actualización
//                 Dialog.create({
//                   title: 'Editar Aeropuerto',
//                   component: FormAirport,
//                   componentProps: {
//                     airport: data, // Pasar los datos del aeropuerto al formulario
//                     typeForm: 2 
//                   },
//                   cancel: true,
//                   persistent: true,
//                 }).onOk(() => {
//                 })
              
//                 // Ejemplo: emitir un evento o usar un store
//               //  openEditModal(a)  // este sería tu método o lógica Vue
//               })
//             }

//           const btnDelete = document.getElementById(`delete-airport-${a.iata_faa || a.icao}`)
//           if (btnDelete){
//             btnDelete.addEventListener('click',()=>{
//               Dialog.create({
//                   title: 'Borrar Aeropuerto',
//                   component: DeleteFormAriport,
//                   componentProps: {
//                     airport: data, // Pasar los datos del aeropuerto al formulario
//                     typeForm: 2 
//                   },
//                   cancel: true,
//                   persistent: true,
//                 }).onOk(() => {
//                   // Aquí puedes implementar la lógica para editar el aeropuerto
//                   Swal.fire({
//                     icon: 'success',
//                     title: '¡Aeropuerto borrado!',
//                     text: 'El Aeropuerto fue eliminado correctamente.'
//                   })
//                 })
//             })
//           }

//           const btnNearby = document.getElementById(`Nearby-airport-${a.iata_faa || a.icao}`)
//           if (btnNearby){
//             btnNearby.addEventListener('click',()=>{
//               Dialog.create({
//                   title: 'Calcular cercanos',
//                   component: NearbyForm,
//                   componentProps: {
//                     airport: data, // Pasar los datos del aeropuerto al formulario
//                   },
//                   cancel: true,
//                   persistent: true,
//                 }).onOk(() => {
//                 })
//             })
//           }
//           // })
//         } catch (e) {
          
//           console.error('Error cargando detalles del aeropuerto', e)
//         }
//       })

//       cluster.addLayer(marker)
//     })

//     map.addLayer(cluster)
//     const bounds = cluster.getBounds()
//     if (bounds.isValid()) {
//       map.fitBounds(bounds)
//     }
//   }, 300)
// })

const loadAirportsAndRenderMarkers = async () => {
  const { data } = await api.get('/airports')
  airports.value = data

  const map = mapRef.value?.leafletObject
  if (!map) return

  // Limpia el mapa (en caso de que haya clusters previos)
  map.eachLayer(layer => {
    if (layer instanceof L.MarkerClusterGroup) {
      map.removeLayer(layer)
    }
  })

  const cluster = L.markerClusterGroup()

  airports.value.forEach(a => {
    if (!a.lat || !a.lng) return

    const marker = L.marker([a.lat, a.lng])

    marker.on('click', async () => {
      try {
        const id = a.iata_faa?.trim() || a.icao?.trim()
        if (!id) return

        const { data } = await api.get(`/airports/${encodeURIComponent(id)}`)

        if (!data) {
          marker.bindPopup("No se encontraron datos del aeropuerto").openPopup()
          return
        }

        const content = `
          <b>${data.name}</b><br/>
          ${data.city}<br/>
          Código: ${data.iata_faa || data.icao}<br/>
          <button id="edit-airport-${id}" class="btn">Editar</button>
          <button id="Nearby-airport-${id}" class="btn">Cercanos</button>
          <button id="delete-airport-${id}" class="btn">Borrar</button>
        `
        marker.bindPopup(content).openPopup()

        // Acciones de los botones
        const btn = document.getElementById(`edit-airport-${id}`)
        if (btn) {
          btn.addEventListener('click', () => {
            Dialog.create({
              title: 'Editar Aeropuerto',
              component: FormAirport,
              componentProps: { airport: data, typeForm: 2 },
              cancel: true,
              persistent: true
            }).onOk(() => loadAirportsAndRenderMarkers())
          })
        }

        const btnDelete = document.getElementById(`delete-airport-${id}`)
        if (btnDelete) {
          btnDelete.addEventListener('click', () => {
            Dialog.create({
              title: 'Borrar Aeropuerto',
              component: DeleteFormAriport,
              componentProps: { airport: data, typeForm: 2 },
              cancel: true,
              persistent: true
            }).onOk(() => {
              Swal.fire({
                icon: 'success',
                title: '¡Aeropuerto borrado!',
                text: 'El Aeropuerto fue eliminado correctamente.'
              })
              loadAirportsAndRenderMarkers() // 👈 Recarga todo
            })
          })
        }

        const btnNearby = document.getElementById(`Nearby-airport-${id}`)
        if (btnNearby) {
          btnNearby.addEventListener('click', () => {
            Dialog.create({
              title: 'Calcular cercanos',
              component: NearbyForm,
              componentProps: { airport: data },
              cancel: true,
              persistent: true
            })
          })
        }
      } catch (e) {
        console.error('Error cargando detalles del aeropuerto', e)
      }
    })

    cluster.addLayer(marker)
  })

  map.addLayer(cluster)
  const bounds = cluster.getBounds()
  if (bounds.isValid()) {
    map.fitBounds(bounds)
  }
}
onMounted(() => {
  setTimeout(() => {
    loadAirportsAndRenderMarkers()
  }, 300)
})

</script>
