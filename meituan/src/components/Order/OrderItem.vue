<style scoped lang="scss">
  .order-detail{
    padding: 10px 18px 20px 18px;
    .order-info{
      display: flex;
      justify-content: space-between;
      .order-name{
        p{
          font-weight:700;
          font-size: 14px;
        }
        span{
          font-size: 10px;
          color: grey;
        }
      }
      .order-count{
        text-align: right;
      }
    }
    .order-control{
      display:flex;
      justify-content: space-between;
      padding-top: 18px;
      .order-status{
        font-size: 14px;
        color:grey;
        line-height: 30px;
      }
      .order-btn{
        .delete-btn{
          margin-right: 15px;
        }
      }
    }
  }
</style>
<template>
<div class="order-item-container">
  <van-cell-group :border="showBorder">
    <van-cell icon="shop-o" title="长沙麦当劳芙蓉中路餐厅" is-link />
  </van-cell-group>
  <div class="order-detail">
    <div class="order-info">
      <div class="order-name">
        <p>ZICO椰子水鸡翅下午茶</p>
        <span>07/05/2019 16:23</span>
      </div>
      <div class="order-count">
        <p>x1</p>
        <span>实付￥24.9</span>
      </div>
    </div>
    <div class="order-control">
      <div class="order-status">
        <span>订单已完成</span>
      </div>
      <div class="order-btn">
        <van-button type="default" size="small" class="delete-btn">删除</van-button>
        <van-button type="warning" size="small" class="add-btn">再来一单</van-button>
      </div>
    </div>
  </div>
</div>
</template>

<script type="text/ecmascript-6">
import { Cell, CellGroup, Button  } from 'vant'

export default {
  name: "order-item",
  data(){
    return{
      showBorder: false
    }
  },
  components: {
    [Cell.name]: Cell,
    [CellGroup.name]: CellGroup,
    [Button.name]: Button
  }
}
</script>
