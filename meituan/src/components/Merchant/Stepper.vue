<style scoped lang="scss">
.stepper-container{
  display: flex;
  align-items: center;
  .substract{
    background-image: url("../../assets/substract.png");
  }
  .add{
    background-image: url("http://s3plus.meituan.net/v1/mss_e2821d7f0cfe4ac1bf9202ecf9590e67/cdn-prod/file:9096d347/318c525df8eba9c557594305c44b2ddf.png");
  }
  .step-btn{
    width: 45px;
    height: 45px;
    border-radius: 50%;
    background-position: center;
    background-repeat: no-repeat;
    background-size: 50%;
    display: inline-block;
  }
}
</style>

<template>
<div class="stepper-container">
  <span class="substract step-btn" v-show="value>0" @click.stop="substractClick"></span>
  <span class="text" v-show="value>0">{{value}}</span>
  <span class="add step-btn" @click.stop="addClick"></span>
</div>
</template>

<script type="text/ecmascript-6">
export default {
  name: "stepper",
  props: {
    value: {
      type: Number,
      default: 0
    }
  },
  model:{
    prop: "value",
    event: "value-changed"
  },
  data(){
    return{
      //value: 0
    }
  },
  components: {

  },
  methods: {
    substractClick(){
      //this.value -= 1
      this.$emit("value-changed", this.value-1)
    },
    addClick(){
      //this.value += 1
      this.$emit("value-changed", this.value+1)
    }
  }
}
</script>
