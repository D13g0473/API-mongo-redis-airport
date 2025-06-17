<template>
    <!-- notice dialogRef here -->
    <q-dialog  ref="dialogRef" @hide="onDialogHide" maximized >
      <q-card class="q-dialog-plugin custom-card" style="width: auto; background-color: transparent;">
        <center>
          <div class="container row justify-center pc-sa">
              <div elevated class="q-ma-sm q-card--bordered col-12">
                <q-card>
                    <q-separator class="q-mb-sm"></q-separator>
                    <q-form @submit="onSubmit" style= "width: 80vw;" >
                        <q-card-section  >
                        <div class="text-h6">
                          <center>
                            {{ "Ingrese la distancia en KM para calcular cercanos." }}
                          </center>
                        </div>
                        </q-card-section >
                    <q-separator></q-separator>
                    <q-card-section >
                        <q-input
                          v-model="radius"
                          type="number"
                          label="Distancia (KM)"
                          :rules="[val => val > 0 || 'La distancia debe ser mayor a 0']"
                          outlined
                          dense
                          class="q-mb-md"
                        />
                    </q-card-section>
                    <q-card-section v-if="airports.length">
                        <center>
                            <q-table    
                                :title="'Aeropuertos Cercanos'"
                                :rows="airports"
                                :columns="[
                                     { name: 'name',         label: 'Nombre',        field: 'name' ,         align: 'center'},
                                     { name: 'city',         label: 'Ciudad',        field: 'city' ,         align: 'center'},
                                     { name: 'iata_faa',     label: 'IATA/FAA Code', field: 'iata_faa' ,     align: 'center'},
                                     { name: 'icao',         label: 'ICAO Code',     field: 'icao',          align: 'center'},
                                     { name: 'distance_km',  label: 'Distancia en KM',    field: 'distance_km',   align: 'center'}
                                 ]"
                            >

                            </q-table>
                    </center>
                    </q-card-section >
                    <q-card-section>
                            <div class="q-pt-xl col-12 q-gutter-xl flex justify-center" >
                                <q-btn
                                  :label="'Cancelar'" 
                                  @click="onCancelClick" 
                                  :color="'grey'"
                                />
                                 <q-btn  
                                   :label="'Calcular'" 
                                   type="submit"
                                   color="positive" 
                                 />
                            </div>
                        </q-card-section>
                        <q-card-section>
                            
                        </q-card-section>
                    </q-form>
                </q-card>
            </div>
          </div>
        </center>
      </q-card>
    </q-dialog>
  </template>
  
  <script>
  import { useDialogPluginComponent }         from 'quasar';
  import { api } from 'src/boot/axios';
  import Swal from 'sweetalert2'
  import { ref } from 'vue'
  export default {
    props: {
       airport: {
          type: Object,
          required: false,
       }
    },
  
    emits: [
      ...useDialogPluginComponent.emits
    ],
    setup (props) 
    {
      const { dialogRef, onDialogHide, onDialogOK, onDialogCancel } = useDialogPluginComponent()
      // REQUIRED; must be called inside of setup()
      // dialogRef      - Vue ref to be applied to QDialog
      // onDialogHide   - Function to be used as handler for @hide on QDialog
      // onDialogOK     - Function to call to settle dialog with "ok" outcome
      //                    example: onDialogOK() - no payload
      //                    example: onDialogOK({ /*.../* }) - with payload
      // onDialogCancel - Function to call to settle dialog with "cancel" outcome

    const radius = ref(0)
    const airports = ref([])    
      const nearby = async ()=>
      {
        if(radius.value <= 0)
        {
          Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'La distancia debe ser mayor a 0.'
          })
          return
        } 
        const response = await api.get(`/airports/nearby?lat=${encodeURIComponent(props.airport.lat)}&lng=${encodeURIComponent(props.airport.lng)}&radius=${radius.value}`)

        airports.value = response.data.filter(port => port.name != props.airport.name);
      }

      const onSubmit = async () => {
          try {
                await nearby()  
              }
          catch (err) 
              {
                console.log(err);

                Swal.fire({
                  icon: 'error',
                  title: 'Error',
                  text: err.response?.data?.error || 'Ocurrió un error al calcular cercanos.'
                })
              }
        }
      return {
        dialogRef            ,
        onDialogHide         ,
        airports             ,
        radius               ,
        onOKClick () 
        {
          onDialogOK()
        },
        onSubmit,
        onCancelClick: onDialogCancel

      }
    }
  }
  </script>

  <style>

.custom-card{
  box-shadow:none

}
</style>