import {Loading } from 'element-ui'

class MTLoading {
  show(text=null){
    this.loading = Loading.service({
      fullscreen: true,
      spinner: "el-icon-loading",
      background: "rgba(255,255,255,0.7)",
      text: text?text:"正在加载中..."
    })
  }

  hide(){
    if(this.loading){
      this.loading.close()
    }
  }
}

export default new MTLoading