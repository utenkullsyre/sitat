<template lang="html">
  <v-layout row wrap justify-center>
    <v-dialog
      v-model="dialog"
      scrollable
      :overlay="true"
      max-width="500px"
      transition="dialog-transition"
      class="ma-1"
    >
    <v-avatar
      slot="activator"
      dark
    >
      <v-icon x-large>add</v-icon>
    </v-avatar>
    <v-card class="py-1" max-height="1000px">
          <v-card-text class="sidelinje">
            <v-form ref="form" @submit="submit">
              <h1>Legg til sitat</h1>
              <v-textarea
                name="input-7-1"
                v-model="sitat"
                label="Sitat"
                hint="Skriv inn sitatet her"
                required
             ></v-textarea>
             <v-textarea
               name="input-7-1"
               v-model="beskrivelse"
               label="Beskrivelse"
               hint="Skriv inn beskrivelse her"
               required
            ></v-textarea>
              <v-select
                ripple

                :items="humoer"
                item-text="navn"
                item-value="id"
                label="Velg humør"
                v-model="humoer_id"
              ></v-select>

                <v-checkbox
                 ripple
                  :disabled="!navigatorGeolocation"
                  label="Legg til plassering"
                  v-model="lokaliser"
                 @change=""
                >
              </v-checkbox>
              <v-flex xs12 sm6 md4>
               <v-menu
                 ref="meny"
                 :close-on-content-click="false"
                 v-model="meny"
                 :return-value.sync="date"
                 lazy
                 transition="scale-transition"
                 full-width
                 min-width="290px"
               >
                 <v-btn color="grey darken-1" flat slot="activator" class="pa-0 ma-0">
                   <v-icon class="pa-0 ma-0">event</v-icon>
                   <span class="subheading px-2" style="text-transform: none !important">Velg dato</span>
                 </v-btn>



               <!-- <v-checkbox

                 label="Velg dato"
                 v-model="date"
                 value="value"
                 readonly></v-checkbox> -->
                 <!-- <v-text-field
                   slot="activator"
                   v-model="date"
                   label="Picker without buttons"
                   prepend-icon="event"
                   readonly
                 ></v-text-field> -->
                 <v-date-picker xs12 v-model="date" @input="$refs.meny.save(date)"></v-date-picker>
               </v-menu>
             </v-flex>
             <v-card tile flat fluid v-if="date">
               <v-card-text class="text-xs-left subheading">
                   <p class="subheading" >Valgt dato: </p>
                   <p  ><span class="text-grey">{{ formatDato._i }}</span></p>
               </v-card-text>
             </v-card>

              <v-btn color="primary" @click="submit">send inn</v-btn>
            </v-form>
          </v-card-text>


    </v-card>
    </v-dialog>
  </v-layout>

</template>


<script>
import axios from 'axios'
import moment from 'moment'
import { mapState, mapMutations } from 'vuex'

export default {
  data() {
    return {
      sitat: '',
      beskrivelse: null,
      humoer_id: null,
      barn_id: 1,
      date: null,
      humoer: null,
      lokaliser: false,
      meny: false,
      navigatorGeolocation: null,
      dialog: false
    }
  },
  computed: {
    formatDato() {
      return moment(this.date)
    },
    ...mapState(['data'])
  },
  methods: {
    ...mapMutations(['SET_DATA']),
    submit () {
          // Native form submission is not yet supported
          axios.post('http://127.0.0.1:5000/api/sitat', {
            "sitat": this.sitat,
            "barn_id": this.barn_id,
            "humoer_id": this.humoer_id,
            "info": this.beskrivelse ? this.beskrivelse : null
          })
          .then((response) => {
            console.log(response, "dette er response")
            this.hentData()
            this.clear()
            this.dialog = false
          })
          .catch((error) => {
            console.log(error, "post data");
          })
      },
      hentData() {
        axios.get('http://127.0.0.1:5000/api/sitat')
        .then((response) => {
          console.log(response)
          const data = response.data.data.map((item) => {
              console.log(moment(item.creation_date));
              return {sitat: item.sitat, id: item.id, date: moment(item.creation_date), barn: item.barn_id, humoer: item.humoer_id, beskrivelse: item.info ? item.info : null}
            })
          this.SET_DATA(data)
      })
        .catch(error => (console.log(error, "hentdata")))
      },
    hentPosisjon(options) {
      return new Promise(function (resolve, reject) {
        navigator.geolocation.getCurrentPosition(resolve, reject, options);
      });
    },
    geolokaliser() {
      const options = {
        enableHighAccuracy: true,
        timeout: 5000,
        maximumAge: 0
      }
      this.hentPosisjon(options)
      .then((response) => {
          console.log(response);
      })
    },
    clear () {
      this.$refs.form.reset()
    },
  },
  created() {
      axios.get('http://127.0.0.1:5000/api/humoer')
      .then((response) => {
        this.humoer = response.data.data
      })
      if (navigator.geolocation) {
        this.navigatorGeolocation = true
      } else {
        this.navigatorGeolocation = false
      }
    }
}
</script>

<style lang="css" scoped>
.sidelinje {
  border-left: 5px solid rgb(145, 196, 218)
}
</style>
