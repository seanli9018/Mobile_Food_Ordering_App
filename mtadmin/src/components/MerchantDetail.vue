<template>
    <v-container fluid>
      <h1>商家详情</h1>
      <v-row style="width: 600px">
        <v-col cols="12">
          <v-tabs v-model="tab">
            <v-tab>基本信息</v-tab>
            <v-tab>商品管理</v-tab>
          </v-tabs>
          <v-tabs-items v-model="tab">
            <v-tab-item>
              <v-card flat>
                <v-card-text>
                  <v-form
                    ref="merchant_form"
                    v-model="merchant_valid"
                    lazy-validation
                    id="merchant-form"
                    @submit.prevent="onSubmit"
                  >
                    <v-text-field
                      v-model="merchantForm.name"
                      :rules="merchantRules.name"
                      label="店铺名称"
                      required
                    ></v-text-field>

                    <v-text-field
                      v-model="merchantForm.address"
                      :rules="merchantRules.address"
                      label="店铺地址"
                      required
                    ></v-text-field>

                    <v-file-input
                      label="店铺图片上传"
                      accept="image/png, image/jpeg"
                      :rules="merchantRules.picture"
                      prepend-icon="mdi-camera"
                      @change="onPictureChange"
                      @click:clear="clearMerchantLogo"
                    >
                    </v-file-input>
                    <v-text-field
                      v-model="merchantForm.logo"
                      v-if="!1"
                    ></v-text-field>
                    <img :src="merchantForm.logo" v-if="merchantForm.logo" alt="" class="logo"/>

                    <v-text-field
                      v-model="merchantForm.lon"
                      :rules="merchantRules.lon"
                      label="店铺经度"
                      type="number"
                      required
                    ></v-text-field>

                    <v-text-field
                      v-model="merchantForm.lat"
                      :rules="merchantRules.lat"
                      label="店铺纬度"
                      type="number"
                      required
                    ></v-text-field>

                    <v-text-field
                      v-model="merchantForm.notice"
                      :rules="merchantRules.notice"
                      label="店铺公告"
                    ></v-text-field>

                    <v-text-field
                      v-model="merchantForm.up_send"
                      :rules="merchantRules.up_send"
                      label="起送价格"
                    ></v-text-field>

                    <v-btn
                      :disabled="!merchant_valid"
                      color="primary"
                      class="mr-4"
                      type="submit"
                      form="merchant-form"
                    >
                      提交商家信息
                    </v-btn>
                  </v-form>
                </v-card-text>
              </v-card>
            </v-tab-item>
            <v-tab-item>
              <v-card flat>
                <v-card-text>
                  <v-list>
                    <v-list-group
                      v-for="(category, index) in categories"
                      :key="category.name"
                      prepend-icon="mdi-food-fork-drink"
                      no-action
                    >
                      <template v-slot:activator>
                        <v-list-item-content>
                          <v-list-item-title v-text="category.name"></v-list-item-title>
                        </v-list-item-content>
                        <v-btn depressed small color="primary" class="category-btn" @click.stop="onCategoryEdit(category)">编辑</v-btn>
                        <v-btn depressed small color="error" class="category-btn" @click.stop="onCategoryDelete(category, index)">删除</v-btn>
                      </template>

                      <v-list-item
                        v-for="(goods, index) in category.goods_list"
                        :key="goods.name"
                        class="goods_items"
                      >
                        <v-list-item-content>
                          <v-list-item-title v-text="goods.name"></v-list-item-title>
                        </v-list-item-content>
                        <v-btn depressed small outlined color="primary" class="goods-btn" @click.prevent="onGoodsEdit(goods)">编辑</v-btn>
                        <v-btn depressed small outlined color="primary" class="goods-btn btn-right" @click.stop="onGoodsDelete(goods, index)">删除</v-btn>
                      </v-list-item>
                      <v-list-item>
                        <v-list-item-content>
                          <v-btn outlined color="primary" @click.prevent="onGoodsAdd(category.id)" ><v-icon left>mdi-plus</v-icon>新增商品</v-btn>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list-group>
                    <v-list-item>
                      <v-list-item-content>
                         <v-btn outlined color="primary" @click.prevent="onCategoryAdd()" ><v-icon left>mdi-plus</v-icon>新增分类</v-btn>
                      </v-list-item-content>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
            </v-tab-item>
          </v-tabs-items>
        </v-col>
      </v-row>
      <v-dialog v-model="categoryDialog" persistent max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">新增/编辑分类</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-form id="categoryEditForm" :v-model="category_validate" ref="category_form">
                    <v-text-field label="分类名称*" v-model="categoryForm.name" :rules="categoryRules.name" required></v-text-field>
                  </v-form>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="categoryDialog = false">取消</v-btn>
            <v-btn color="blue darken-1" text @click="onCategorySubmit">确认</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
      <v-dialog v-model="goodsDialog" persistent max-width="600px">
        <v-card>
          <v-card-title>
            <span class="headline">新增/编辑商品</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-form id="goodsEditForm" :v-model="goods_validate" ref="goods_form">
                    <v-text-field label="商品名称*" v-model="goodsForm.name" :rules="goodsRules.name" required></v-text-field>
                    <v-file-input label="商品图片*" v-model="goodsPicInput" accept="image/png, image/jpeg" 
                    :rules="goodsRules.picture" @change="onPictureChange" 
                    @click:clear="clearGoodsPicture" required></v-file-input>
                    <v-text-field v-model="goodsForm.picture" v-if="goodsForm.picture" disabled></v-text-field>
                    <img :src="goodsForm.picture" v-if="goodsForm.picture" alt="" class="goods_picture"/>
                    <v-text-field label="商品价格*" v-model="goodsForm.price" :rules="goodsRules.price" required></v-text-field>
                    <v-text-field label="商品介绍*" v-model="goodsForm.intro" :rules="goodsRules.intro" required></v-text-field>
                  </v-form>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="blue darken-1" text @click="goodsDialog = false">取消</v-btn>
            <v-btn color="blue darken-1" text @click="onGoodsSubmit">确认</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-container>
</template>

<script type="text/ecmascript-6">

export default {
  name: "MerchantDetail",
  data(){
    return{
      merchant_id: null,
      tab: null,
      merchant_valid: true,
      merchantForm: {
        name: '',
        address: '',
        logo: '',
        lon: null,
        lat: null,
        notice: '',
        up_send: 0.00
      },
      merchantRules: {
        name:[
          v => !!v || '店铺名称必填',
          v => (v.length >= 2 && v.length <= 20) || '店铺名称需要大于1个字符，小于20个字符',
        ],
        address: [
          v => !!v || '店铺地址必填',
        ],
        picture: [
          value => (!!value || !!this.merchantForm.logo) || '必须上传图片',
          value => !value || /(.*?)\.(png|jpe?g)/.test(value.name.toLowerCase()) || "必须为jpg，或者png格式",
          value => !value || value.size < 2097152 || '图片文件必须小于2M!'
        ],
        lon: [
          v => !!v || '店铺经度必填',
        ],
        lat: [
          v => !!v || '店铺纬度必填',
        ],
        notice: [
          v => !v || v.length >= 2 && v.length <= 40 || '店铺公告需要大于1个字符，小于40个字符',
        ],
        up_send: [
          v => !!v || '起送价格必填！',
          v => /^\d*(\.\d{0,2})?$/.test(v) || '必须填入价格，最小到小数点后两位！',
          v => (v <= 200) || '起送价格不能超过200元！',
        ],
      },
      categories: [],
      categoryDialog: false,
      category_validate: true,
      categoryForm: {
        id: null,
        name: '',
        merchant_id: null
      },
      categoryRules: {
        name: [
          v => !!v || '分类名称必填',
          v => (v.length >= 2 && v.length <= 20) || '分类名称需要大于1个字符，小于20个字符',
        ]
      },
      goodsDialog: false,
      goods_validate: true,
      goodsPicInput: null,
      goodsForm: {
        id: null,
        name: '',
        picture: '',
        price: null,
        intro: '',
        category_id: null
      },
      goodsRules: {
        name: [
          v => !!v || '商品名称必填',
          v => (v.length >= 2 && v.length <= 20) || '商品名称需要大于1个字符，小于20个字符',
        ],
        price: [
          v => !!v || '商品价格必填',
          v => /^\d*(\.\d{0,2})?$/.test(v) || '只能填入商品价格，最小到小数点后两位！'
        ],
        intro: [
          v => !!v || '商品介绍必填',
          v => (v.length == 0 || (v.length >= 2 && v.length <= 40)) || '商品描述需要大于1个字符，小于40个字符',
        ],
        picture: [
          value => !!value || !!this.goodsForm.picture || '必须上传图片',
          value => !value || /(.*?)\.(png|jpe?g)/.test(value.name.toLowerCase()) || "必须为jpg，或者png格式",
          value => !value || value.size < 2097152 || '图片文件必须小于2M!'
        ]
      }
    }
  },
  components: {

  },
  mounted(){
    this.merchant_id = this.$route.query.id
    if(this.merchant_id){
      this.$loading.show()
      this.$http.getMerchant(this.merchant_id).then(response => {
        const merchant = response.data
        this.merchantForm.name = merchant.name
        this.merchantForm.address = merchant.address
        this.merchantForm.logo = merchant.logo
        this.merchantForm.lon = merchant.lon
        this.merchantForm.lat = merchant.lat
        this.merchantForm.notice = merchant.notice
        this.merchantForm.up_send = merchant.up_send
      }).catch(e => {
        this.$message.error("数据加载失败！错误：" + e)
        this.$loading.hide()
      })

      this.$http.getCategories(this.merchant_id).then(response => {
        this.categories = response.data
        console.log(response.data);
        this.$loading.hide()
      }).catch(e => {
        this.$message.error("操作失败！错误：" + e)
        this.$loading.hide()
      })
    }
  },
  methods: {
    initCategoryForm(){
      this.categoryForm = {
        id: null,
        name: '',
        merchant_id: null
      }
    },
    initGoodsForm(){
      this.goodsForm = {
        id: null,
        name: '',
        picture: '',
        price: null,
        intro: '',
        category_id: null
      }
      this.goodsPicInput = null
    },
    onSubmit () {
      if(this.$refs.merchant_form.validate()){
        this.$loading.show()
        this.sendMerchantData(this.merchantForm);
      }else{
        this.$message.error("表格填写不正确！无法提交")
      }
    },
    sendMerchantData(formData){
      if(!this.merchant_id){
        this.$http.addMerchant(formData).then(response => {
          this.$router.push({"name":"merchant"})
          this.$loading.hide()
          console.log(response);
        }).catch(e => {
          this.$message.error("操作失败！错误：" + e)
          this.$loading.hide()
        })
      }else{
        this.$http.editMerchant(this.merchant_id, formData).then(response => {
          this.$router.push({"name":"merchant"})
          this.$loading.hide()
          console.log(response);
        }).catch(e => {
          this.$message.error("操作失败！错误：" + e)
          this.$loading.hide()
        })
      }
    },
    onPictureChange(file) {
      if(!file){
        this.$message.error("必须上传图片!")
      }else{
        const isImage = file.type ==='image/jpeg' || file.type === 'image/png';
        const isUnder2M = file.size/1024/1024 < 2;
        if(!isImage){
          this.$message.error("必须上传图片格式的文件")
        }else if(!isUnder2M){
          this.$message.error("文件必须小于2M!")
        }else{
          if(this.goodsDialog){
            const is_goods = true
            this.sendPicture(file, is_goods)
          }else{
            const is_goods = false
            this.sendPicture(file, is_goods)
          }
        }
      }
    },
    sendPicture(file, is_goods){
      let fileData = new FormData
      fileData.append('file', file)
      this.$loading.show()
      this.$http.uploadPicture(fileData).then(response => {
        is_goods?this.goodsForm.picture=response.data.picture:this.merchantForm.logo=response.data.picture
        this.$loading.hide()
      }).catch(e => {
        this.$message.error("操作失败！错误：" + e)
        this.$loading.hide()
      })
    },
    clearGoodsPicture(){
      this.goodsForm.picture = ''
    },
    clearMerchantLogo(){
      this.merchantForm.logo = ''
    },
    onCategoryEdit(category){
      this.categoryForm = {
        id: category.id,
        name: category.name,
        merchant_id: category.merchant_id
      }
      this.categoryDialog = true
    },
    onCategorySubmit(){
      if(this.$refs.category_form.validate()){
        this.$loading.show()
        if(this.categoryForm.id){
          this.$http.editCategory(this.categoryForm.id, this.categoryForm).then(response => {
            this.categoryDialog = false
            console.log(response)
            this.$message.success()
            for(let category of this.categories){
              if (category.id == this.categoryForm.id){
                category.name = this.categoryForm.name
                break
              }
            }
            this.$loading.hide()
          }).catch(e => {
            this.$message.error("操作失败！错误：" + e)
            this.$loading.hide()
          })
        }else {
          this.categoryForm.merchant_id = this.merchant_id
          this.$http.addCategory(this.categoryForm)
          .then(response => {
            this.categoryDialog = false
            this.$message.success("分类添加成功！")
            this.categories.push(response.data)
            this.$loading.hide()
          }).catch(e => {
            this.$message.error("操作失败！错误：" + e)
            this.$loading.hide()
          })
        }
      }else{
        this.$message.error("表格填写不正确！无法提交")
      }
    },
    onCategoryAdd(){
      this.initCategoryForm();
      this.categoryDialog = true
    },
    onCategoryDelete(category, index){
      if(category.goods_list.length > 0){
        this.$message.error("该分类下还有商品，无法直接删除！")
        return
      }
      this.$http.deleteCategory(category.id).then(response => {
        console.log(response);
        this.$message.success("删除分类成功！")
        this.categories.splice(index,1)
      }).catch(e => {
        this.$message.error("操作失败！错误：" + e)
      })
    },
    onGoodsAdd(category_id){
      this.initGoodsForm();
      this.goodsForm.category_id = category_id
      this.goodsDialog = true
    },
    onGoodsSubmit(){
      if(this.$refs.goods_form.validate()){
        this.$loading.show()
        if(this.goodsForm.id){
          this.$http.editGoods(this.goodsForm.id, this.goodsForm).then(response => {
            console.log(response);
            this.$message.success("商品修改成功！")
            this.goodsDialog = false
            for (let category of this.categories){
              for (let goods of category.goods_list){
                if(response.data.id == goods.id){
                  goods.name = response.data.name
                  goods.intro = response.data.intro
                  goods.picture = response.data.picture
                  goods.price = response.data.price
                  this.$loading.hide()
                  return
                }
              }
            }
          }).catch(e => {
            this.$message.error("商品修改失败，错误：" + e)
            this.$loading.hide()
          })
        }else{
          this.$http.addGoods(this.goodsForm).then(response => {
            this.goodsDialog = false
            this.$message.success("商品添加成功！")
            for (let category of this.categories){
              if(response.data.category_id == category.id){
                category.goods_list.push(response.data)
                break
              }
            }
            this.$loading.hide()
          }).catch(e => {
            this.$loading.hide()
            this.$message.error("操作失败！请检查表格是否填写正确！" + e)
          })
        }
      }else{
        this.$message.error("表格填写不正确！无法提交")
      }
    },
    onGoodsEdit(goods){
      this.goodsForm = {
        id: goods.id,
        name: goods.name,
        picture: goods.picture,
        price: goods.price,
        intro: goods.intro,
        category_id: goods.category_id
      }
      this.goodsDialog = true
    },
    onGoodsDelete(goods, index){
      this.$messageBox.confirm().then(()=>{
        // if confirm btn clicked
        this.$http.deleteGoods(goods.id).then(response => {
          console.log(response);
          this.$message.success("删除商品成功！")
          for (let category of this.categories){
            if(goods.category_id == category.id){
              category.goods_list.splice(index, 1)
              break
            }
          }
        }).catch(e => {
          this.$message.error("删除商品失败！错误：" + e)
        })
      }).catch(() => {
        // if cancel or close btn clicked
        this.$message.success("操作已取消。")
      })
    }
  }
}
</script>

<style scoped lang="scss">
.logo{
  width: 178px;
  height: 133px;
  background-color: #ccc;
}
.goods-btn{
  margin-left: 10px;
}
.category-btn{
  margin-left: 10px;
}
.btn-right{
  margin-right: 48px;
}
.goods_picture{
  width: 178px;
  height: 133px;
  background-color: #ccc;
}
</style>

<style scoped>
  .goods_items >>> .v-list-item__content {
    color: rgba(0,0,0,.54);
}
</style>