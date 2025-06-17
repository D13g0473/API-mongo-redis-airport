import { LMap, LTileLayer, LMarker, LPopup } from '@vue-leaflet/vue-leaflet'

export default ({ app }) => {
  app.component('l-map', LMap)
  app.component('l-tile-layer', LTileLayer)
  app.component('l-marker', LMarker)
  app.component('l-popup', LPopup)
}