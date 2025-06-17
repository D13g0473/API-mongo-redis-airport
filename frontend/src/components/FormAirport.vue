<template>
    <!-- notice dialogRef here -->
    <q-dialog  ref="dialogRef" @hide="onDialogHide" maximized >
      <q-card class="q-dialog-plugin custom-card" style="width: auto; background-color: transparent;">
        <center>
          <div class="container row justify-center pc-sa">
              <div elevated class="q-ma-sm q-card--bordered col-12">
                <q-card>
                    <q-separator class="q-mb-sm"></q-separator>
                    <q-form @submit="onSubmit" >
                    <q-card-section >
                        <q-card-section  >
                        <div class="text-h6">
                          <center>
                            {{ title }}
                          </center>
                        </div>
                    </q-card-section >
                    <q-separator></q-separator>
                        <q-card-section>
                            <div class="row q-py-sm">
                            <div class="col-12 flex justify-center" style="height: 25px;">
                                      <q-item>
                                        <q-input
                                            style   = "min-width: 25vw; height: 20px;"
                                            v-model = "name"
                                            type    = 'text'
                                            label   = 'Nombre del Aeropuerto'
                                            :disable="(typeForm==3)"
                                            required
                                            filled
                                            dense
                                        />
                                      </q-item>
                            </div>
                          </div>
                        <div class="row q-py-sm">
                            <div class="col-12 flex justify-center" style="height: 25px;">
                                      <q-item>
                                        <q-input
                                            style   = "min-width: 25vw; height: 20px;"
                                            v-model = "city"
                                            type    = 'text'
                                            label   = 'Ciudad'
                                            :disable="(typeForm==3)"
                                            required
                                            filled
                                            dense
                                        />
                                      </q-item>
                            </div>
                          </div>
                        <div class="row q-py-sm">
                            <div class="col-12 flex justify-center" style="height: 25px;">
                                      <q-item>
                                        <q-input
                                            style   = "min-width: 25vw; height: 20px;"
                                            v-model = "iata_faa"
                                            type    = 'text'
                                            label   = 'Código IATA/FAA'
                                            :disable="(typeForm==2)"
                                            required
                                            filled
                                            dense
                                        />
                                      </q-item>
                            </div>
                          </div>
                        <div class="row q-py-sm">
                            <div class="col-12 flex justify-center" style="height: 25px;">
                                      <q-item>
                                        <q-input
                                            style   = "min-width: 25vw; height: 20px;"
                                            v-model = "icao"
                                            type    = 'text'
                                            label   = 'Código ICAO'
                                            :disable="(typeForm==2)"
                                            required
                                            filled
                                            dense
                                        />
                                      </q-item>
                            </div>
                          </div>
                        <div class="row q-py-sm">
                            <div class="col-12 flex justify-center" style="height: 25px;">
                                      <q-item>
                                        <q-input
                                            style   = "min-width: 25vw; height: 20px;"
                                            v-model = "lat"
                                            type    = 'number'
                                            label   = 'Latitud'
                                            :disable="(typeForm==3)"
                                            required
                                            filled
                                            dense
                                        />
                                      </q-item>
                            </div>
                          </div>
                        <div class="row q-py-sm">
                            <div class="col-12 flex justify-center" style="height: 25px;">
                                      <q-item>
                                        <q-input
                                            style   = "min-width: 25vw; height: 20px;"
                                            v-model = "lng"
                                            type    = 'number'
                                            label   = 'Longitud'
                                            :disable="(typeForm==3)"
                                            required
                                            filled
                                            dense
                                        />
                                      </q-item>
                            </div>
                          </div>
                        <div class="row q-py-sm">
                            <div class="col-12 flex justify-center" style="height: 25px;">
                                      <q-item>
                                        <q-input
                                            style   = "min-width: 25vw; height: 20px;"
                                            v-model = "altitude"
                                            type    = 'number'
                                            label   = 'Altitud'
                                            :disable="(typeForm==3)"
                                            required
                                            filled
                                            dense
                                        />
                                      </q-item>
                            </div>
                          </div>
                        <div class="row q-py-sm">
                            <div class="col-12 flex justify-center" style="height: 25px;">
                                      <q-item>
                                        <q-input
                                            style   = "min-width: 25vw; height: 20px;"
                                            v-model = "timezone"
                                            type    = 'text'
                                            label   = 'Zona Horaria'
                                            :disable="(typeForm==3)"
                                            required
                                            filled
                                            dense
                                        />
                                      </q-item>
                            </div>
                          </div>
                        </q-card-section>
                    </q-card-section >
                    <q-card-section>
                            <div class="q-pt-xl col-12 q-gutter-xl flex justify-center" >
                                <q-btn
                                  :label="typeForm==3?'Cerrar':'Cancelar'" 
                                  @click="onCancelClick" 
                                  :color="typeForm==3?'info':'grey'"
                                />
                                 <q-btn  
                                   v-if = "!(typeForm==3)"
                                   :label="'Guardar'" 
                                   type="submit"
                                   color="green" 
                                 />
                            </div>
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
//   import { onMounted } from "vue";
  import { useDialogPluginComponent }         from 'quasar';
  import { api } from 'src/boot/axios';
  import { ref } from 'vue'
  import Swal from 'sweetalert2'




  export default {
    props: {
       airport: {
          type: Object,
          required: false,
       },
       typeForm:{
          type:Number,
          required:true,
          default:1
       }
    },
  
    emits: [
      ...useDialogPluginComponent.emits
    ],
    // components: {
    //     FormScheme          : defineAsyncComponent(() => import('components/assets/FormScheme.vue'))
    // }, 
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
      const name = ref('')
      const city = ref('')
      const iata_faa = ref('')
      const icao = ref('')
      const lat = ref('')
      const lng = ref('')
      const altitude = ref('')
      const timezone = ref('')


      const post = async (body)=>
      {
        console.log(body);
        
        const response = await api.post("/airports", body)
          Swal.fire({
            icon: 'success',
            title: '¡Aeropuerto creado!',
            text: response.data.message || 'El Aeropuerto fue creado correctamente.'
          })
      }

      const update = async (body)=>
      {
        console.log(body);
        const id = body.iata_faa?.trim() || body.icao?.trim()
        const response = await api.put(`/airports/${encodeURIComponent(id)}`, body)
          Swal.fire({
            icon: 'success',
            title: '¡Aeropuerto editado!',
            text: response.data.message || 'El Aeropuerto fue actualizado correctamente.'
          })
      }

      const onSubmit = async () => {
          const body = {
            name: name.value,
            city: city.value,
            iata_faa: iata_faa.value,
            icao: icao.value,
            lat: lat.value,
            lng: lng.value,
            alt: altitude.value,
            tz: timezone.value
          }
        
           
          try {
          
                if (props.typeForm==1) 
                  await post(body)
          
                if (props.typeForm==2) 
                await update(body)  
          
                onDialogOK()
              }
          catch (err) 
              {
                console.log(err);

                Swal.fire({
                  icon: 'error',
                  title: 'Error',
                  text: err.response?.data?.error || 'Ocurrió un error al guardar el aeropuerto.'
                })
              }
        }

      if(props.typeForm==2 && props.airport)
      {
        name.value = props.airport.name
        city.value = props.airport.city
        iata_faa.value = props.airport.iata_faa
        icao.value = props.airport.icao
        lat.value = props.airport.lat
        lng.value = props.airport.lng
        altitude.value = props.airport.alt
        timezone.value = props.airport.tz
      }
      return {
        dialogRef            ,
        name                 ,
        city                 ,
        iata_faa             ,
        icao                 ,  
        lat                  ,
        lng                  ,
        altitude             ,
        timezone             ,
        title :  props.typeForm==1 ? "Crear Aeropuerto" : props.typeForm==2 ? "Editar Aeropuerto" : "Ver Aeropuerto",
        onDialogHide         ,
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