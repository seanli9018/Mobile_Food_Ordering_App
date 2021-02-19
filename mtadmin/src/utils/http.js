import auth from './auth'
import router from '../router/index'
import axios from 'axios'

const BASE_URL = 'http://127.0.0.1:8000'

class Http {
  constructor(){
    this.http = axios.create({
      baseURL: BASE_URL,
      timeout: 5000
    });

    //请求拦截器，发送任何请求之前都会执行这一个函数。
    // 这样我们就能实时获取到登录用户的token了
    this.http.interceptors.request.use(config => {
      const token = auth.token
      if(token){
        config.headers.common.Authorization = "JWT " + token
      }
      return config
    })

    //响应拦截器，接收到response之后，会执行这一个函数
    this.http.interceptors.response.use(response => {
      return response
    }, error => {
      if(error == 403){
        auth.clearUserToken()
        router.replace('/login')
        this.$message.error("请重新登录！")
      } else if(error == 400){
        this.$message.error("表格填写有误，请按照规范填写！")
      }else{
        this.$message.error("错误500，服务器错误！")
      }
      return Promise.reject(error)
    })
  }

  login(params) {
    const url = "/cms/login"
    return this.http.post(url, params)
  }

  getMerchants(page=1){
    const url = "/cms/merchant?page="+page
    return this.http.get(url)
  }

  addMerchant(data){
    const url = "/cms/merchant"
    return this.http.post(url, data)
  }

  uploadPicture(file){
    const url = "/cms/upload"
    return this.http.post(url, file)
  }
  
  getMerchant(merchant_id){
    const url = "cms/merchant/" + merchant_id
    return this.http.get(url) 
  }

  editMerchant(merchant_id, data){
    const url = "cms/merchant/" + merchant_id
    return this.http.put(url, data) 
  }

  getCategories(merchant_id){
    const url = "cms/category/merchant/" + merchant_id
    return this.http.get(url)
  }

  editCategory(category_id, data){
    const url = "cms/category/" + category_id
    return this.http.put(url, data)
  }

  addCategory(data){
    const url = "cms/category"
    return this.http.post(url, data)
  }

  deleteCategory(category_id){
    const url = "cms/category/" + category_id
    return this.http.delete(url)
  }

  addGoods(data){
    const url = "cms/goods"
    return this.http.post(url, data)
  }

  editGoods(goods_id, data){
    const url = "cms/goods/" + goods_id
    return this.http.put(url, data)
  }

  deleteGoods(goods_id){
    const url = "cms/goods/" + goods_id
    return this.http.delete(url)
  }
}

export default new Http()