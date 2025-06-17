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
                            {{ "¿Esta Seguro de que desea borrar este aeropuerto?" }}
                          </center>
                        </div>
                        </q-card-section >
                    <q-separator></q-separator>
                    </q-card-section >
                    <q-card-section>
                            <div class="q-pt-xl col-12 q-gutter-xl flex justify-center" >
                                <q-btn
                                  :label="'Cancelar'" 
                                  @click="onCancelClick" 
                                  :color="'grey'"
                                />
                                 <q-btn  
                                   :label="'Borrar'" 
                                   type="submit"
                                   color="negative" 
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
  import { useDialogPluginComponent }         from 'quasar';
  import { api } from 'src/boot/axios';
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

      const eliminate = async ()=>
      {
         
        const id = props.airport.iata_faa?.trim() || props.airport.icao?.trim()
        const response = await api.delete(`/airports/${encodeURIComponent(id)}`)
          Swal.fire({
            icon: 'success',
            title: '¡Aeropuerto editado!',
            text: response.data.message || 'El Aeropuerto fue actualizado correctamente.'
          })
      }

      const onSubmit = async () => {
          try {
                await eliminate()  
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
      return {
        dialogRef            ,
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