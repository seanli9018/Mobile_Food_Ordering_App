<style scoped lang="scss">
.logo-box{
  height: 200px;
  position: fixed;
  top: 0px;
  left: 0px;
  right: 0px;
  div{
    width: 80px;
    margin: 55px auto;
    img{
      width: 80px;
      height: 80px;
    }
  }
}
.login-detail{
  padding: 10px 18px;
  .button{
    margin-top: 20px;
  }
}
.van-cell-group{
  margin-top: 200px;
}
</style>

<template>
<div class="login-container">

  <div class="logo-box">
    <div>
      <img src="https://is4-ssl.mzstatic.com/image/thumb/Purple123/v4/42/e9/d6/42e9d6f1-db17-f691-2fbb-8013403276c2/AppIcon-0-0-1x_U007emarketing-0-0-0-7-0-0-sRGB-0-0-0-GLES2_U002c0-512MB-85-220-0-0.png/400x400.png" alt="">
    </div>
  </div>
  <div class="login-detail">
    <van-cell-group>
      <van-field v-model="tel" :required="required" size="large" placeholder="请输入手机号">
        <template #button>
          <van-button size="small" type="default" :disabled="smsCodeButtonDisabled" @click="sendSMSCode">{{sendText}}</van-button>
        </template>
      </van-field>
      <van-field v-model="smscode" size="large" placeholder="请输入短信验证码"></van-field>
    </van-cell-group>
    <div class="button">
      <van-button type="primary" size="large" :disabled="submitButtonDisabled" @click="onLogin">登录</van-button>
    </div>
  </div>
</div>
</template>

<script type="text/ecmascript-6">
import { CellGroup, Field, Button} from 'vant';
export default {
  name: "",
  data() {
    return {
      tel: '',
      smscode: '',
      required: true,
      sendText: "发送验证码",
      timeout: 0
    };
  },
  components: {
    [Field.name]:Field,
    [CellGroup.name]: CellGroup,
    [Button.name]: Button
  },
  computed:{
    smsCodeButtonDisabled(){
      if(!this.tel.match(/1[3456789]\d{9}/) || this.timeout>0){
        return true
      }else{
        return false
      }
    },
    submitButtonDisabled(){
      if(!this.tel.match(/1[3456789]\d{9}/) || !this.smscode.match(/\d{4}/)){
        return true
      }else{
        return false
      }
    }
  },
  methods:{
    sendSMSCode(){
      const telephone = this.tel
      const that = this;
      this.$http.getSMSCode(telephone).then(response => {
        this.$toast.success("验证码已发送！")
        console.log(response)
        that.timeout = 60;
        const interval = setInterval(()=>{
          that.timeout--;
          that.sendText = that.timeout + "s后重新发送"
          if(that.timeout==0){
            clearInterval(interval)
            that.sendText = "发送验证码"
          }
        }, 1000);
      }).catch(e => {
        console.log(e)
        this.$toast("验证码发送失败！")
      })
    },
    onLogin(){
      const telephone = this.tel
      const smscode = this.smscode
      this.$http.login({"telephone": telephone, "smscode": smscode}).then(response => {
        const data = response.data
        const user = data.user
        const token = data.token
        this.$auth.setUserToken(user, token)
        const from = this.$route.query['from']
        if(from){
          this.$router.push(from)
        }else{
          this.$router.replace('/')
        }
      }).catch(e => {
        console.log(e)
        this.$toast("登录失败！")
      })
    }
  }
}
</script>
