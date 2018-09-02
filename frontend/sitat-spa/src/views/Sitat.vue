<template lang="html">
  <section>
    <v-container grid-list-sm xs12 sm8 md6 lg6 xl6>
        <v-container class="elevation-4">
          <v-form ref="form" @submit="submit">
            <h1 class="headline">Legg til sitat</h1>
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
                @change="geolokaliser"
               >
             </v-checkbox>

             <v-btn color="primary" @click="submit">send inn</v-btn>
           </v-form>
        </v-container>
        <v-divider></v-divider>
        <v-container grid-list-sm fill-height class="blue lighten-4 elevation-4" xs12>
          <v-layout row wrap reverse>
            <v-flex xs12>
              <span class="display-1">Sitater</span>
            </v-flex>
            <v-flex xs12 v-for="i in data" >
              <v-card :key="i.id">
                <v-card-title primary-title class="subheading">
                  <v-layout row wrap justify-space-between >
                    <div class="">
                      <v-avatar
                        size="50"
                      >
                      <v-img
                        :src= "require('@/assets/' + i.humoer + '.png')"
                        alt="alt" contain></v-img>
                      </v-avatar>
                      <small class="headline grey--text lighten-3"> {{ i.barn == 1 ? 'Vinjar' : i.barn}}  </small>
                    </div>
                      <v-btn color="transparent" flat @click="delItem(i.id)">
                        <v-icon color="grey">close</v-icon>
                      </v-btn>
                  </v-layout>
                </v-card-title>
                <v-card-text class="my-4">
                    <v-layout column wrap justify-start align-start class="mb-4">
                      <blockquote class="title pb-2">
                          &#8220;<span >{{ i.sitat }}</span>&#8221;
                        </blockquote>
                        <small>{{ i.date.date() }}/{{ i.date.month()+1 }}/{{ i.date.year() }}</small>
                    </v-layout>
                </v-card-text>

              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
    </v-container>

  </section>

</template>

<script>
import axios from 'axios'
import moment from 'moment'

export default {
  name: 'Sitat',
  data() {
    return {
      data:null,
      sitat: '',
      beskrivelse: null,
      humoer_id: null,
      barn_id: 1,
      humoer: null,
      lokaliser: false,
      navigatorGeolocation: null
    }
  },
  computed: {
  },
  methods: {
    submit () {
          // Native form submission is not yet supported
          axios.post('http://127.0.0.1:5000/api/sitat', {
            "sitat": this.sitat,
            "barn_id": this.barn_id,
            "humoer_id": this.humoer_id,
            "info": this.beskrivelse ? this.beskrivelse : null
          })
          .then((response) => {
            console.log(response)
            this.hentData()
            this.clear()
          })
          .catch((error) => {
            console.log(error, "post data");
          })
      },
      delItem (id) {
        console.log(id);
        axios.delete('http://127.0.0.1:5000/api/sitat', {
          data: {
            id: id
          }
        })
        .then((response) => {
          console.log(response)
          this.hentData()
        })
        .catch((error) => {
          console.log(error, "post data");
        })
      },
      clear () {
        this.$refs.form.reset()
      },
      hentData() {
        axios.get('http://127.0.0.1:5000/api/sitat')
        .then((response) => {
          console.log(response)
          this.data = response.data.data.map((item) => {
          console.log(moment(item.creation_date));
          return {sitat: item.sitat, id: item.id, date: moment(item.creation_date), barn: item.barn_id, humoer: item.humoer_id, beskrivelse: item.info ? item.info : null}
        })
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

    }

    },
    created(){
    this.hentData()
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

<style lang="css">
</style>
