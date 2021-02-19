<template>
<div class="addressedit-container">
  <mt-navbar arrowColor="#000" titleText="修改地址"></mt-navbar>
  <van-address-edit
    :area-list="areaList"
    show-postal
    show-delete
    show-set-default
    :address-info="addressInfo"
    :area-columns-placeholder="['请选择', '请选择', '请选择']"
    @save="onSave"
    @delete="onDelete"
  />
</div>
</template>

<script type="text/ecmascript-6">
import { AddressEdit } from 'vant';
import areaList from "../data/area";
import MTNavBar from "./Common/MTNavBar";
import Address from "@/utils/addressConverter";

export default {
  name: "MTAddressEdit",
  data(){
    return{
      areaList: areaList,
      addressInfo: {}
    }
  },
  components: {
    [AddressEdit.name]: AddressEdit,
    [MTNavBar.name]:MTNavBar
  },
  computed:{
    isEditing(){
      if(this.$route.name == 'mt_address_edit'){
        return true
      }else{
        return false
      }
    }
  },
  mounted(){
    if(this.isEditing){
      this.addressInfo = this.$store.state.editingAddress;
    }
  },
  methods: {
    onSave(content){
      const address = Address.convertToServer(content)
      if(!this.isEditing){
        this.$toast.loading()
        this.$http.addAddress(address).then(response => {
          console.log(response)
          this.$toast.close()
          this.$toast.success()
          this.$router.back()
        }).catch(e => {
          this.$toast.fail("保存失败，请稍候再试！")
          console.log(e)
        })
      }else{
        this.$toast.loading()
        this.$http.editAddress(this.addressInfo.id, address).then(response => {
          console.log(response)
          this.$toast.close()
          this.$toast.success()
          this.$router.back()
        }).catch(e => {
          this.$toast.fail("编辑失败，请稍候再试！")
          console.log(e)
        })
      }
    },
    onDelete(){

    }
  },
}
</script>

<style scoped lang="scss">

</style>