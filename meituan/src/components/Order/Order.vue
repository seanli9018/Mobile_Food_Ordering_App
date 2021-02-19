<template>
<div class="order-container">
  <order-item></order-item>
  <order-item></order-item>
  <order-item></order-item>
</div>
</template>

<script type="text/ecmascript-6">
import OrderItem from "./OrderItem"
export default {
  name: "Order",
  data(){
    return{

    }
  },
  components: {
    [OrderItem.name]:OrderItem
  }
}
</script>

<style scoped lang="scss">

</style>