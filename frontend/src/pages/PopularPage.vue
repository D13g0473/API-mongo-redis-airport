<template>
    <q-card >
    <q-table
    style="height: 100vh;"
        :rows="popularAirports"
        :columns="[
            { name: 'name',         label: 'Nombre',        field: 'name' ,         align: 'center'},
            { name: 'city',         label: 'Ciudad',        field: 'city' ,         align: 'center'},
            { name: 'iata_faa',     label: 'IATA/FAA Code', field: 'iata_faa' ,     align: 'center'},
            { name: 'icao',         label: 'ICAO Code',     field: 'icao',          align: 'center'},
            { name: 'popularity',   label: 'Popularidad',   field: 'popularity',    align: 'center'}
        ]"
        row-key="id"
        title="Popular Airports"
        no-data-label="No popular airports found"
        :pagination="{
            rowsPerPage: 10,
            page: 1
        }"
    >

    </q-table>
    </q-card>
</template>

<script setup>
import { api } from 'src/boot/axios';

import { ref, onMounted } from 'vue';

const popularAirports = ref([]);
onMounted(async () => {
    try {
        const { data } = await api.get('/airports/popular');
        console.log(data);
        var true_data =  data.filter(airport => airport.code != 'undefined'); // Filter out airports with no popularity
        console.log(true_data);
        popularAirports.value = true_data;
    } catch (error) {
        console.error('Error fetching popular airports:', error);
    }
});


</script>