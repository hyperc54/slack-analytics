<template>
    <div>
        Analytics
        <component :bus="bus" @askForData="askForData" v-bind:is="currentAnalyticsComponent"></component>
    </div>
</template>

<script>
import Vue from 'vue'
import Search from './Search.vue'
import Loading from './Loading.vue'
import Graphs from './Graphs.vue'
import axios from 'axios'

export var analyticsDetails = {
    chan_name: 'random',
    start_date: '20180701',
    nb_days: '3',
    g: new Object(),
    code: ''
};

export default {
  name: 'analytics',
  data: function () {
    return {
        analyticsDetails,
        currentAnalyticsComponent : 'search',
        bus: new Vue(),
    }
  },
  created: function(){
    var queryDict = {}
    window.location.hash.substr(1).split("?")[1].split("&").forEach(function(item) {queryDict[item.split("=")[0]] = item.split("=")[1]})
    this.analyticsDetails.code = queryDict['code']

    var url = "http://localhost:5000/api/auth/" + this.analyticsDetails.code

        axios({ method: "GET", "url": url }).then(result => {
            console.log(result);
        }, error => {
            console.error(error);
        });
  },
  methods: {
    askForData () {
        this.currentAnalyticsComponent = 'loading';

        var url = "http://localhost:5000/api/load/" +
            this.analyticsDetails.start_date + "/" +
            this.analyticsDetails.chan_name + "/" +
            this.analyticsDetails.nb_days + "/" +
            this.analyticsDetails.code

        axios({ method: "GET", "url": url }).then(result => {
            console.log(result);
            this.analyticsDetails.g = result.data;
            this.currentAnalyticsComponent = 'graphs';
            this.bus.$emit('plotnow');
        }, error => {
            console.error(error);
        });
    }
  },
  components: { Search, Loading, Graphs }
}
</script>
