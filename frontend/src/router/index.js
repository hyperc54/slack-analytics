import Vue from 'vue'
import Router from 'vue-router'
import Welcome from '@/components/Welcome.vue'
import Analytics from '@/components/Analytics.vue'
import NotFound from '@/components/NotFound.vue'


Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Welcome',
      component: Welcome
    },
    {
      path: '/analytics',
      name: 'analytics',
      component: Analytics
    },
    {
      path: '*',
      name: 'notfound',
      component: NotFound
    }
  ]
})
