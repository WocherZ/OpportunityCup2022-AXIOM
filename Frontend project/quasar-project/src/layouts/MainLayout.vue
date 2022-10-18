<template>
  <q-layout view="lHh Lpr lFf row">
    <q-header>
      <div class="col-2 row justify-start items-center text-h3 text-weight-light text-white text-center">
        <q-btn class="col-grow row justify-start items-center q-pl-xl text-h3 text-weight-light" flat no-caps exact clickable to="/">
          <span style="color: #2c3e50"> SBER</span>
        </q-btn>

        <q-btn to="/transactions" @click="test" flat>
          <q-icon left size="3em" name="paid" />
          <div>Transactions</div>
        </q-btn>

        <q-btn to="/charts" flat>
          <q-icon left size="3em" name="bar_chart" />
          <div>Charts</div>
        </q-btn>

        <q-btn to="/patterns_guide" class="q-mr-md" flat>
          <q-icon left size="3em" name="help" />
          <div>Patterns guide</div>
        </q-btn>
      </div>
    </q-header>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { defineComponent, ref } from 'vue'

export default {
  name: 'MainLayout',
  data() {
    return {
      jsonData: null,

    }
  }

}
</script>
