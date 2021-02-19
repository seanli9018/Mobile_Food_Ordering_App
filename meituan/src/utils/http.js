import auth from './auth'
import router from '../routers'
import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:8000'

class Http {
  constructor(){
    //在构造函数里, init一个axios实例
    this.http = axios.create({
      baseURL: BASE_URL,
      timeout: 10000
    });

    // 请求拦截器，发送任何请求之前都会执行这一个函数。
    // 这样我们就能实时获取到登录用户的token了
    // 发送任何请求到服务器的时候，header里面都会带着"JWT jk34nc89fs678fsdfsd"
    // 以便后台视图有authentication_classes，和permission_classes需要
    this.http.interceptors.request.use(config => {
      const token = auth.token
      if(token){
        config.headers.common.Authorization = "JWT " + token
      }
      return config
    });

    // 响应拦截器，接收到response之后，会执行这一个函数
    this.http.interceptors.response.use(null, error => {
      if(error == 403){
        auth.clearUserToken()
        router.replace('/login')
        console.log("请重新登录！")
      }
      return Promise.reject(error)
    })
  }

  login(data) {
    const url = "/login"
    return this.http.post(url, data)
  }

  getSMSCode(telephone){
    const url = "/smscode?tel=" + telephone
    return this.http.get(url)
  }

  getMerchants(page){
    const url = "/merchants?page=" + page
    return this.http.get(url)
  }

  searchMerchants(keyword){
    const url = "/merchants/search?search=" + keyword
    return this.http.get(url)
  }

  getMerchant(merchant_id){
    const url = "/merchant/" + merchant_id
    return this.http.get(url)
  }

  getCategories(merchant_id){
    const url = "category/merchant/" +merchant_id
    return this.http.get(url)
  }

  addAddress(address){
    const url = "/address"
    return this.http.post(url, address)
  }

  getAddressList(){
    const url = "/address"
    return this.http.get(url)
  }

  editAddress(address_id, address){
    const url = '/address/' + address_id
    return this.http.put(url, address)
  }

  getDefaultAddress(){
    const url = '/address/default'
    return this.http.get(url)
  }

  submitOrder(data){
    const url = '/submitorder'
    return this.http.post(url, data)
  }
}

export default new Http()