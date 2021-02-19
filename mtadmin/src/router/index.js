import Vue from 'vue'
import VueRouter from 'vue-router'
import Frame from '../views/Frame.vue'
import Login from '../views/Login.vue'
import Index from '../components/Index'
import Merchant from '../components/Merchant'
import Order from '../components/Order'
import User from '../components/User'
import MerchantDetail from '../components/MerchantDetail'

Vue.use(VueRouter)

  const routes = [
    {
      path: "/", 
      component: Frame,
      children: [
        {path: "", component:Index, name: "index"},
        {path: "merchant", component:Merchant, name: "merchant"},
        {path: "order", component:Order, name: "order"},
        {path: "user", component:User, name: "user"},
        {path: "merchant_detail", component: MerchantDetail, name: "merchant_detail"}
      ]
    },
    {
      path: "/login", 
      component: Login,
      name: "login"
    },
]

const router = new VueRouter({
  routes: routes
})

router.afterEach(function(to,from){
  console.log('to:',to);
  console.log('from:',from);
})
export default router
