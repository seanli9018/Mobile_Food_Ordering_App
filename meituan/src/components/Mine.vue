<style scoped lang="scss">
  .avatar{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 200px;
    background-color: gold;
    .middle-box{
      margin: 55px auto;
      width: 80px;
      img{
        width: 80px;
        height: 80px;
        border-radius: 50%;
      }
      .username{
        text-align: center;
        font-size: 16px;
        font-weight: 700;
        margin-top: 10px;
      }
    }
  }
  .van-cell-group {
    margin-top: 200px;
  }
</style>
<template>
<div class="profile-container">
  <div class="avatar">
    <div class="middle-box">
      <img src="https://www.yxwoo.com/uploads/images/xiaz/2020/0407/1586223138482.jpg" alt="">
      <div class="username">Sean Li</div>
    </div>
  </div>
  <van-cell-group :border="showBorder"> 
    <van-cell title="我的红包" is-link :border="showBorder"/>
    <van-cell title="收货地址" is-link :border="showBorder"/>
    <van-cell title="常见问题" is-link :border="showBorder"/>
    <van-cell title="协议与说明" is-link :border="showBorder"/>
    <van-cell title="退出登录" is-link :border="showBorder"/>
  </van-cell-group>
</div>
</template>

<script type="text/ecmascript-6">
import { Cell, CellGroup } from 'vant';
export default {
  name: "Mine",
  data(){
    return{
      showBorder: false
    }
  },
  components: {
    [Cell.name]: Cell,
    [CellGroup.name]: CellGroup
  }
}
</script>
