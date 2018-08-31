<template lang="html">
  <section>
    <div class="">
      <h1>Humør</h1>
    </div>
    <v-container>
      <v-form ref="form" @submit="submit">
         <v-text-field
           v-model="humoer"
           label="Humør"
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
            <p>Sitat: <span class="subheading">{{ i.navn }}</span></p>
            <v-btn color="primary" @click="delItem(i.id)">Delete</v-btn>
          </v-card>
        </v-flex>
      </v-layout>
    </v-container>
  </section>

</template>

<script>
import axios from 'axios'
export default {
  name: 'Humoer',
  data() {
    return {
      data: null,
      humoer: ''
    }
  },
  methods: {
    submit () {
          // Native form submission is not yet supported
          axios.post('http://127.0.0.1:5000/api/humoer', {
              "navn": this.humoer
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
        axios.delete('http://127.0.0.1:5000/api/humoer', {
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
        axios.get('http://127.0.0.1:5000/api/humoer')
        .then(response => (this.data = response.data.data))
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
