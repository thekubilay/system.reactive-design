<template>
  <header class="app-bar flex justify-space-between column-1">
    <h2 class="title flex align-center"></h2>
    <div class="user-content flex align-center">
      <button class="signout flex align-center" @click="signout()">ログアウト</button>
    </div>
  </header>
</template>

<script>
import {useRoute} from 'vue-router'

export default {
  name: "AppBar",
  setup() {
    const route = useRoute()
    const signout = () => {
      window.location = "https://system.reactive-design.com/accounts/logout/"
    }
    return {
      route,
      signout,
    }
  }
}
</script>

<style scoped>
.app-bar {
  height: 44px;
}

.app-bar > h2.title {
  padding: 0 14px;
  height: 100%;
  font-weight: 500;
  font-size: 1.2rem;
}

.app-bar > .user-content {
  height: 100%;
  padding: 0 14px;
}

.app-bar > .user-content > button.signout {
  width: 70px;
  height: 100%;
  color: #e74c3c;
  font-weight: 500;
}
</style>