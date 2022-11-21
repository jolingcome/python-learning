# pendulum 是一个操作日期时间的开源库，相比内置库 datetime 更加简单、易操作，实际上，pendulum 就是基于 datetime 标准库的。
# https://xugaoxiang.com/2022/08/22/python-module-35-pendulum/
import pendulum
now = pendulum.now("Asia/Shanghai")
print(now)
print(now.year)
print(now.day)
print(now.hour)
print(now.minute)
print(now.minute)
print(now.second)
print(now.day_of_week)
print(now.day_of_year)
print(now.week_of_month)
print(now.week_of_year)
print(now.days_in_month)

print("__________________________________________________")
#转换成常见的datetime格式
print(now.to_iso8601_string())

print("__________________________________________________")
#转换成时间戳
print(now.timestamp())

print("__________________________________________________")
# 转换成其它的时区
print(now.in_timezone("America/Toronto"))

print("__________________________________________________")
# 日期时间字符的格式化
print(now.to_date_string())
print(now.to_formatted_date_string())
print(now.to_time_string())
print(now.to_datetime_string())
print(now.to_day_datetime_string())

print("__________________________________________________")
# 在原来日期上加1年2月3天4小时
print(now.add(years=1, months=2, days=3, hours=4))

print("__________________________________________________")
# 对应于 add,还有 subtract 方法, 如回到去年的现在
print(now.subtract(years=1))

print("__________________________________________________")
# 构造实例并格式化
dt = pendulum.datetime(2022, 8, 22, 14, 15, 16)
dt.format('YYYY-MM-DD HH:mm:ss')
print(dt)

print("__________________________________________________")
# 比较差异，这里有个早晚的问题，diff 方法的第二个参数可以指定返回值是正数还是负数，默认是 True
dt_ottawa = pendulum.datetime(2000, 1, 1, tz='America/Toronto')
dt_vancouver = pendulum.datetime(2000, 1, 1, tz='America/Vancouver')
print(dt_ottawa.diff(dt_vancouver).in_hours())
print(dt_ottawa.diff(dt_vancouver, False).in_hours())

# pendulum 继承自 datetime，相比于 datetime，pendulum 的 API 更加的干净、更加的简单易用，很多的类都进行了改进。
# 很多的代码中，可以直接使用 pendulum 中的 DateTime 实例来代替原有代码中的 datetime 实例。