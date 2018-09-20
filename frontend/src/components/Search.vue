<template>
    <div>
        <form id="search" novalidate class="md-layout">
            <md-card class="md-layout-item md-size-50 md-small-size-100" style="margin:auto">
                <md-card-header>
                    <div class="md-title">What do you want</div>
                </md-card-header>
                <md-card-content>
                    <div class="md-layout md-gutter">
                        <!-- Chan -->
                        <div class="md-layout-item md-small-size-100">
                            <md-field>
                                <label for="chan_name">Nom du chan</label>
                                <md-input name="chan_name" id="chan_name" placeholder="Chan name, ex: chan-cool" v-model="analyticsDetails.chan_name"/>
                            </md-field>
                        </div>
                    </div>

                        <!-- datestart -->
                        <div class="md-layout-item md-small-size-100">
                            <md-field>
                                <label for="start_date">Start date</label>
                                <md-input name="start_date" id="start_date" placeholder="Start date, ex: YYYY-MM-DD" v-model="analyticsDetails.start_date"/>
                            </md-field>
                        </div>
                        <!-- Nb days -->
                        <div class="md-layout-item md-small-size-100">
                            <md-field>
                                <label for="nb_days">Number of days</label>
                                <md-input name="nb_days" id="nb_days" placeholder="Number of days: X" v-model="analyticsDetails.nb_days"/>
                            </md-field>
                        </div>
                </md-card-content>
                <md-card-actions>
                    <md-button v-on:click="askForData" class="md-primary">Gogogo</md-button>
                </md-card-actions>
            </md-card>
        </form>
    </div>
</template>

<script>
import Vue from 'vue'

import { MdCard } from 'vue-material/dist/components'
import 'vue-material/dist/theme/default.css'
import 'vue-material/dist/vue-material.min.css'

import { analyticsDetails } from '@/components/Analytics.vue'

Vue.use(MdCard)

export default {
  name: 'search',
  data:function () {
    return {
        analyticsDetails
    }
  },
  methods: {
    askForData: function () {
      this.$emit('askForData')
    }
  }
}
</script>
