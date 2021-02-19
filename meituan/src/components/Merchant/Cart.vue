<style scoped lang="scss">
.cart-container{
  .bg-mask{
    position: fixed;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: rgba(0,0,0,0.7);
    z-index:3;
  }
  .cart-group{
    z-index:3;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    .delivery-limit{
      height: 20px;
      line-height: 20px;
      text-align: center;
      background-color: #fff1d0;
    }
    .cart-info{
      .cart-clean{
        height: 28px;
        line-height: 28px;
        background-color:gainsboro;
        display: flex;
        justify-content: space-between;
        span{
          padding: 0 8px;
        }
      }
      .cart-items{
        .cart-li{
          height: 45px;
          line-height: 45px;
          background-color: #fff;
          display: flex;
          justify-content: space-between;
          .item-name{
              font-size: 16px;
              font-weight: 700;
              padding-left: 8px;
            }
          .item-info{
            display:flex;
            .item-price{
              font-size: 14px;
              color: #FB4E44;
            }
          }
        }
      }
    }
    .cart-bottom{
      height: 45px;
      line-height: 45px;
      display: flex;
      .hot-area{
        background-color: #3b3b3c;
        font-size: 16px;
        font-weight: 700;
        flex: 1;
        display: flex;
        .shop-icon{
          width: 45px;
          margin-right: 18px;
          position: relative;
          img{
            width: 100%;
            padding-left: 8px;
            margin-top: -10px;
          }
          .badage{
            width: 16px;
            height: 16px;
            font-size: 10px;
            background-color: red;
            color: #fff;
            border-radius: 50%;
            position: absolute;
            text-align: center;
            line-height: 16px;
            right: -8px;
            top: -8px;
          }
        }
        .total-price{
          .text{
            color:#fff;
          }
        }
      }
      .pay-btn{
        width: 90px;
        font-size: 16px;
        text-align: center;
        background-color: #f8c74e;
      }
    }
  }
}
</style>

<template>
<div class="cart-container" v-show="show">
  <div class="bg-mask" v-show="cartShow" @click="cartShow=false">
  </div>
  <div class="cart-group">
    <div class="delivery-limit">
      已满足起送价
    </div>
    <div class="cart-info" v-show="cartShow">
      <div class="cart-clean">
        <span>购物车</span>
        <span class="clean-cart" @click="clearCart"><i class="iconfont icon-delete"></i>清空购物车</span>
      </div>
      <ul class="cart-items" v-for="item in items" :key="item.name">
        <li class="cart-li">
          <div class="item-name">
            {{item.name}}
          </div>
          <div class="item-info">
            <div class="item-price">
              ￥ {{item.price}}
            </div>
            <div class="item-stepper">
              <stepper v-model="item.count"></stepper>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <div class="cart-bottom">
      <div class="hot-area" @click="cartShowClick">
        <div class="shop-icon">
          <img src="http://s3plus.meituan.net/v1/mss_e2821d7f0cfe4ac1bf9202ecf9590e67/cdn-prod/file:9096d347/03098cb323a0263fdbbb102c696433c5.png" alt="">
          <div class="badage"><span>{{totalCount}}</span></div>
        </div>
        <div class="total-price">
          <span class="text">￥{{totalPrice}}</span>
        </div>
      </div>
      <div class="pay-btn" @click="gotoSettle"> 
        <span>去结算</span>
      </div>
    </div>
  </div>
</div>
</template>

<script type="text/ecmascript-6">
import Stepper from "./Stepper";

export default {
  name: "cart",
  props: ["categories"],
  data(){
    return{
      cartShow: false
    }
  },
  components: {
    [Stepper.name]: Stepper
  },
  computed:{
    show: function(){
      if(this.items.length>0){
        return true
      }else{
        return false
      }
    },
    items: function(){
      const selected_items = []
      for(let category of this.categories){
        for(let item of category.goods_list){
          if(item.count > 0){
            selected_items.push(item)
          }
        }
      }
      return selected_items
    },
    totalPrice: function(){
      let total = 0
      for(let item of this.items){
        total += (parseFloat(item.price)) * item.count
      }
      return total
    },
    totalCount: function(){
      let total_count = 0
      for(let item of this.items){
        total_count += item.count
      }
      return total_count
    }
  },
  methods:{
    cartShowClick(){
      this.cartShow=!this.cartShow;
    },
    clearCart(){
      for(let category of this.categories){
        for(let item of category.goods_list){
          item.count = 0
        }
      }
    },
    gotoSettle(){
      this.$store.commit("setCart",this.items)
      this.$router.push("/submitorder")
    }
  },
  watch: {
    show: function(val){
      if(val==false){
        this.cartShow = false
      }
    }
  }
}
</script>
