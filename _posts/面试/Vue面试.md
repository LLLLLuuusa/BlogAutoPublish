---
title: java面试
tags: 
- Java
categories:
- 面试宝典
---

# Vue基础

## v-if和v-for的执行顺序
+ vue2先执行v-if,再执行v-for
+ vue3先执行v-for,再执行v-if

## v-show和v-if的区别
+ v-if再渲染的时候,根据条件判断是否渲染对应的dom,因此其渲染快,更新慢,适用于更新频次不高的场景
+ v-show在对应的dom上添加display:条件来判断是否渲染,因此其渲染慢,更新快,使用与更新频次较高的场景

## vue3的ref和react的异同/vue如何实现数据绑定的
vue通过ref/react来实现数据绑定,它们都是通过defineProps来实现的
+ ref可以响应式更新任何对象或数值或字符串
+ react只能绑定js对象

## vue的生命周期

| Vue2 生命周期       | Vue3 对应生命周期（组合式 API）         | 执行阶段说明      |
| --------------- | ---------------------------- | ----------- |
| —               | `setup`                      | 所有生命周期函数执行前 |
| `beforeCreate`  | `beforeCreate`（建议使用 `setup`） | Vue 实例初始化之前 |
| `created`       | `created`（建议使用 `setup`）      | Vue 实例初始化之后 |
| `beforeMount`   | `beforeMount`                | 组件挂载到页面前    |
| `mounted`       | `mounted`                    | 组件挂载到页面后    |
| `beforeUpdate`  | `beforeUpdate`               | 数据更新前       |
| `updated`       | `updated`                    | 数据更新后       |
| `beforeDestroy` | `beforeUnmount`（Vue3 改名）     | 组件卸载前       |
| `destroyed`     | `unmounted`（Vue3 改名）         | 组件卸载后       |

## vue的父子组件通信方法

+ 子组件通过props获取父组件参数
```vue
<!--父组件-->
<div>
    <ChildComponent :message="parentMsg" />
</div>
```
```vue
<!--子组件-->
<script>
export default {
  props: {
    message: {
      type: String,
      required: true
    }
  }
}
</script>
```
+ 父组件通过$emit获取子组件参数
```vue
<!--子组件-->
<script>
export default {
  methods: {
    sendData() {
      this.$emit('update-message', '子组件传来的数据')
    }
  }
}
</script>
```
```vue
<!-- 父组件 -->
<template>
  <div>
    <ChildComponent @update-message="handleMessage" />
  </div>
</template>

<script>
import ChildComponent from './ChildComponent.vue'

export default {
  components: { ChildComponent },
  methods: {
    handleMessage(value) {
      console.log(value)
    }
  }
}
</script>
```

## vue2和vue3的处理虚拟dom区别
+ vue2通过diff算法来计算哪些dom需要更新
+ 由于两个虚拟dom只是更换了顺序,vue2会重新所有都便利更新一遍,浪费效率,因此vue3采用最长公共子序列+diff算法来避免重复计算问题

## options API和Composition API的区别
+ options API：vue2的传统api使用方式,结构简单,易于理解,但是代码过长时不易阅读,需要组件化处理
+ Composition API：vue3的api使用方式，灵活使用,代码简单,但是学习成本高,不易记

## vue如何做权限控制
vue可以通过守护路由的方式实现权限控制,当页面在跳转前后可自定义函数,做权限判断跳转对应页面
```js
Vue.use(Router)

const router = new Router({
  routes: [
    { path: '/login', component: Login }
  ]
})

// 全局前置守卫：判断是否登录
router.beforeEach((to, from, next) => {
    // to:来自哪个页面
    // from:去哪个页面
    // next():放行
    next()
})

// 全局后置守卫：页面切换后执行
router.afterEach((to, from) => {

})

export default router
```

## vuex是什么
vuex是vue的一个状态管理工具,可以实现vue的数据缓存
使用vuex需要配合localstore和computed来使用

vuex由5个核心参数构成：
+ store:存储vue参数,本身只是临时存储,需要配合localstore来使用
+ getter:获取store的参数
+ mutations:设置store的参数
+ actions:通常配合new Promise来异步执行mutations的方法,使用场景:通过ajax来更新store
+ modules:模块化,若vue项目过大,可以配置不同模块对应的不同sotre

# 浏览器渲染原理

1. 浏览器通过url访问服务器,获取静态资源
2. 拿到静态html,开始解析html包含的纯html、css和js
3. 纯html会解析成dom,如果时vue或者react,那么会先解析成虚拟dom,再转换为dom
4. css会转换为cssom
5. js会在转换dom和cssom中同步执行
6. 最终将生成的cssom和dom构建成一个渲染树进行渲染

# 渲染优化手段/页面优化手段
页面优化可以从渲染的角度进行分析和优化
1. 通过url获取的静态资源,可以放在具有cdn的第三方服务器,如果是图片的话可以使用url而非静态资源
2. 构建的html时,可以使用webpack+treeshaking,它可以在构建的时候删掉未使用的代码
3. css使用