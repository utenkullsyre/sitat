<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <add-sitat></add-sitat>
  </div>
</template>

<script>
// @ is an alias to /src
import HelloWorld from '@/components/HelloWorld.vue'
import AddSitat from '@/components/AddSitat.vue'

export default {
  name: 'home',
  components: {
    HelloWorld, AddSitat
  }
}
</script>
