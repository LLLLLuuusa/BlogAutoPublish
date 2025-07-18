---
title: Hibernate Validator
tags: 
- 数据校验
categories:
- 学习笔记
---
# 介绍

Hibernate Validator 是 Java 平台上的一个验证框架，用于在应用程序中执行数据验证。它基于 Bean Validation 规范，并且可以帮助确保数据的有效性和一致性。

# 安装

```xml
<dependency>
    <groupId>org.hibernate.validator</groupId>
    <artifactId>hibernate-validator</artifactId>
    <version>6.0.9.Final</version>
</dependency>
```

# 使用

## 常用注解

| 注解                        | 说明                                                         | 用法                                               |
| --------------------------- | ------------------------------------------------------------ | -------------------------------------------------- |
| @Nul                        | 被注释的元素必须为 null                                      |                                                    |
| @NotNull                    | 被注释的元素必须不为 null                                    | @NotNull 用在**基本类型**上,字符串和自定义类不能用 |
| @NotBlank                   | 被注释的字符串的必须非空                                     | @NotBlank 用在**String**上面                       |
| @NotEmpty                   | 被注释的列表的必须非空                                       | @NotEmpty 用在**集合类**上面                       |
| @AssertTrue                 | 被注释的元素必须为 true                                      |                                                    |
| @AssertFalse                | 被注释的元素必须为 false                                     |                                                    |
| @Min(value)                 | 被注释的元素必须是一个数字，其值必须大于等于指定的最小值     |                                                    |
| @Max(value)                 | 被注释的元素必须是一个数字，其值必须小于等于指定的最大值     |                                                    |
| @DecimalMin(value)          | 被注释的元素必须是一个数字，其值必须大于等于指定的最小值     |                                                    |
| @DecimalMax(value)          | 被注释的元素必须是一个数字，其值必须小于等于指定的最大值     |                                                    |
| @Size(max, min)             | 被注释的元素的大小必须在指定的范围内，元素必须为集合，代表集合个数 |                                                    |
| @Pattern(regexp = )         | 正则表达式校验                                               |                                                    |
| @Digits (integer, fraction) | 被注释的元素必须是一个数字，其值必须在可接受的范围内         |                                                    |
| @Past                       | 被注释的元素必须是一个过去的日期                             |                                                    |
| @Future                     | 被注释的元素必须是一个将来的日期                             |                                                    |
| @Length(min=, max=)         | 被注释的字符串的大小必须在指定的范围内，必须为数组或者字符串，若微数组则表示为数组长度，字符串则表示为字符串长度 |                                                    |
| @Range(min=, max=)          | 被注释的元素必须在合适的范围内                               |                                                    |
| @URI                        | 字符串是否是一个有效的URL                                    | \                                                  |

```tex
注意：
1.@NotNull：不能为null，但可以为empty(“”," “,” “)
2.@NotEmpty：不能为null，而且长度必须大于0 (” “,” ")
3.@NotBlank：只能作用在String上，不能为null，而且调用trim()后，长度必须大于0(“test”) 即：必须有实际字符
```

## 实体类

```java
@ToString
@NoArgsConstructor
@AllArgsConstructor
public class User {
    @NotBlank(message = "id不能为空")
    String id;
}
```

## 校验

### 直接校验

```java

public static void main(String[] args) {
    User user = new User();
    user.setId("1");

    ValidatorFactory factory = Validation.buildDefaultValidatorFactory();
    Validator validator = factory.getValidator();

    Set<ConstraintViolation<User>> violations = validator.validate(user);

    for (ConstraintViolation<User> violation : violations) {
        System.out.println(violation.getMessage());
    }
}
```

### 注解校验

```java
@RestController
@RequestMapping("/v2/api")
@Validated
public class demoController {
    @GetMapping("/demo")
    public String demo(@Valid User user) {
        System.out.println(user);
        return "测试成功";
    }
}
```

## 捕捉异常

```java
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(MethodArgumentNotValidException.class)
    @ResponseBody
    public Result handleBindException(MethodArgumentNotValidException ex) {
        FieldError fieldError = ex.getBindingResult().getFieldError();
        return Result.error(fieldError.getDefaultMessage());
    }
}
```

