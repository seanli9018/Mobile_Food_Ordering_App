<template>
<div class="index-container">
    这是首页
    <el-button type="primary">测试按钮</el-button>
    <el-button type="warning">测试按钮</el-button>
</div>
</template>

<script type="text/ecmascript-6">
import {Button} from 'element-ui'
export default {
    name: "Index",
    data(){
        return{

        }
    },
    components: {
        [Button.name]: Button
    }
}
</script>

<style scoped lang="scss">

</style>