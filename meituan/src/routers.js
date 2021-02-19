//导入的前提是用npm install安装了vue-router
import VueRouter from "vue-router"
import Vue from "vue"
import Home from "./components/Home"
import Order from "./components/Order/Order"
import Mine from "./components/Mine"
import Merchant from "./components/Merchant/Merchant"
import SubmitOrder from "./components/SubmitOrder"
import MTAddressList from "./components/MTAddressList"
import MTAddressEdit from "./components/MTAddressEdit"
import Login from "./components/Login"
import auth from "./utils/auth"

Vue.use(VueRouter)

const routes = [
  {
    path: "/", 
    component: Home,
    name: "home"
  },
  {
    path: "/order", 
    component: Order,
    name: "order",
    meta: {
      requireAuth: true
    }
  },
  {
    path: "/mine", 
    component: Mine,
    name: "mine",
    meta: {
      requireAuth: true
    }
  },
  {
    path: "/merchant/:merchant_id", 
    component: Merchant,
    name: "merchant"
  },
  {
    path: "/submitorder", 
    component: SubmitOrder,
    name: "submit_order",
    meta: {
      requireAuth: true
    }
  },
  {
    path: "/address", 
    component: MTAddressList,
    name: "mt_address_list",
    meta: {
      requireAuth: true
    }
  },
  {
    path: "/address/add", 
    component: MTAddressEdit,
    name: "mt_address_add",
    meta: {
      requireAuth: true
    }
  },
  {
    path: "/address/edit", 
    component: MTAddressEdit,
    name: "mt_address_edit",
    meta: {
      requireAuth: true
    }
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

router.beforeEach((to, from, next) => {
  if(to.meta.requireAuth && !auth.is_authenticated){
    next({
      "name": "login",
      "query": {
        "from": to.path
      }
    })
  }else{
    next()
  }
})

export default router;