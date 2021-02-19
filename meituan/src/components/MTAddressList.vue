<template>
<div class="addresslist-container">
  <mt-navbar arrowColor="#000" titleText="地址管理"></mt-navbar>
  <van-address-list
    v-model="chosenAddressId"
    :list="list"
    :disabled-list="disabledList"
    disabled-text="以下地址超出配送范围"
    default-tag-text="默认"
    @add="onAdd"
    @edit="onEdit"
    @select="onSelect"
  />
</div>
</template>

<script type="text/ecmascript-6">
import { AddressList } from 'vant';
import MTNavBar from "./Common/MTNavBar";
import Address from "@/utils/addressConverter";

export default {
  name: "MTAddressList",
  data(){
    return {
      chosenAddressId: '1',
      list: [],
      disabledList: [
        {
          id: '3',
          name: '王五',
          tel: '1320000000',
          address: '浙江省杭州市滨江区江南大道 15 号',
        },
      ],
    };
  },
  components: {
    [AddressList.name]: AddressList,
    [MTNavBar.name]: MTNavBar,
  },
  mounted(){
    this.$http.getAddressList().then(response => {
      let addressList = response.data
      for(let index=0; index<addressList.length;index++){
        if(addressList[index].is_default){
          this.chosenAddressId = addressList[index].id
        }
        this.list.push(Address.convertToFront(addressList[index]))
      }
      const selectedAddress = this.$store.state.selectedAddress
      if(selectedAddress){
        this.chosenAddressId = selectedAddress.id
      }
    }).catch(e => {
      console.log(e)
      this.$toast.fail("加载地址失败，请稍候再试！")
    })
  },
  methods: {
    onAdd(){
      this.$router.push("./address/add")
    },
    onEdit(item){
      this.$router.push("./address/edit")
      this.$store.commit('setEditingAddress', item)
    },
    onSelect(item){
      this.$store.commit('setSelectedAddress', item)
      this.$router.back()
    }
  }
}
</script>

<style scoped lang="scss">

</style>