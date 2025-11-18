---
title: specify规范驱动
tags: 
- ai
categories:
- 学习笔记
---

# Spec Kit 规范驱动工具

Spec Kit 是 GitHub 提出的 规格驱动开发（Specification-driven Development） 工具包，用于通过“规格 → 计划 → 任务 → 实现”的流程，让软件开发更加结构化、可追踪、可协作。

+ git官网:https://github.com/github/spec-kit
+ 第三方汉化:https://github.com/888888888881/spec-kit-chinese

# 安装

使用uv命令进行安装
```shell
uv tool install specify-cli --from git+https://github.com/github/spec-kit.git
```

安装成功后使用命令检查是否安装
```shell
 specify
```

# 使用

在终端上使用命令初始化项目,构建规范文档,并按照构建过程选择自己的ide
```shell
 specify  init . 
```
![](../img/屏幕截图%202025-11-18%20111334.jpg)

在ai终端上依次使用
|命令|作用|
|-|-|
|specify  constitution 原则 |给ai定义开发原则,如变量命名规范|
|specify  specify 用户场景 |为当前项目定义用户场景,避免ai过度设计|
|specify  plan 实施计划 |为ai定义实施计划|
|specify  task |生成任务|
|specify  implement |执行任务|

# 评价
+ 优点:
相较于市面上一些常规的规范驱动工具,如OpenSpec,SpecifyKit定义的规范更加详细,更加注重产品价值和用户场景

+ 缺点:
  + 由于SpecifyKit定义的规范驱动过于庞大,导致一次任务消耗过量的token,性价比不高,且由于目前ai模型上下文都有限制,这种工具很容易导致ai失忆,即使常规ide有上下文压缩,该工具也有保存记录,但避免ai发散的会好解决办法还是避免超出上下文
  + 不适用与多人协作团队开发,每个人关注的业务和模块不同,不能共用同一specify,会导致每个人的specify定义的用户场景不同,从而导致产品混乱
  + 摒弃了cursor等ide自带的优点,cursor最大的优点在于其可以随时回退到指定chat去修改需求而不影响整体代码,但是SpecifyKit问题在于需求在最开始的时候进行定义,即使后期可以修改需求,但是所有的任务计划都会因此改变,从而影响流程(比如当前已执行到阶段3,但是需求又修改了,那么任务计划就会因为需求改变而改变,从而导致流程中断)
  + 使用如"specify plan 写一份总分总格式的日记",agent可能不会执行specify plan,而是直接生成日记