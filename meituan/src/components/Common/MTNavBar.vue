<template>
<div class="mt-navbar">
  <van-nav-bar @click-left="$router.back()" :title="titleText">
    <van-icon name="arrow-left" slot="left" :color="arrowColor"></van-icon>
  </van-nav-bar>
</div>
</template>

<script type="text/ecmascript-6">
import { NavBar, Icon } from "vant";
export default {
  name: "mt-navbar",
  props: {
    arrowColor:{
      type: String,
      default: "#fff"
    },
    titleText: {
      type: String,
      default: ""
    }
  },
  data(){
    return{
    }
  },
  components: {
    [NavBar.name]: NavBar,
    [Icon.name]: Icon
  }
}
</script>

<style scoped>
  .mt-navbar >>> .van-nav-bar{
    background: none;
  }
  .mt-navbar >>> .van-hairline--bottom::after{
    border: none;
  }
  /* .van-nav-bar >>> .van-icon{
    color: white;
  } */
</style>