import { Message } from "element-ui"

class MTMessage{
  constructor(){
    this.config = {
      duration: 2000,
      center: false,
      showClose: true,
    }
  }
  show(){
    Message(JSON.parse(JSON.stringify(this.config)))
  }
  success(message_text="恭喜，操作成功"){
    this.config.message = message_text
    this.config.type = "success"
    this.show()
  }

  info(message_text=""){
    this.config.message = message_text
    this.config.type = "info"
    this.show()
  }

  warning(message_text=""){
    this.config.message = message_text
    this.config.type = "warning"
    this.show()
  }
  
  error(message_text="操作失败！"){
    this.config.message = message_text
    this.config.type = "error"
    this.show()
  }
}

const message = new MTMessage()
export default message