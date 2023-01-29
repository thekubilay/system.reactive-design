<template>
  <div class="page-toolbar overflow-hidden">
    <slot></slot>
  </div>
</template>

<script>
export default {
  name: "PageToolbar"
}
</script>

<style>
.page-toolbar {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 78px;
  min-height: 78px;
  background-color: #f5f6fa;
  border-bottom: 2px solid #6ca8da;
  box-shadow: rgba(0, 0, 0, 0.08) 0px 3px 5px;
}
.page-toolbar > .right {
  padding-right: 18px;
}
.page-toolbar .wrapper.dr2 {
  margin-left: 14px;
  margin-right: 14px;
}
.page-toolbar .wrapper > span.label-title {
  font-size: .8rem;
  margin-bottom: 6px;
  padding-left: 2px;
}

.page-toolbar .wrapper > .p-multiselect,
.page-toolbar .wrapper > .p-dropdown {
  border-radius: 0;
}
.page-toolbar .wrapper.dr2 .p-dropdown {
  width: 100px;
  min-width: 100px;
  max-width: 100px;
}
.page-toolbar .wrapper.dr3 .p-multiselect {
  width: 222px;
  min-width: 222px;
  max-width: 222px;
}
.page-toolbar .p-dropdown .p-dropdown-label,
.page-toolbar .p-multiselect .p-multiselect-label {
  font-size: .9rem;
  height: 34px;
  display: flex;
  align-items: center;
  padding: 0 8px;
}
.page-toolbar .p-multiselect .p-multiselect-trigger,
.page-toolbar .p-dropdown .p-dropdown-trigger {
  width: 2rem;
}
.page-toolbar .p-dropdown-panel .p-dropdown-items .p-dropdown-item {
  padding: 6px !important;
  font-size: .8rem !important;
}
</style>