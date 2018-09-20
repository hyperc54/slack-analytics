<template>
    <div>
        <h3>Your personal stats</h3>
        You posted {{ analyticsDetails.g.personal_stats.number_messages }} messages !
        That represents {{ analyticsDetails.g.personal_stats.number_words }} words !

        <h3>Top chatters</h3>
        <div id="graph-top-chatters"></div>

        <h3>Wordcloud</h3>
        <div id="graph-wordcloud"></div>
    </div>
</template>

<script>
import { analyticsDetails } from '@/components/Analytics.vue'

import Plotly from 'plotly.js/dist/plotly'

export default {
  name: 'graphs',
  props: ['bus'],
  data:function () {
    return {
        analyticsDetails
    }
  },
  methods: {
    plotBar () {
        console.log(this.analyticsDetails['g']);
        var TESTER = document.getElementById('graph-top-chatters');
        var key_values = Object.assign({}, this.analyticsDetails['g']['big_chatters']); //static copy of vue variable

        Plotly.plot( TESTER, [{
        x: Object.keys(key_values),
        y: Object.values(key_values),
        type: 'bar'}], {
        margin: { t: 0 } } );
    }
  },
  mounted() {
    this.bus.$on('plotnow', this.plotBar())
  }
}
</script>
