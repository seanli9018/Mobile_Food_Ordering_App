<template>
  <v-app id="inspire">
    <v-main>
      <v-container
        class="fill-height"
        fluid
      >
        <v-row
          align="center"
          justify="center"
        >
          <v-col
            cols="12"
            sm="8"
            md="6"
            lg="4"
          >
            <v-card class="elevation-12">
              <v-toolbar
                color="primary"
                dark
                flat
                class="title-bar"
              >
                <v-toolbar-title>后台管理系统登录</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form class="input-box" ref="loginForm" v-model="valid">
                  <v-text-field
                    label="手机号"
                    v-model="telephone"
                    prepend-icon="mdi-account"
                    type="text"
                    :rules="phoneRules"
                  ></v-text-field>

                  <v-text-field
                    id="password"
                    label="密码"
                    v-model="password"
                    prepend-icon="mdi-lock"
                    type="password"
                    :rules="passwordRules"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="onSubmit">登录</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script type="text/ecmascript-6">

export default {
  name: "Login",
  props: {
    //source: String,
  },
  data(){
    return{
      valid: true,
      telephone: '',
      phoneRules: [
        v => !!v || '手机号码不能为空',
        v => (/1[3456789]\d{9}/).test(v) || '请输入一个正确的手机号码'
      ],
      password: '',
      passwordRules: [
        v => !!v || '密码不能为空',
        v => (v.length >= 6 && v.length <= 20) || '密码长度在6位-20位之间'
      ]
    }
  },
  components: {

  },
  methods: {
    onSubmit(){
      if(!this.$refs.loginForm.validate()){
        console.log("验证失败");
      }
      else{
        const params = {
          username: this.telephone,
          password: this.password
        }
        // send axios(ajax) api request to server side.
        // and get server side api response data
        this.$loading.show()
        this.$http.login(params)
        .then(response => {
          const data = response.data;
          const user = data.user;
          const token = data.token;

          this.$auth.setUserToken(user, token)
          this.$router.push("/")
          this.$loading.hide()
        })
        .catch(e => {
            console.log(e);
            this.$loading.hide()
        })
      }
    }
  }
}
</script>

<style scoped lang="scss">
.v-toolbar__title{
  margin: 0 auto;
}
.v-card__text{
  padding: 25px;
}
.v-card__actions{
  padding: 0 25px 16px 0;
}
</style>