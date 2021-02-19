<style scoped lang="scss">
.goods-group{
  padding: 10px;
  display: flex;
  justify-content: space-between;
  background-color: #F8F8F8;
  .thumbnail-group{
    width: 55px;
    height: 55px;
    min-width: 55px;
    img{
      width: 100%;
      height: 100%;
    }
  }
  .info-group{
    flex: 1;
    padding-left: 10px;
    .title-group{
      display: flex;
      justify-content: space-between;
      font-size: 14px;
      color: #333;
    }
  }
}
.submit-bar{
  position: fixed;
  right: 0;
  left: 0;
  bottom: 0;
  height: 50px;
}
</style>
<style scoped>
  .van-cell >>> .van-cell__title{
    font-size: 12px;
  }
</style>
<template>
<div class="submit-container">
  <mt-navbar arrowColor="#000" titleText="确认订单"></mt-navbar>
  <van-cell-group>
    <van-cell title="请选择送餐地址" icon="location-o" is-link to="/address">
      <template slot="title" v-if="address">
        <div class="user-info">
          {{address.name}} | {{address.tel}}
        </div>
        <div class="address">
          {{address.province}}{{address.city}}{{address.county}}{{address.addressDetail}}
        </div>
      </template> 
    </van-cell>
  </van-cell-group>
  <van-cell-group title="肯德基" border>
    <van-cell v-for="goods in goodsList" :key="goods.name">
      <template slot="title">
        <div class="goods-group">
          <div class="thumbnail-group">
            <img :src="goods.picture" alt="">
          </div>
          <div class="info-group">
            <div class="title-group">
              <span>{{goods.name}}</span>
              <span>￥{{goods.price}}</span>
            </div>
            <div class="number">份*{{goods.count}}</div>
          </div>
        </div>
      </template> 
    </van-cell>
  </van-cell-group>
  <div class="submit-bar">
    <van-submit-bar :price="totalPrice" button-text="提交订单" @submit="onSubmit" />
  </div>
</div>
</template>

<script type="text/ecmascript-6">
import MTNavBar from "./Common/MTNavBar";
import { Cell, CellGroup, SubmitBar } from 'vant';
import Address from "@/utils/addressConverter";

export default {
  name: "SubmitOrder",
  data(){
    return{
      goodsList:[],
      address: {}
    }
  },
  computed: {
    totalPrice(){
      let total = 0
      for(let goods of this.goodsList){
        total += goods.price*goods.count
      }
      return total*100
    }
  },
  mounted(){
    this.goodsList = this.$store.state.cart
    const selectedAddress = this.$store.state.selectedAddress
    if(selectedAddress){
      this.address = selectedAddress
    }else {
      this.$http.getDefaultAddress().then(response => {
        this.address = Address.convertToFront(response.data)
      }).catch(e => {
        console.log(e)
        this.$toast.fail("获取地址失败，请稍候再试！")
      })
    }
  },
  components: {
    [MTNavBar.name]: MTNavBar,
    [Cell.name]: Cell,
    [CellGroup.name]: CellGroup,
    [SubmitBar.name]: SubmitBar
  },
  methods: {
    onSubmit(){
      const goods_list = []
      for (let goods of this.goodsList){
        goods_list.push(goods.id)
      }
      this.$http.submitOrder({
        goods_id_list: goods_list,
        address_id: this.address.id
      }).then(response => {
        console.log(response.data)
        const pay_url = response.data
        window.location = pay_url
      }).catch(e => {
        console.log(e)
      })
    }
  }
}
</script>
