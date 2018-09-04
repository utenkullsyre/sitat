<template lang="html">
  <section>
      <v-container grid-list-sm fill-height class="blue lighten-4 elevation-4" xs12>
        <v-layout row wrap>
          <v-flex xs12>
            <span class="display-1">Sitater</span> <add-sitat></add-sitat>
          </v-flex>
          <v-flex xs12 md6 xl4 v-for="i in data" fill-height>
            <v-card :key="i.id" fill-height class="mx-2">
              <v-card-title primary-title class="subheading">
                <v-layout row wrap justify-space-between >
                  <div class="">
                    <v-avatar
                      size="50"
                      color="red lighten-4"
                    >
                    <v-img
                      :src= "require('@/assets/' + i.humoer + '.png')"
                      alt="alt" contain></v-img>
                    </v-avatar>
                    <small class="headline grey--text lighten-3"> {{ i.barn == 1 ? 'Vinjar' : i.barn}}  </small>
                  </div>
                  <v-avatar
                  ripple
                  >
                    <v-icon @click="delItem(i.id)" large>close</v-icon>
                  </v-avatar>

                </v-layout>
              </v-card-title>
              <v-card-text class=" my-1 py-0">
                  <v-layout column wrap justify-start align-start class="pb-4">
                    <blockquote class="title pb-2 text-xs-left">
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
import AddSitat from '@/components/AddSitat.vue'
import axios from 'axios'
import moment from 'moment'
import { mapState, mapMutations } from 'vuex'

export default {
  name: 'Sitat',
  data() {
    return {
    }
  },
  computed: {
    ...mapState(['data']),
    formatDato() {
      return moment(this.date)
    }
  },
  components: {
    AddSitat
  },
  methods: {
    ...mapMutations(['SET_DATA']),
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
      hentData() {
        axios.get('http://127.0.0.1:5000/api/sitat')
        .then((response) => {
          console.log(response)
          const data = response.data.data.map((item) => {
              return {sitat: item.sitat, id: item.id, date: moment(item.creation_date), barn: item.barn_id, humoer: item.humoer_id, beskrivelse: item.info ? item.info : null}
            })
          this.SET_DATA(data)
      })
        .catch(error => (console.log(error, "hentdata")))
      }
    },
    created(){
      console.log("Skal fyrt av en mutat");
    this.hentData()
    console.log("Helvete");
  }
}
</script>

<style lang="css">
</style>
