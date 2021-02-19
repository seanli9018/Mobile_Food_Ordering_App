<style scoped lang="scss">
.good-container{
  position: absolute;
  top: 0;
  right: 0;
  left: 0;
  bottom: 0;
  z-index: 999;
  background-color: rgba(0,0,0,0.7);
  display: flex;
  justify-content: center;
  align-items: center;

  .middle-box{
    $middleBoxWidth: 331px;
    width: $middleBoxWidth;
    height: 450px;
    //background-color: pink;
    position: relative;
    .goods-detail-group{
      height: 368px;
      background-color: #fff;
      border-radius: 10px;
      overflow: hidden;
      padding:10px;
      .picture{
        width: 100%;
        height: 236px;
      }
      .month-sale{
        font-size: 12px;
        margin-top: 10px;
      }
      .intro{
        font-size: 14px;
        margin-top: 10px;
      }
      .price{
        font-size: 18px;
        margin-top: 10px;
        color: #fb4e44;
      }
    }
    .close-btn{
      height: 40px;
      width: 40px;
      //background-color: brown;
      position: absolute;
      bottom: 0px;
      left: ($middleBoxWidth - 30px) / 2;
      border-radius: 50%;
      background-image: url("http://s3plus.meituan.net/v1/mss_e2821d7f0cfe4ac1bf9202ecf9590e67/cdn-prod/file:9096d347/df125964473c5a2c4edadb74d8a11995.png");
      background-size: 40px;
      background-position: center;
    }
  }
}
</style>

<template>
<div class="good-container" v-show="show">
  <div class="middle-box">
    <div class="goods-detail-group">
      <img :src="goods.picture" alt="" class="picture">
      <div class="month-sale">月售10份</div>
      <div class="intro">{{goods.intro}}</div>
      <div class="price">￥{{goods.price}}</div>
    </div>
    <div class="close-btn" @click="closeClick"></div>
  </div>
</div>
</template>

<script type="text/ecmascript-6">
export default {
  //不是整个页面组件，是小组件所以用小写和-命名
  name: "goods-detail",
  props:{
    goods: {
      type: Object,
      default: function(){
        return {}
      }
    }
  },
  data(){
    return{
      show: false,
    }
  },
  watch: {
    goods(newValue, oldValue){
      if(newValue || oldValue){
        this.show = true;
      }
    }
  },
  components: {

  },
  methods: {
    closeClick(){
      this.show = false;
    }
  }
}
</script>
