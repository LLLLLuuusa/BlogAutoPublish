---
title: Mockito
tags: 
- 软件测试
categories:
- 学习笔记
---
# 介绍

Mockito是一种Java Mock框架,主要是用来做Mock测试,它可以模拟任何Spring管理的Bean、模拟方法的返回值、模拟抛出异常等待

# 安装

```xml
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-core</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>
```

# 使用

## 创建

```java
List<Integer> list = Mockito.mock(List.class);
```

### 注解创建

```java
@Mock
private List<Integer> list;

// 初始化模拟对象
@BeforeEach
public void setup() {
    MockitoAnnotations.initMocks(this);
    //最新版本mocks用openMocks(this);
}

@Test
void testVerfy(){
    list.add(1);
    Mockito.verify(list).add(1);//有该行为,正常执行
    Mockito.verify(list).add(2);//无该行为,报错
}
```



虚拟对象使用时,若不定义其返回值,则默认其返回值为其类型的默认值

```java
//list是Int类型,所以返回int默认值0
list.get(0);
```

术语上,给虚拟对象定义返回值的行叫**打桩**

## 校验

校验可用来判断虚拟对象是否执行某行为,未执行则报错

```java
@Test
void testVerfy(){
    List<Integer> list = Mockito.mock(List.class);
    list.add(1);
    Mockito.verify(list).add(1);//有该行为,正常执行
    Mockito.verify(list).add(2);//无该行为,报错
}
```

校验也可以判断某行为的执行次数

```java
@Test
void testVerfy(){
    List<Integer> list = Mockito.mock(List.class);
    list.add(1);
    Mockito.verify(list, times(2)).add(1);//行为不为2次,报错
}
```



## 打桩/存根

定义某个虚拟对象执行某行为时的返回值

```java
@Test
void testWhen(){
    List<Integer> list = Mockito.mock(List.class);
    Mockito.when(list.get(0)).thenReturn(100);//打桩返回值
    Mockito.when(list.get(1)).thenThrow(new NullPointerException("空指针异常"));//打桩异常
    log.info(list.get(0));//返回100
    log.info(list.get(1));//返回空指针异常
}
```

打桩的写法有两种

```java
Mockito.when(list.get(0)).thenReturn(100);
Mockito.doReturn(100).when(list.get(0));
```

## 断言

判断虚拟对象的返回值是否是期望值,不是则报错

```java
@Test
void TestAssertions(){
    List<Integer> list = Mockito.mock(List.class);
    Mockito.when(list.get(0)).thenReturn(100);
    Assertions.assertEquals(101,list.get(0));//判断返回值是否为期望值
}
```

## spy

spy区别与moke()创建虚拟对象,如果不打桩默认都会执行真实的方法，如果打桩则返回桩实现

spy传对象实例,moke传class

```java
@Test
void TestSpy(){
    List<Integer> list = Mockito.spy(new ArrayList<>());
    list.add(10);
    Assertions.assertEquals(10,list.get(0));//不打桩,返回对象值
    Mockito.when(list.get(0)).thenReturn(100);
    Assertions.assertEquals(100,list.get(0));//打桩,返回虚拟对象值
}
```

### 注解创建

```java
@Spy
private List<Integer> list = new ArrayList<>()

// 初始化模拟对象
@BeforeEach
public void setup() {
    MockitoAnnotations.initMocks(this);
    //最新版本mocks用openMocks(this);
}

@Test
void TestSpy(){
    list.add(10);
    Assertions.assertEquals(10,list.get(0));//不打桩,返回对象值
    Mockito.when(list.get(0)).thenReturn(100);
    Assertions.assertEquals(100,list.get(0));//打桩,返回虚拟对象值
}
```

## 依赖注解

Service里面有一个工具类,我们对工具类进行mock,并希望在调用Service的时候能拿到工具类的虚拟对象,就需要使用依赖注解

```java
@Mock
private Calculator calculatorMock;//工具类

@InjectMocks
private CalculatorService calculatorService;//Service类

@BeforeEach
public void setup() {
    MockitoAnnotations.initMocks(this);
}

@Test
public void testAddition() {
    //给工具类打桩
    when(calculatorMock.add(2, 3)).thenReturn(5);
	
    //在Service里使用工具类
    int result = calculatorService.addUsingCalculator(2, 3);
	
    //校验和断言
    verify(calculatorMock, times(1)).add(2, 3);
    assertEquals(5, result);
}
```

# 拓展

## 安装

```xml
<!-- 不能和core一起使用 -->
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-inline</artifactId>
    <scope>test</scope>
</dependency>
<dependency>
    <groupId>org.junit.jupiter</groupId>
    <artifactId>junit-jupiter</artifactId>
    <scope>test</scope>
</dependency>
```

## 使用

```java
@Test
void TestStatic(){
    MockedStatic<静态类> staticUtilsMockedStatic = Mockito.mockStatic(静态类.class);
    staticUtilsMockedStatic.when(()->静态类.方法()).thenReturn(Object);//同mocket,打桩
    staticUtilsMockedStatic.when(静态类::方法).thenReturn(Object);//同mocket,另一种打桩
}
```



