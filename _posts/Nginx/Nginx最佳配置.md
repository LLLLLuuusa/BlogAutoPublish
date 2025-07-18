---
title: Nginx最佳配置
tags: 
- Nginx
categories:
- 学习笔记
---
# configure

推荐:

```sh
./configure 
--with-http_gzip_static_module
--with-http_ssl_module
```

可选:

```sh
./configure 
--add-module=/root/nginx/module/purge
--add-module=/root/fair
```

+ with-http_gzip_static_module:压缩模块
+ --with-http_ssl_module:https模块
+ purge:清除缓存模块
+ fair:智能负载均衡模块

# Nginx主配置

```sh
worker_processes auto; #并发数,与cpu内核相同
worker_rlimit_nofile 51200; #当前worker运行用户的最大文件打开数值
user 用户名 #设置用户名

events{
	use epoll; #nginx底层使用的函数
    worker_connections 51200; #单个worker最大连接数
    multi_accept on; #同时收到多个网络连接
}

http{
	include	mime.types; #解析前端响应的资源
	
    server_names_hash_bucket_size 512; #服务器名大小限制512字节
    client_header_buffer_size 32k; #请求头大小限制32k
    large_client_header_buffers 4 32k;#请求行+请求头限制4*32
    client_max_body_size 50m; #最大上传文件
    limit_conn_zone $binary_remote_addr zone=perip:10m; #限制同一ip并发连接数以及下载带宽
	limit_conn_zone $server_name zone=perserver:10m; #$server_name是限制同一server并发连接数以及下载带宽
	
	sendfile on; #使用sendflie()提升文件传输性
    tcp_nopush on; #提高网络传输效率
    tcp_nodelay on; #保证网络连接实效性
    keepalive_timeout 60; #接超时时间
	
	include proxy.conf; #导入反向代理配置
	include gzip.conf #导入压缩配置
	
	include /项目名称/*.conf; #导入具体项目的配置
}

```

# 反向代理配置

```nginx
proxy_temp_path /www/server/nginx/proxy_temp_dir; #从代理服务器接收到的数据的临时文件定义目录
proxy_cache_path /www/server/nginx/proxy_cache_dir levels=1:2 keys_zone=cache_one:20m inactive=1d max_size=5g;#从代理服务器接收到的数据的缓存文件定义目录,有两层目录,缓存区为cache_one,1天内为访问就删除,最大缓存空间5g
client_body_buffer_size 512k;#如果请求的值大于512小于就会将数据先存储到临时文件中
proxy_connect_timeout 60;#建立连接超时时间
proxy_read_timeout 60;#获取数据超时时间
proxy_send_timeout 60;#发送数据超时时间
proxy_buffer_size 32k;#被代理服务器响应头大小,不够会再申
proxy_buffers 4 64k;#被代理服务器响应体大小,4*64k,不够会再申
proxy_busy_buffers_size 128k; #在没有完全读完响应就开始传送数据
proxy_temp_file_write_size 128k;#设置同时写入临时文件的数据量的总大小
proxy_next_upstream error timeout invalid_header http_500 http_503 http_404;#发送503和404时重试
proxy_cache cache_one; #开启缓存,缓存名cache_one
```



# 压缩配置

```nginx
gzip on; #开启压缩
gzip_min_length 1k; #超过指定大小不压缩
gzip_buffers     4 16k; #压缩申请的空间数和大小
gzip_comp_level 5; #压缩等级,好点服务器可以用6
gzip_types     text/plain application/javascript application/x-javascript text/javascript text/css application/xml; #压缩类型
gzip_vary on; #请求头显示已压缩
gzip_proxied   expired no-cache no-store private auth; #根据请求头判断是否压缩
gzip_disable   "MSIE [1-6]\."; #老版浏览器不压缩
```



# 项目配置

```nginx
upstream 集群名{
	server tomcatip:端口 weight=1;
	server tomcatip:端口;
	server tomcatip:端口;
}
server{
    listen 80; #端口
	listen 443 ssl http2; #使用ssl
    server_name 域名; #Ip/域名
    index index.html; #默认打开的html
    root /home/用户/项目 ;#html路径
    
    limit_conn perserver 300; #限制同一server_name并发连接数
    limit_conn perip 25; #限制同一ip并发连接数
    limit_rate 512k; #限制下载带宽
    ssl_certificate /home/用户/项目/.pem; #pew文件
    ssl_certificate_key /home/用户/项目/.pem; #key文件
    ssl_protocols TLSv1.1 TLSv1.2 TLSv1.3; #ssl使用的协议
    
    #禁止访问的文件或目录
    location ~ ^/(\.user.ini|\.htaccess|\.git|\.svn|\.project|LICENSE|README.md){
        return 404;
    }
    
    #SSL证书验证,浏览器会判断证书是否安全
    location ~ \.well-known{
        allow all;
    }
    
    #图片缓存30天
    location ~ .*\.(gif|jpg|jpeg|png|bmp|swf)${
        expires      30d;
    }
    
    #js和css缓存12天
    location ~ .*\.(js|css)?${
        expires      12h; 
    }
    
    location /uri {
        proxy_pass http://集群名/uri; #反向代理
        proxy_set_header Host $host; #请求头带网站名
        proxy_set_header X-Real-IP $remote_addr; #请求头带客户端ip
        proxy_set_header REMOTE-HOST $remote_addr;#请求头带客户端ip
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; #用户真实Ip(用了代理就不能获取真实的)
    }
    
    location /uri {
    	default_type application/json; #默认响应类型
    	content_by_lua_file lua/item.lua #响应结果由lua/item.lua文件决定
    }
```

