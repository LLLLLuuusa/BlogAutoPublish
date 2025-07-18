---
title: Flowable
tags: 
- 工作流引擎
categories:
- 学习笔记
---
# 介绍

Flowable是一个使用Java编写的轻量级业务流程引擎.它拥有自己的用户管理、微服务API等一些了功能,是一个服务平台

可使用此框架完成工作流操作,如A请假,需要B同意才可运行.

# 安装

```xml
<dependency>
    <groupId>org.flowable</groupId>
    <artifactId>flowable-engine</artifactId>
    <version>6.7.2</version>
</dependency>
```

若使用spring则导入依赖

```xml
<dependency>
    <groupId>org.flowable</groupId>
    <artifactId>flowable-spring-boot-starter</artifactId>
    <version>6.7.2</version>
</dependency>
```

## 使用mysql

flowable会找flowable数据库,若里面没有表会初始化导入表

```java
ProcessEngineConfiguration cfg = new StandaloneProcessEngineConfiguration()
    .setJdbcUrl("jdbc:h2:mem:flowable;DB_CLOSE_DELAY=-1")
    .setJdbcUsername("sa")
    .setJdbcPassword("")
    .setJdbcDriver("org.h2.Driver")
    .setDatabaseSchemaUpdate(ProcessEngineConfiguration.DB_SCHEMA_UPDATE_TRUE);

ProcessEngine processEngine = cfg.buildProcessEngine();
```

## spring使用mysql

spring模式会根据配置文件寻找数据库

```properties
# 数据库驱动：
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
# 数据源名称
spring.datasource.name=defaultDataSource
# 数据库连接地址
spring.datasource.url=jdbc:mysql://localhost:3306/flowable?serverTimezone=Asia/Shanghai&useUnicode=true&characterEncoding=utf-8&zeroDateTimeBehavior=convertToNull&useSSL=false&allowPublicKeyRetrieval=true
# 数据库用户名&密码：
spring.datasource.username=root
spring.datasource.password=root
```



# 流程定义

在resources/processes中创建流程文件,格式为:流程名.bpmn20.xml

流程定义主要成员有:

+ 流程区:process
+ 启动事件:start event
+ 用户任务:user task
+ 排他网卡:exclusive gateway
+ 目标引入:sequenceFlow
+ 事件处理:service task

## 文件配置

可通过修改xml文件来配置流程

### 流程区

```xml
<process id="流程id" name="流程名" isExecutable="true">
    ...
</process>
```

### 启动事件

```xml
<startEvent id="启动id"/>
```

### 用户任务

```xml
<userTask id="任务id" name="任务名"/>
```

可指定任务的候选人或候选组

```xml
<userTask id="任务id" name="任务名" flowable:candidateGroups="组名"/>
<userTask id="任务id" name="任务名" flowable:assignee="人名"/> 
```

一般使用,动态设置处理人,这样历史信息可以查看处理人

```xml
<userTask id="任务id" name="任务名" flowable:candidateGroups="组名" flowable:assignee="${处理人}"/>
```

### 目标引入

目标引入可将两个对象连接

```xml
<sequenceFlow id="引入id" sourceRef="起点id" targetRef="终点id" />
```

### 排他网关

排他网关用来做判断,是则执行某事件,否则执行某事件

排他网关需结合目标引入使用

```xml
<exclusiveGateway id="排他网关id"/>
<sequenceFlow sourceRef="引入启动,排他网关Id" targetRef="终点id">
    <!-- 条件表达式,判断参数是否成立 -->
    <conditionExpression xsi:type="tFormalExpression">
        <![CDATA[
          ${参数}
        ]]>
    </conditionExpression>
</sequenceFlow>
<sequenceFlow  sourceRef="引入启动,排他网关Id" targetRef="终点id">
    <!-- 条件表达式,判断参数是否成立 -->
    <conditionExpression xsi:type="tFormalExpression">
        <![CDATA[
          ${!参数 }
        ]]>
    </conditionExpression>
</sequenceFlow>
```

### 事件处理

```xml
<serviceTask id="事件处理id" name="事件处理名"
        flowable:class="执行处理的class文件位置"/>
```

官方提供了一些默认的执行处理class

| 文件                                    | 说明 |
| --------------------------------------- | ---- |
| org.flowable.CallExternalSystemDelegate |      |
| org.flowable.SendRejectionMail          |      |

也可以自定义事件

```java
@Log4j2
public class SendRejectMessage implements JavaDelegate {
    @Override
    public void execute(DelegateExecution delegateExecution) {
       log.info("你的请假被拒绝了..."); 
    }
}
```

# 流程部署

## java部署

```java
// 获取部署对象
RepositoryService repositoryService = processEngine.getRepositoryService();
// 资源管理对象,用于定义流程文件
Deployment deployment = repositoryService.createDeployment()
  .addClasspathResource("流程定义文件.bpmn20.xml")
  .name("流程名,和流程区一致")
  .deploy();
// 流程管理对象
RuntimeService runtimeService = processEngine.getRuntimeService();
// 任务管理对象
TaskService taskService = processEngine.getTaskService();
// 历史信息管理对象
HistoryService historyService = processEngine.getHistoryService();
```

## spirng部署

spring会自动识别resources/processes内的流程定义文件,注册对应的bean即可部署,不用再部署repositoryService

```java
// 资源管理对象
@Autowired
private RepositoryService repositoryService;
// 流程管理对象
@Autowired
private RuntimeService runtimeService;
// 任务管理对象
@Autowired
private TaskService taskService;
// 历史信息管理对象
@Autowired
private HistoryService historyService;
```

# 资源管理

## 查询流程

```java
@Test
void query(){
    //创建流程查询对象
    ProcessDefinitionQuery processDefinitionQuery = repositoryService.createProcessDefinitionQuery();
    //根据id查询
    ProcessDefinition processDefinition = processDefinitionQuery.deploymentId("id").singleResult();
    log.info("流程DeploymentId:"+processDefinition.getDeploymentId());
    log.info("流程名:"+processDefinition.getName());
    log.info("流程描述信息:"+processDefinition.getDescription());
    log.info("流程id:"+processDefinition.getId());
}
```

## 删除流程

```java
@Test
void delete(){
    //第二个参数是级联删除,默认无级联删除
    repositoryService.deleteDeployment("流程id",false);
}
```

## 新增流程

```java
@Test
void add(){
    Deployment deployment = repositoryService.createDeployment()
  .addClasspathResource("流程定义文件.bpmn20.xml")
  .name("流程名,和流程区一致")
  .deploy();
}
```

# 流程管理

## 流程启动

```java
@Test
void request(){   
    String name = "张三";
    String day = "1";
    String description = "生病";

    HashMap<String, Object> variables = new HashMap<>();
    variables.put("name", name);
    variables.put("day", day);
    variables.put("description", description);
	//启动流程
    runtimeService.startProcessInstanceByKey("流程名",variables);
}
```

# 任务管理

## 查询任务

```java
@Test
void query(){
    List<Task> tasks = taskService.createTaskQuery()
        //不指定查询默认查询全部
        .processDefinitionKey("holiday-request")//指定查询流程
        .taskAssignee("指定人")//操作人,userTask有配置则需要
        .taskCandidateGroup("指定组")//操作人所属组,userTask有配置则需要
        .list();
    for (Task task : tasks) {
        System.out.println("################");
        System.out.println(taskService.getVariables(task.getId()));
    }
}
```

## 处理任务

```java
@Test
void complete(){
    HashMap<String, Object> variables = new HashMap<>();
    variables.put("变量", 值);//需要传给目标引入的变量
    taskService.complete("任务id",variables);
}
```

# 历史信息管理

flowable对比其他工作流框架最大优点就是其会自动保存历史信息

## 获取活动信息

```java
@Test
void history(){
    List<HistoricActivityInstance> activities =
        historyService.createHistoricActivityInstanceQuery()
        .processInstanceId("流程id")//指定查询流程
        .finished()//指定查询已完成的
        .orderByHistoricActivityInstanceEndTime().asc()//根据结束事件排序
        .list();

    for (HistoricActivityInstance activity : activities) {
        System.out.println("################");
        System.out.println("id:"+ activity.getActivityId());
        System.out.println("处理人:"+ activity.getAssignee());
        System.out.println("处理时间:"+ activity.getDurationInMillis());
    }
}
```

## 获取历史任务信息

```java
@Test
void history(){
    List<HistoricTaskInstance> historicTasks = historyService.createHistoricTaskInstanceQuery()
            .processInstanceId("流程id")
            .list();

    for (HistoricTaskInstance historicTask : historicTasks) {
        System.out.println("################");
        System.out.println("任务ID:" + historicTask.getId());
        System.out.println("处理组:" + historicTask.getCandidateGroups());
    }
}
