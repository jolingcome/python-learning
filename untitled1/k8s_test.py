#k8s连接及操作
# pip install kubernetes
# https://www.cnblogs.com/zhangb8042/p/11444756.html
# https://www.cnblogs.com/wuchangblog/p/14087926.html
# https://github.com/kubernetes-client/python/search?q=list_namespace 中文文档

import yaml
from dateutil.tz import tzutc, gettz
from kubernetes import client, config,watch

# """
# 用此命令拿root的token日志
# kubectl -n kubernetes-dashboard describe secret $(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}') |grep token: |cut -d ':' -f 2
# """

api_server = '10.151.5.183:6443'
# token = 'eyJhbGciOiJSUzI1NiIsImtpZCI6IjgxSzF5ZWxUSHNyaHpZTjJ5UlNxU1V4YzdVR0F4amRiR0pPX2pyRnI1cVkifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJkZWZhdWx0Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZWNyZXQubmFtZSI6ImRlZmF1bHQtdG9rZW4tNDhwbjQiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiZGVmYXVsdCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VydmljZS1hY2NvdW50LnVpZCI6ImI1ODA2NWFhLTg0M2QtNDE5OC1iNjMwLTBjYzI0NmFlMDJmZiIsInN1YiI6InN5c3RlbTpzZXJ2aWNlYWNjb3VudDpkZWZhdWx0OmRlZmF1bHQifQ.dobnvC8gxrei43ETlAMl1Cm4JXInqIvZxnlEj1jJ5ekgarI3GdGoP2IwmhSjuTLLYgAXm9UKTjYI7qNtaA9g5gZ9NiJlMNV1eMAhxR06tTF_D4pbmQXjaeCEK6ABDiTtwjfFF0_R_G2LTbnm7CwTdpI7VdkZ4XKD4MiFNStZ39OKjkZKAguUUBwHYIBg-gWygYdz0IydeyUAhLIzMeNsWYpBTsmK7jwlMy-Ov8Mm3gsTp0iuq9dt8hphoclfY353TF7-W8Ly8Xe0aqrldCxkPaLX1Cz5MVHjVtPdlzb0TiiMnN7ZFVl1rFpYntHiNkfR8n5WPrLoLs6faV3uUVQtAQ'
token='eyJhbGciOiJSUzI1NiIsImtpZCI6IkJSTnRBRmdtYW5aQ0FzVlR6NjdhZGF4Y2JHT3hPRWxQZ2k5dzdHekVXY28ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlcm5ldGVzLWRhc2hib2FyZCIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJhZG1pbi11c2VyLXRva2VuLXFtdjd4Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQubmFtZSI6ImFkbWluLXVzZXIiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC51aWQiOiJhODBhYjM2My1mZDFkLTRkZTctYWM0NS0xN2QxODdiMTY4N2IiLCJzdWIiOiJzeXN0ZW06c2VydmljZWFjY291bnQ6a3ViZXJuZXRlcy1kYXNoYm9hcmQ6YWRtaW4tdXNlciJ9.weJSSbMjc7-j4dz-Oxg_8Sg8GfikSCeVQEPbFBPBvy66MZAmghy8GfsP58_00SQoJcnuiSfx-HIRrTC40rly7UinrGlf1cPJBlH06wSM8r9blsLFcZ5tQn6qav2sA-5UXySGIdM9LZC22l41niOv6adjS_0OkK7FvFYLbRLds5nFSdDly_bvjudXfKfZ7NqHm7yZM7ebrim_eW0a1rsALAJ3Ow308JFIGP91gtwEHNoLxCDTgmgpL-koCdDUsU6LhajRzzcAMP_-qQYgmKQzY3R9KymLfmmMRbsbDlzU77Z6q9oQ0Chrh4e3VGQN4nQ__wSwpYN8y8Yz7CNPx7hhnA'
from kubernetes import client,config
config.kube_config.load_kube_config(config_file="./k8s-config")

#获取API的CoreV1Api版本对象
v1=client.CoreV1Api()
print(v1)

#列出 namespaces
count=10
w=watch.Watch()
for event in w.stream(v1.list_namespace,timeout_seconds=10):
    print(event)
#列出 namespaces
for ns in v1.list_namespace().items:
    print(ns.metadata.name)
#列出 所有services
ret=v1.list_service_account_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s \t%s \t%s \t%s \t%s \n" % (i.kind, i.metadata.namespace, i.metadata.name, i.spec.cluster_ip, i.spec.ports))

#列出所有的pod
ret=v1.list_pod_for_all_namespaces(watch=False)
for i in ret.items():
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))

#列出所有的deploy
ret=v1.list_deployments_for_all_namespaces(watch=False)
for i in ret.items:
    print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))


