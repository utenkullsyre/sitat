<template lang="html">
  <section>
    <div class="">
      <h1>Helvete</h1>

    </div>
    <v-container>
      <v-form ref="form" @submit="submit">
         <v-text-field
           v-model="sitat"
           label="Sitat"
           box
           required
         ></v-text-field>
         <v-btn
           @click="submit"
         >
           submit
         </v-btn>
       </v-form>
    </v-container>
    <v-container grid-list-sm fill-height>
      <v-layout row wrap reverse>
        <v-flex xs12 v-for="i in data" >
          <v-card :key="i.id">
            <v-card-title primary-title class="headline">
              {{ i.id }}
            </v-card-title>
            <p>Sitat: <span class="subheading">{{ i.sitat }}</span></p>
            <p>Dato: <span>{{ i.date }}</span></p>
            <v-btn color="primary" @click="delItem(i.id)">Delete</v-btn>
          </v-card>
        </v-flex>
      </v-layout>
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
      sitat: ''
    }
  },
  methods: {
    submit () {
          // Native form submission is not yet supported
          axios.post('http://127.0.0.1:5000/api/sitat', {
            "sitat": this.sitat,
            "barn_id": 1,
            "humoer_id": 0
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
        this.data = response.data.data.map((item) => {
          console.log(moment(item.creation_date));
          return {sitat: item.sitat, id: item.id, date: moment(item.creation_date)}
        })
      })
        .catch(error => (console.log(error, "hentdata")))
      }

    },
  mounted(){
    this.hentData()
  }
}
</script>

<style lang="css">
</style>
