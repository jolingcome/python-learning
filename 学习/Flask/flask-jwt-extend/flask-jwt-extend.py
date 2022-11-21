# 在web开发中，Client与Server的交互都是通过HTTP协议发送请求和接收响应，但是因为HTTP协议是无状态的(stateless)，
# 也就是说Client和Server都不会记得先前的状态，Client每次发送request都会被视为是独立的，Server无法确定Client是否已经发送过认证请求。
#
# 本文分享基于Token即令牌的认证。在flask中，使用的扩展是flask-jwt-extended。

# JWT的原名是JSON Web Token，它是一种协定，就是把JSON结构的信息进行加密后变成Token传递给Client端，然后客户端透过这个Token来与服务器进行交互。
# 简单来说就是：使用者在登录或是验证过身份后，后端会在返回请求中附上JWT Token，
# 未来使用者发送Request时携带此Token，就表示通过验证，而沒有携带JWT Token的使用者就会被拒绝访问，需要重新登录或重新验证身份。

# 这次示例，我们会用上之前介绍flask-sqlalchemy、flask-cors、flask-restful等扩展，编写一个相对完整的前后端分离的web后端系统，它具备如下功能
#
# 可以实现用户登录
# 用户登录信息的数据库存储
# 基于Token的前后端交互、RESTful API
# 跨域访问

# 通过scripts目录下的dbInitialize.py脚本文件创建初始数据库表并插入一条数据，用户名是admin@gmail.com，
# 密码是字符串123456经过sha256加密后的数据，默认用户是激活状态

