yege_life
=========

这是一个使用Django和微信公众平台相结合的小项目。

主要功能是用来发布一些文本 图片和地理位置信息。

微信端发送的文本 图片和地理位置信息保存在文件中。

### 设置setting.py

需要设置以下两项：

	WEIXIN_TOKEN:微信token
	FILE_PATH:保存文件的路径
	
### 文件结构

	--
	 --files 
	 --sites
	 --weixin
	 --yege_life
	   --write.py

	 files 用来保存文件的路径，它可用来配置 FILE_PATH
	 sites 项目的一个app，提供web页面显示
	 weixin 项目的一个app，用来响应微信端的请求
	 write.py 包含了文件读写等操作
	 
### 微信公众平台配置
	
	URL：http://example.com/weixin/check/ 
	Token：与WEIXIN_TOKEN一致
	
### web 访问

	http://example.com/sites/username/show/
	
### 微信端命令
	
	用户注册： @#usename#pwd
	测试： ##
	发布文本信息：@@text
	发布地理信息：@+
	发布图片信息：@*
	
### 其他
	
	地图不显示，可能是因为 google map api 被墙

	联系方式：gewenmao@gmail.com
	