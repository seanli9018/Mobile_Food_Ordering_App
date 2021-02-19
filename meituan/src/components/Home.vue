<!--template, script, style-->

<style scoped>
/* 因为这是修改vant 组件里面的样式，所以只能用css，不能用scss
而且组件里面的样式传递格式必须是 父元素>>>目标元素 的方式才能有效 */
  .van-dropdown-menu >>> .van-dropdown-menu__title{
    font-size: 16px;
    color:#767676;
  }
  .van-dropdown-menu__item{
    font-size: 16px;
    color:#767676;
  }
</style>

<style scoped lang="scss">
.header-group{
  background-color: #1c1B20;
  padding: 20px 15px 10px 15px;
  .address-group{
    color: #fff;
    font-size: 18px;
    font-weight: 700;
    i{
      font-size:18px;
    }
  }
  .search-group{
    margin-top: 10px;
  }
}

.main-group{
  h2{
    padding: 20px 10px 10px;
  }
  overflow: hidden;
  .merchant-list{
    .merchant-item{
      padding: 10px;
      display: flex;
      .logo{
        width: 85px;
        height: 64px;
      }
      .merchant-info{
        margin-left: 5px;
        .merchant-name{
          font-size: 16px;
          font-weight: 700;
        }
        .rate-group{
          padding-top: 5px;
        }
        .tag-group{
          padding-top: 5px;
          span{
            margin-right: 3px;
          }
        }
      }
    }
  }
}
</style>

<template>
<div class="home-container">
  <div class="header-group">
    <div class="address-group">
      <i class="iconfont icon-dingwei-xianxing"></i>
      <span class="address">三里屯</span>
      <i class="iconfont icon-iconfonti"></i>
    </div>
    <div class="search-group">
      <van-search v-model="value" @input="onInput" @clear="onClear" placeholder="请输入搜索关键词"/>
    </div>
  </div>
  <div class="main-group" ref="main" :style="mainHeightStyle">
    <div>
      <h2>附近商家</h2>
      <van-dropdown-menu>
        <van-dropdown-item v-model="sort" :options="sorts"></van-dropdown-item>
        <div class="van-dropdown-menu__item">距离最近</div>
        <div class="van-dropdown-menu__item">品质联盟</div>
        <div class="van-dropdown-menu__item">筛选<i class="iconfont icon-filter"></i></div>
      </van-dropdown-menu>
      <div class="merchant-list" v-for="merchant in merchantList" :key="merchant.name">
        <router-link :to="'/merchant/'+ merchant.id">
          <div class="merchant-item">
            <img :src="merchant.logo" alt="logo" class="logo">
            <div class="merchant-info">
              <div class="merchant-name">{{ merchant.name }}</div>
              <div class="rate-group">
                <van-rate v-model="rate" size="12px"></van-rate>
              </div>
              <div class="tag-group">
                <van-tag plain>美团专送</van-tag>
                <van-tag plain>炸鸡薯条</van-tag>
              </div>
            </div>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</div>
</template>

<script type="text/ecmascript-6">
import { Search, DropdownMenu, DropdownItem, Rate, Tag } from 'vant';
import BScroll from "better-scroll";

export default {
  name: "Home",
  data(){
    return{
      sort: 0,
      sorts: [
        { text: '综合排序', value: 0 },
        { text: '好评优先', value: 1 },
        { text: '距离最近', value: 2 },
        { text: '销量最高', value: 3 },
      ],
      rate: 9,
      merchants: [],
      scroller: null,
      page: 1,
      total_pages: 1,
      value: null,
      fn: null,
      searchResults: []
    }
  },
  components: {
    [Search.name]: Search,
    [DropdownMenu.name]: DropdownMenu,
    [DropdownItem.name]: DropdownItem,
    [Rate.name]:Rate,
    [Tag.name]:Tag
  },
  computed: {
    mainHeightStyle(){
      const occupiedHeight = 115 + 50
      const phoneHeight = 667
      const mainHeight = phoneHeight - occupiedHeight
      const mainRem = mainHeight / 37.5
      return {"height": mainRem+"rem"}
    },
    merchantList(){
      if(this.searchResults.length > 0){
        return this.searchResults
      }else{
        return this.merchants
      }
    }
  },
  mounted() {
    this.scroll = new BScroll(this.$refs.main,{
      scrollY: true,
      click: true,
      //上拉滚动加载
      pullUpLoad: {
        threshold: 0
      }
    })
    this.scroll.on("pullingUp", ()=>{
      this.loadMerchantData(this.page+1)
    })
    this.loadMerchantData(1)
  },
  methods: {
    loadMerchantData(page){
      if(page <= this.total_pages){
        this.$http.getMerchants(page).then(response => {
          if(response.data && response.data.results && response.data.results.length > 0){
            this.page = page
            this.total_pages = response.data.total_pages
            const data = response.data.results
            this.merchants = this.merchants.concat(data)
          }
          this.scroll.refresh()
          this.scroll.finishPullUp()
        }).catch(e => {
          console.log(e)
          this.$toast.fail('获取商家信息失败，请稍候再试！')
        })
      }
    },
    debounce(fnArg){
      let timer = null
      return function(value){
        clearTimeout(timer)
        timer = setTimeout(() => {
          fnArg(value)
        }, 500)
      }
    },
    onInput(value) {
      if(!this.fn){
        this.fn = this.debounce((valueArg) => {
          //console.log(valueArg)
          if(valueArg){
            this.$http.searchMerchants(valueArg).then(response => {
              this.searchResults = response.data
            }).catch(e => {
              console.log(e)
              this.$toast.fail('获取商家信息失败，请稍候再试！')
            })
          }else{
            this.searchResults = []
          }
        })
      }
      this.fn(value)
    },
    onClear(){
      this.searchResults = []
    }
  }
}
</script>

