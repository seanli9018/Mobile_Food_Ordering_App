<template>
  <div id="app">
    <router-view></router-view>
    <van-tabbar v-model="active" active-color="#1c1B20" v-if="showTabbar">
      <van-tabbar-item icon="home-o" to="/">首页</van-tabbar-item>
      <van-tabbar-item icon="orders-o" to="/order" dot>订单</van-tabbar-item>
      <van-tabbar-item icon="user-o" to="/mine">我的</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script>
//import Home from "./components/Home.vue";
import { Tabbar, TabbarItem } from 'vant';

export default {
  name: 'App',
  data(){
    return{
      active: 0
    }
  },
  components: {
    //Home: Home,
    [Tabbar.name]: Tabbar,
    [TabbarItem.name]: TabbarItem
  },
  computed:{
    showTabbar(){
      const name = this.$route.name
      if(name=='home' || name=='order' || name=='mine'){
        return true
      } else{
        return false
      }
    }
  }
}
</script>

<style lang="scss">
  @import "./styles/init.css";
  .van-search{
    padding: 0px;
  }
</style>
<style scoped>
  .van-tabbar-item >>> .van-tabbar-item__text{
    font-size: 16px;
  }
</style>
