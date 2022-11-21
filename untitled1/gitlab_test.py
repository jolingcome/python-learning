#使用gitlab包执行gitlab操作
#https://www.cnblogs.com/snailgirl/articles/9454701.html
# https://blog.csdn.net/wmj150731/article/details/103314533
# https://blog.csdn.net/weixin_39918043/article/details/110829861
import gitlab,base64
#登录
gl = gitlab.Gitlab('https://gitlab.sh.sensetime.com', private_token='Liwgmpgzh17ychyzSMyZ')

#获取项目方法：
print("*********列出所有项目**************")
#列出所有项目
projects=gl.projects.list()
# print(projects)
for project in projects:
    print(project)
print("*********查找项目**************")
#查找项目
project=gl.projects.list(search='genieadapter')
print(project)


print("*********通过id获取项目**************")
#通过id获取项目
project=gl.projects.get(3937) #3937是genieadapter
print(project)
print(project.name,project.id,project.attributes)
print("*********通过对象获取分支**************")
branches=project.branches.list()
print(branches)
print("*********通过指定分支的属性**************")
branch=project.branches.get('master')
print(branch)
print("*********获取所有commit info**************")
commits=project.commits.list()
print(commits)
print("*********获取指定项目的merge request**************")
mrs=project.mergerequests.list()
print(mrs)


print("*********获取issue**************")
issues = project.issues.list()
print(issues)




#组的操作：
#列出所有组
print("*********列出所有组**************")
all_groups=gl.groups.list(all=True)
print(all_groups)
for group in all_groups:
    print(group.name,group.id)
#根据groupid 获取某个组：
print("*********根据groupid 获取某个组**************")
singal_group=gl.groups.get(8051)
print(singal_group.name,singal_group.id)

#创建组，修改、删除组：
# group=gl.groups.create({'name':'group1','path':'group1'})
# #修改
# group.description='My awesome group'
# group.save()
# #删除
# gl.groups.delete(1) #通过id来删除
# group.delete() #通过对象直接删除

#获取当前组的成员
print("*********获取当前组的成员**************")
members=group.members.list()
print(members)
#获取所有成员
print("*********获取所有成员**************")
members1=group.members.all(all=True)
print(members1)
#通过id获取组员member_id
print("*********通过id获取组员member_id**************")
members2=group.members.get(213)
print(members2)

#添加一个成员到指定组
"""
GIT权限
gitlab.GUEST_ACCESS=10
gitlab.REPORTER_ACCESS=20
gitlab.DEVELOPER_ACCESS=30
gitlab.MAINTAINER_ACCESS=40
gitlab.OWNER_ACCESS=50
"""
# user_id=15
# member4=group.members.creat({'user_id':user_id,'access_level':gitlab.GUEST_ACCESS})

# #修改组的权限
# members1.access_level=gitlab.DEVELOPER_ACCESS
# members1.save()
# #or
# members1.access_level=10
# members1.save()

#将成员从某组移除
# group.members.delete(1) #通过组成员ID进行移除member_id
# members.delete() #通过组成员对象直接进行删除



# #获取某文件的内容
# f=project.files.get(file_path='/sensetime-sfe/genieadapter/pom.xml',ref='master')
# print(f)
# content_base=base64.b64decode(f.content)
# content=str(content_base,'utf-8')
# print(content)

