<template>
  <app-sidebar />
  <main class="column-1">
    <app-bar />
    <router-view/>
  </main>
</template>
<script>
import AppSidebar from "@/components/bars/AppSidebar";
import AppBar from "@/components/bars/AppBar";
export default {
  components: {AppBar, AppSidebar}
}
</script>