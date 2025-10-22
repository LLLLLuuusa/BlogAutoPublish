---
title: TypeScript
tags:
  - ts
categories:
  - 学习笔记
---

# 类型推断
ts的对象是强类型,js的对象是弱类型
+ 强类型:不符合规范的赋值会报错
+ 弱类型：赋值的时候可以随时修改对象类型

ts会根据输入的数据自动判断类型
```typescript
let a = 'aaa'
a = 10 //会报错
```

# 类型注解
可以在赋值的时候规定类型
```typescript
let a:string = 'aaa'
let b:string
```

# 类型断言
ts在执行复制操作时,会判断该操作是否可以执行,如果可能不会执行成功,则不允许对结果对象操作
```typescript
let arr = [1,2,3]
let result = arr.find(item => {item > 2})
result * 5 //会报错,认为result对象可能为空,不允许操作result

result = arr.find(item => {item > 2}) as number
result * 5 //断言result必然返回值
```

# 基本类型和联合类型
```typescript
// 基本类型：string、number、boolean、null、undefined
let str:string
let num:number
let bo:boolean
let nu:null //不常用,通常用联合替代
let un:undefined //不常用,通常用联合替代
// 联合类型：可以指定对象有哪些类型或者范围
let str2:string|undefined = undefined //指定对象可能是string或者undefind
let num2:1|2|3 = 5 //指定对象范围只能是1|2|3,赋值5会报错
```

# 数组
ts的数组有3种写法
```typescript
//不推荐,类型可以随意赋值
let arr1 = [1,'a',true]
//推荐
let arr2:number[] = [1,2,3]
//另类写法
let arr3:Array<number> = [1,2,3]
```

# 元组
ts的元组是一种特殊集合类型,限定了集合的存储个数和类型
```typescript
let t1:[number,string,boolean] = [1,'a',3] //会报错,第三个类型要求是boolean
let t2:[number1,number2] = [1] //会报错,少了第二种类型
let t3:[number1,number2?] = [1] //不会报错,使用？代表该值可选
```

# 枚举
ts提供一种枚举类型
```typescript
enum myEnum{
    A,
    B,
    C
}
console.log(myEnum.A)
console.log(myEnum[0])
```

# 函数
```typescript
//第一个参数必填,第二个参数有默认值,第三个参数选填,第四个参数选填
function Fn(a:number,b = true,c?:string,...rest:number[]):void{
    return 1 //会报错,指定了返回值是void
}
Fn('1') //会报错,指定了传参是number
Fn(20,true,'aa',1,2,3,4) //正确用法
```

# 接口
接口定义了一个对象的使用规范
```typescript
interface Obj{
    name:string,
    age,number
}

let obj:Obj = {
    name:'a',
    age:10
}
```

# 类型
```typescript
let a:string|number //每次定义对象都要写一次很长的类型,过于麻烦

type MyType = string|number
let b:MyType //定义一次type,之后直接使用
```

# 泛型
ts支持泛型,定义方法的时候先不定义其类型,使用的时候再定义
```typescript
function Fn<T>(a:T,b:T):T[]{
    return [a,b]
}
Fn<number>(1,'a') //会报错,当指定泛型后,所有的T都会变为指定类型
Fn<number>(1,2) //正确用法

```

# 函数重载
js不支持函数重载,但是ts支持

```typescript
function hello(): string {
    return "hello"
}

function hello(value: string | number): string {
    if (typeof value === 'string') {
        return `hello,我的名字是${value}`
    } else if (typeof value === 'number') {
        return `hello,我的年龄是${value}`
    }else {
        return 'hello'
    }
}

hello('demo')
```

# 接口的继承
```typescript
interface parther{
    name:string
    age:number
}
interface child extends parent{
    phone:string
}

let user:child = {
    name:'张三',
    age:18,
    phone:'10086'
}
```

# 类的使用
ts的类使用和python/java的方法很像

```typescript
class myClass extends fatherClas implements fatherInterface{
    public name: string // 类的属性
    age: number // public可以省略,除了public还有private、protected和static,用法和java一样
    phone?: string // 若ts的配置文件开启了强制验证,那么类的属性必须赋值,除非它是可选或有默认值
    birthday = '2001.9'
    private static readonly address = 'china' //readonly类似java的final,表示不可修改

    // 构造函数,构造函数必须给必填项赋值
    constructor(name:string,age:number) {
        super();
        this.name = name;
        this.age = age;
    }

}
```

# 存取器
ts提供了一个getter和setter的封装,可以取和设置类的私有属性
```typescript
class User{
    private _phone:string = ''
    
    get phone(): string {
        if (!this._phone) return '';

        if (this._phone.length === 11) {
            return this._phone.replace(/^(\d{3})\d{4}(\d{4})$/, '$1****$2');
        } else {
            return '******';
        }
    }
    
    set phone(newPhone:string){
        this._phone = newPhone
    }
}

let user = new User()
user.phone = "12345678901"
console.log(user.phone) // 输出：123****8901
```

# 抽象类
ts的抽象类和java的抽象类概念和用法时一样的
```typescript
abstract class Animal {
  constructor(public name: string) {}

  abstract makeSound(): void; // 抽象方法：必须由子类实现

  move() {
    console.log(`${this.name} is moving`);
  }
}

class Dog extends Animal {
  makeSound() {
    console.log('Woof! Woof!');
  }
}

const d = new Dog('Buddy');
d.makeSound(); // Woof! Woof!
d.move(); // Buddy is moving
```

# 泛型类
用法和java的泛型类是一样的,在不确定传入的类型之前,可以使用T来代替
```typescript
class myClass<T>{
    public name: T

    // 构造函数,构造函数必须给必填项赋值
    constructor(name:T) {
        this.name = name;
    }
}

let cls = new MyClass<string>('张三')
```

