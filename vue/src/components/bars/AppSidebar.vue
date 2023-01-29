<template>
  <div class="app-sidebar">
    <router-link class="brand flex-column justify-center" to="/">
      <span class="brand-text">reactive design</span>
      <span class="sub-text block">.system /> </span></router-link>
    <nav>
      <div class="part" v-if="team">
<!--        <h3 class="title flex align-center">invoices</h3>-->
        <div class="part-content">
          <router-link class="ab__item flex align-center" :to="{name:'ProjectList', query:this.$route.query}" active-class="active">物件</router-link>
          <router-link class="ab__item flex align-center" :to="{name:'Invoice', query:this.$route.query}" active-class="active">見積書</router-link>
          <router-link class="ab__item flex align-center" :to="{name:'TotalInvoice',query:this.$route.query}" active-class="active">合計表</router-link>
          <router-link class="ab__item flex align-center" :to="{name:'CustomInvoice', query:this.$route.query}" active-class="active">カスタム見積書 </router-link>
        </div>
      </div>
    </nav>
  </div>
</template>

<script>
import useStates from "@/helpers/useStates";
export default {
  name: "AppSidebar",
  setup(){
    const {team} = useStates()
    return{
      team
    }
  }
}
</script>

<style scoped>
.app-sidebar {
  width: 244px;
  min-width: 244px;
  height: 100%;
  background-color: #10171e;
}
.app-sidebar > a.brand {
  color: #f1f1f1;
  padding: 14px;
  height: 54px;
  font-size: 1rem;
  line-height: 1;
  margin-bottom: 20px;
}
.app-sidebar > a.brand span.brand-text {
  letter-spacing: 1px;
}
.app-sidebar > a.brand span.sub-text {
  font-size: .64rem;
  color: #e74c3c;
  margin-top: 4px;
}

.app-sidebar > nav .part {
  margin-bottom: 10px;
}
.app-sidebar > nav .part h3.title {
  padding: 0 14px;
  height: 20px;
  font-size: .7rem;
  color: #6ca8da;
  font-weight: 400;
}
.app-sidebar > nav .part .part-content {
  height: auto;
  max-height: 200px;
}
.app-sidebar > nav .part .part-content a.ab__item {
  padding: 0 0 0 14px;
  height: 40px;
  max-height: 200px;
  color: #f1f1f1;
  opacity: .7;
  font-weight: 300;
  font-size: 1.4rem;
}
.app-sidebar > nav .part .part-content a.ab__item.active {
  color: #f1f1f1;
  background-color: rgba(255, 0, 140, 0.28);
  opacity: 1;
}
</style>