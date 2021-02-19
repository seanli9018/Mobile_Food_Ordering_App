<template>
  <v-container>
    <h1>商家列表</h1>
    <v-row>
      <v-col cols="12" lg="2" md="3" sm="6" xs="12" v-if="page==1">
        <router-link to="/merchant_detail" class="text-decoration-none"> 
          <v-card>
            <v-img
              src="https://img.icons8.com/carbon-copy/2x/plus.png"
              class="white--text align-end"
              height="200px"
            >
            </v-img>
            <v-card-title>
              添加商家
            </v-card-title>
          </v-card>
        </router-link>
      </v-col>
      <v-col cols="12" lg="2" md="3" sm="6" xs="12" v-for="merchant in merchants" :key="merchant.id">
        <router-link :to="'/merchant_detail?id='+merchant.id" class="text-decoration-none">
          <v-card>
            <v-img
              :src="merchant.logo"
              class="white--text align-end"
              height="200px"
            >
            </v-img>
            <v-card-title v-text="merchant.name">
            </v-card-title>
          </v-card>
        </router-link>
      </v-col>
    </v-row>
    <div class="text-center">
      <v-pagination 
        v-model="page"
        :length="total_page"
        :total-visible="5"
        @input="onCurrentChange"
      ></v-pagination>
    </div>
  </v-container>
</template>

<script type="text/ecmascript-6">
export default {
  name: "Index",
  data(){
      return{
        merchants:{},
        page: 1,
        total_page: 0,
      }
  },
  components: {

  },
  mounted(){
    this.getMerchants(1)
  },
  methods: {
    onCurrentChange(page){
      this.getMerchants(page)
    },
    getMerchants(page){
      this.$loading.show()
      this.$http.getMerchants(page)
      .then(response => {
        this.merchants = response.data.results
        this.total_page = response.data.total_pages
        this.$loading.hide()
      })
      .catch(e => {
        console.log(e);
        this.$loading.hide()
      })
    },
  }
}
</script>

<style scoped lang="scss">
</style>