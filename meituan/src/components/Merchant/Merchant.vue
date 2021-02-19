<!-----------------------scss--------------------->
<style scoped lang="scss">
  .header-group{
    background-color: #2e2f3b;
    padding: 10px;
    display: flex;
    margin-top: -46px;
    padding-top: 46px;

    .logo{
      width: 85px;
      height: 64px;
    }
    .merchant-info{
      flex: 1;
      margin-left: 10px;
      color: #fff;
      display: flex;
      flex-direction: column;
      justify-content: space-around;
      overflow: hidden;
      .notice{
        //实现文字超过长度，隐藏，并且加上...
        text-overflow: ellipsis;
        white-space: nowrap;
        overflow: hidden;
      }
    }
  }
  .tab-group{
    .menu-group{
      display: flex;
      .category-group{
        width: 80px;
        text-align: center;
        height: 100%;
        overflow: hidden;
        .category-list{
          li{
            height: 50px;
            line-height: 50px;
            &.active{
              background-color: #ccc;
            }
          }
        }
      }
      .goods-group{
        flex: 1;
        margin-left: 10px;
        //background-color: olive;
        overflow: hidden;
        height: 100%;
        .goods-list{
          .category-name{
            font-size: 12px;
            height: 32px;
            line-height: 32px;
          }
          .goods-item{
            display: flex;
            height: 75px;
            .thumbnail{
              width: 75px;
            }
            .goods-info{
              flex:1;
              margin-left: 10px;
              display: flex;
              flex-direction: column;
              justify-content: space-around;
              .goods-name{
                font-size: 16px;
                font-weight: 700;
              }
              
              .goods-info-bottom{
                display: flex;
                justify-content: space-between;
                align-items: center;
                .price{
                  color: #fb4e44;
                  font-size: 16px;
                  font-weight: 700;
                }
              }
            }
          }
        }
      }
    }
  }
</style>

<!-----------------------html--------------------->
<template>
<div class="merchant-container">
  <mt-navbar></mt-navbar>
  <div class="header-group">
    <img :src="merchant.logo" alt="" class="logo">
    <div class="merchant-info">
      <div class="delivery-info">
        <span>20分钟</span> | <span>1km</span>
      </div>
      <div class="notice">
        公告：{{ merchant.notice }}
      </div>
    </div>
  </div>
  <van-tabs v-model="active" class="tab-group">
    <van-tab title="点菜">
      <div class="menu-group" :style="menuHeightStyle">
        <div class="category-group" ref="category">
          <ul class="category-list">
            <li v-for="(category,index) in categories" :key="category.name" @click="categoryClick(index)" 
            :class="index==currentIndex?'active':''">
             {{category.name}}
            </li>
          </ul>
        </div>
        <div class="goods-group" ref="goods">
          <!--下面多加一层空的div是因为，better-scroller需要在最外层的下一层是一个整体包装-->
          <div class="dl-wrapper">
            <dl class="goods-list" v-for="(category, category_index) in categories" :key="category.name">
              <dt class="category-name">{{category.name}}</dt>
              <dd class="goods-item" v-for="(goods, goods_index) in category.goods_list" :key="goods.id" 
              @click="goodsClick(category_index, goods_index)">
                <img :src="goods.picture" alt="" class="thumbnail">
                <div class="goods-info">
                  <div class="goods-name">{{goods.name}}</div>
                  <div class="month-sale">月售10份</div>
                  <div class="goods-info-bottom">
                    <div class="price">￥ {{goods.price}}</div>
                    <stepper v-model="goods.count"></stepper>
                  </div>
                </div>
              </dd>
            </dl>
          </div>
        </div>
      </div>
    </van-tab>
    <van-tab title="评价">
      评价页面
    </van-tab>
    <van-tab title="商家">
      商家页面
    </van-tab>
  </van-tabs>
  <goods-detail :goods="detailGoods"></goods-detail>
  <cart :categories="categories"></cart>
</div>
</template>

<!-----------------------JS--------------------->
<script type="text/ecmascript-6">
import { Tab, Tabs } from "vant";
import BScroll from "better-scroll";
import GoodsDetail from "./GoodsDetail";
import Stepper from "./Stepper";
import Cart from "./Cart";
import MTNavBar from "../Common/MTNavBar"

export default {
  name: "Merchant",
  data(){
    return{
      active: 0,
      categories: [],
      positions: [],
      currentIndex: 0,
      //在undefined的时候，这个detailGood不会传值给绑定的GoodsDetail小组件
      detailGoods: undefined,
      merchant: {}
    }
  },
  components: {
    [MTNavBar.name]: MTNavBar,
    [Tab.name]: Tab,
    [Tabs.name]: Tabs,
    [GoodsDetail.name]: GoodsDetail,
    [Stepper.name]: Stepper,
    [Cart.name]: Cart
  },
  computed: {
    menuHeightStyle(){
      const height = window.innerHeight - 164;
      return {
        height: height + "px"
      }
    }
  },
  mounted(){
    this.$nextTick(() => {
      //如果不用箭头函数，this是不能用的。必须要用that传进来
      this.menuScroller = new BScroll(this.$refs.category, {
        scrollY: true,
        click: true
      })
      this.goodsScroller = new BScroll(this.$refs.goods, {
        scrollY: true,
        click: true,
        //一定要设置probeType为2才能实时监听scroll事件
        probeType: 2
      })
      this.goodsScroller.on("scroll", (pos)=>{
        const y = Math.abs(pos.y);
        const positions = this.positions;
        for (let index = positions.length-1; index>=0; index--){
          if(y >= positions[index]){
            this.currentIndex = index;
            break
          }
        }
      })
    })
    const merchant_id = this.$route.params.merchant_id
    this.$http.getMerchant(merchant_id).then(response => {
      this.merchant = response.data
    }).catch(e => {
      console.log(e)
    })
    this.$http.getCategories(merchant_id).then(response => {
      const categories = response.data
      for(let category of categories){
        for(let goods of category.goods_list){
          goods.count = 0
        }
      }
      this.categories = categories
      this.$nextTick(() => {
        const positions = [0];
        let offset = 0;
        const goodsList = document.getElementsByClassName("goods-list");
        // for...in...:用来循环对象
        // for...of...:用来循环数组
        for(let dl of goodsList){
          const height = dl.clientHeight;
          offset += height;
          positions.push(offset)
        }
        this.positions = positions;
        this.menuScroller.refresh();
        this.goodsScroller.refresh();
      })
    }).catch(e => {
      console.log(e)
    })
  },
  methods: {
    categoryClick(index){
      const position = this.positions[index];
      this.goodsScroller.scrollTo(0, -position, 500)
      this.currentIndex = index
    },
    goodsClick(category_index, goods_index){
      let category = this.categories[category_index]
      let goods = category.goods_list[goods_index]
      this.detailGoods = JSON.parse(JSON.stringify(goods));
    }
  }
}
</script>
