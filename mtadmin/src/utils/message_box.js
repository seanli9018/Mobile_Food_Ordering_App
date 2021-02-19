import { MessageBox } from 'element-ui'

class MTMessageBox {
  confirm(message_text="是否确定该操作？", title="提示"){
    let options = {
      type: "warning"
    }
    return MessageBox.confirm(message_text, title, options)
  }

  alert(message_text="发生严重错误！", title="警告"){
    let options = {
      type: "error"
    }
    return MessageBox.alert(message_text, title, options)
  }
}

export default new MTMessageBox()