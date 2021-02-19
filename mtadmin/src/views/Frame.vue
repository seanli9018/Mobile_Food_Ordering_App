<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      :clipped="$vuetify.breakpoint.lgAndUp"
      app
    >
      <v-list dense>
        <v-list-item-group 
          v-model="active"
          color="indigo"
        >
          <v-list-item
            v-for="(item, i) in items"
            :key="i"
            :to=item.to
          >
            <v-list-item-action>
              <v-icon>{{ item.icon }}</v-icon>
            </v-list-item-action>
            <v-list-item-content>
              <v-list-item-title>
                {{ item.text }}
              </v-list-item-title>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar
      :clipped-left="$vuetify.breakpoint.lgAndUp"
      app
      color="blue darken-3"
      dark
    >
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title
        style="width: 300px"
        class="ml-0 pl-4"
      >
        <span class="hidden-sm-and-down">后台管理系统</span>
      </v-toolbar-title>
      <v-text-field
        flat
        solo-inverted
        hide-details
        prepend-inner-icon="mdi-magnify"
        label="Search"
        class="hidden-sm-and-down"
      ></v-text-field>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-apps</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-bell</v-icon>
      </v-btn>
      <v-btn
        icon
        large
        @click="toggleProfileSetting"
      >
        <v-avatar
          size="32px"
          item
        >
          <v-img
            src="https://cdn.vuetifyjs.com/images/logos/logo.svg"
            alt="Vuetify"
          ></v-img>
        </v-avatar>
        <div class="profile-setting-box" v-if="ProfileRendering" v-show="ProfileToggle" @click.stop>
          <span class="username-text">{{$auth.user.username}}</span>
          <a href="#">我的页面</a>
          <a href="#" @click.prevent="onLogout">退出登录</a>
        </div>
      </v-btn>
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
    <v-btn
      bottom
      color="pink"
      dark
      fab
      fixed
      right
      @click="dialog = !dialog"
    >
      <v-icon>mdi-plus</v-icon>
    </v-btn>
    <v-dialog
      v-model="dialog"
      width="800px"
    >
      <v-card>
        <v-card-title class="grey darken-2">
          Create contact
        </v-card-title>
        <v-container>
          <v-row class="mx-2">
            <v-col
              class="align-center justify-space-between"
              cols="12"
            >
              <v-row
                align="center"
                class="mr-0"
              >
                <v-avatar
                  size="40px"
                  class="mx-3"
                >
                  <img
                    src="//ssl.gstatic.com/s2/oz/images/sge/grey_silhouette.png"
                    alt=""
                  >
                </v-avatar>
                <v-text-field
                  placeholder="Name"
                ></v-text-field>
              </v-row>
            </v-col>
            <v-col cols="6">
              <v-text-field
                prepend-icon="mdi-account-card-details-outline"
                placeholder="Company"
              ></v-text-field>
            </v-col>
            <v-col cols="6">
              <v-text-field
                placeholder="Job title"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                prepend-icon="mdi-mail"
                placeholder="Email"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                type="tel"
                prepend-icon="mdi-phone"
                placeholder="(000) 000 - 0000"
              ></v-text-field>
            </v-col>
            <v-col cols="12">
              <v-text-field
                prepend-icon="mdi-text"
                placeholder="Notes"
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
        <v-card-actions>
          <v-btn
            text
            color="primary"
          >More</v-btn>
          <v-spacer></v-spacer>
          <v-btn
            text
            color="primary"
            @click="dialog = false"
          >Cancel</v-btn>
          <v-btn
            text
            @click="dialog = false"
          >Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script type="text/ecmascript-6">
export default {
  name: "Frame",
  props: {
    source: String,
  },
  data: () => ({
    dialog: false,
    drawer: null,
    activeItem: 0,
    active: 0,
    items: [
      { icon: 'mdi-home', text: '首页', to: "/" },
      { icon: 'mdi-storefront', text: '商家', to: "merchant" },
      { icon: 'mdi-account-multiple', text: '用户', to: "user" },
      { icon: 'mdi-clipboard-text', text: '订单', to: "order"}
    ],
    ProfileToggle: false,
  }),
  methods:{
    toggleProfileSetting(){
      this.ProfileToggle = !this.ProfileToggle;
    },
    onLogout(){
      this.$auth.clearUserToken();
      this.$router.replace({name: 'login'});
    },
  },
  computed:{
    ProfileRendering(){
      if(this.$auth.user){
        return true
      }
      return false
    }
  }
}
</script>

<style scoped lang="scss">
.profile-setting-box{
  width: 150px;
  flex-direction: column;
  display: flex;
  position: absolute;
  top: 54px;
  right: 0px;
  border: 1px solid #ccc;
  text-transform: none;
  background-color: #fff;
  a{
    text-decoration: none;
    padding: 5px 0;
  }
  .username-text{
    color: rgba(0, 0, 0, 0.87);
    font-size:0.8rem;
    padding: 5px 0;
    cursor: auto;
  }
}
</style>