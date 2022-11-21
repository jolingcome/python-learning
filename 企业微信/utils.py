import subprocess, os
import logging, sys, time, json, hashlib
import argparse, paramiko, requests
from datetime import datetime, timedelta
import config


def prepare_log_path(p=None):
    date = time.strftime("%Y%m%d")
    logpath = f"/storage4/nebula1.2/{date}"
    if p:
        logpath = p
        cmd = f"mkdir -p {logpath}"
        print(cmd)
        out = run_cmd(cmd)
    else:
        cmd = f"rm -rf /storage4/nebula1.2/latest; mkdir -p {logpath}; ln -s {logpath} /storage4/nebula1.2/latest"
        print(cmd)
        out = run_cmd(cmd)

    return logpath


def disable_warnings():
    import warnings

    warnings.filterwarnings(action="ignore", module=".*paramiko.*")
    warnings.filterwarnings(action="ignore", module=".*urllib3.*")


def get_md5(key):
    return hashlib.md5(key.encode("utf-8")).hexdigest()


def setup_basic_config(file=""):
    logfile = "utils.log"
    if file:
        logfile = file
    logging.basicConfig(
        filename="/tmp/" + logfile,
        filemode="a",
        format="%(asctime)-15s %(threadName)s:%(message)s",
        level=logging.DEBUG,
        force=True,
    )


def setup_log(file=""):
    disable_warnings()
    logging.getLogger("paramiko").setLevel(logging.ERROR)
    logging.getLogger("requests").setLevel(logging.ERROR)
    logging.getLogger("urllib3").setLevel(logging.ERROR)
    if file:
        file = file.replace('.log', '.1.2.log')
        setup_basic_config(file=file)
    else:
        log = logging.getLogger()
        log.setLevel(logging.DEBUG)
        stdout = logging.StreamHandler(sys.stdout)
        log.addHandler(stdout)


def run_cmd(cmd):
    logging.info("CMD : " + cmd)
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    )
    p.wait()
    out = p.stdout.readlines()
    ret = "\n".join(x.decode('utf-8', errors='ignore') for x in out)
    err = p.stdout.readlines()
    ret += "\n".join(x.decode('utf-8', errors='ignore') for x in err)
    logging.info("OUTPUT: " + ret)
    return ret


def run_screen_job(name, cmd):
    cmd = f"screen -wipe; screen -S 1.2_{name} -d -m bash -c '%s'" % cmd
    logging.info("SCREEN CMD: %s" % cmd)
    os.system(cmd)


def check_screen_exists(name):
    cmd = f"screen -ls | grep {name} 2>&1 > /dev/null"
    logging.info("check SCREEN: %s" % cmd)
    out = os.system(cmd)
    # 有是0, 没有是1
    if out:
        return False
    else:
        return True


def stop_screen_job(name):
    cmd = f"ps -aux | grep {name} | awk {'print $2'}  | xargs kill -9 2>&1 > /dev/null"
    logging.info("stop SCREEN: %s" % cmd)
    out = os.system("screen -wipe 2>&1 > /dev/null")
    return True


def check_ssh_avaiblable(ip="", user="", pwd="", sleep=60, timeout=1800):
    logging.info("check SSH Avaiable: %s" % get_current_time())
    t = 0
    while t < timeout:
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                hostname=ip,
                port=22,
                username=user,
                password=pwd,
                auth_timeout=20,
                timeout=60,
            )
            logging.info("SSH is OK")
            return True
        except Exception as e:
            logging.info(e)
            time.sleep(sleep)
            t += sleep
    logging.info("SSH timeout : %s" % get_current_time())
    return False


def ssh_cmd(ip="", user="root", pwd="", cmd=""):
    if not pwd:
        pwd = config.pwd
    logging.info(f"SSH {user}/{pwd} CMD : " + cmd)
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(
        hostname=ip,
        port=22,
        username=user,
        password=pwd,
        auth_timeout=400,
        # key_filename="./misc/ssh/id_rsa",
        timeout=400,
    )
    result = ""
    stdin, stdout, stderr = ssh.exec_command(cmd, timeout=40000)
    while True:
        v = stdout.channel.recv(1024)
        try:
            result += v.decode("utf-8", errors="ignore")
        except:
            result += f"{v}"
        v = stderr.channel.recv(1024)
        try:
            result += v.decode("utf-8", errors="ignore")
        except:
            result += f"{v}"
        if not v:
            break
    logging.info(f"SSH CMD OUTPUT: \n{result}")
    # stat = stdout.channel.recv_exit_status()
    return result


def index_exists(ls, i):
    return (0 <= i < len(ls)) or (-len(ls) <= i < 0)


def get_start_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--ip", help="Test System IP address")
    parser.add_argument(
        "-t", "--system", help="define system type", default="", type=str,
    )
    parser.add_argument(
        "-s",
        "--select",
        help="select tests to run, all tests will be selected by default",
        type=str,
    )
    parser.add_argument(
        "-r", "--restart", action="store_true", help="restart screen for test",
    )
    parser.add_argument(
        "-p", "--position", help="file position",
    )
    parser.add_argument(
        "-a", "--part_position", help="part file position",
    )
    parser.add_argument(
        "-T", "--type", help="type of system",
    )
    args = parser.parse_args()
    return parser, args


def get_current_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def print_current_time(msg=""):
    print("%s : %s" % (msg, get_current_time()))


def get_yesterday_time():
    yesterday = datetime.now() - timedelta(1)
    return datetime.strftime(yesterday, "%Y-%m-%d 00:00:00")


def get_today_end_time():
    today = datetime.now() + timedelta(1)
    return datetime.strftime(today, "%Y-%m-%d 00:00:00")


def get_weekday():
    today = datetime.now()
    return today.weekday()  # 0-6 , 5 是礼拜六， 6 是礼拜天


def parse_time(start_time, finish_time):
    duration = time.gmtime(int(round(float(finish_time) - float(start_time))))
    if duration.tm_yday > 1:
        duration_str = time.strftime("%H:%M:%S", duration) + ", %d day(s)" % (
                duration.tm_yday - 1
        )
    else:
        duration_str = time.strftime("%H:%M:%S", duration)
    return duration_str


def wait_state(target, func, sleep=60, timeout=3000):
    t = 0
    resp = func()
    logging.info("target is :%s, func is : %s" % (target, func.__name__))
    while target != resp:
        logging.info(f"{target} != {resp} state not reached,  waited {t} please wait")
        time.sleep(sleep)
        t += sleep
        resp = func()
        if t > timeout:
            logging.info("Timeout to wait")
            raise TimeoutError
    logging.info("state reached")
    return True


def load_env_config(file="/opt/config.json"):
    if os.path.exists(file):
        with open(file, encoding="utf-8", ) as f:
            return json.load(f)
    else:
        return None


def save_env_config(file="/opt/config.json", data=None):
    with open(file, mode="w", encoding="utf-8", ) as f:
        json.dump(data, f, ensure_ascii=False)


def write_file(file, message):
    logging.info(f"write '{message}' to '{file}'")
    output = open(file, "w")
    output.write(message)
    output.close()


def read_file(file):
    logging.info(f"read '{file}'")
    if os.path.exists(file):
        F = open(file, "r")
        content = F.read()
        F.close()
        logging.info(f"content : '{content}'")
        return content
    else:
        return ""


def send_event(data):
    rsp = requests.post("http://10.151.3.74:3300", json=data)
    return rsp


def is_hour_between(start=None, end=None, now=None):
    is_between = False

    if not now:
        t = datetime.now()
        now = t.hour
    is_between |= start <= now <= end
    is_between |= end < start and (start <= now or now <= end)

    return is_between


def send_sms(message="", to=""):
    return True
    from twilio.rest import Client

    if not to:
        to = "+8618621662567"
    if not message:
        message = "测试"
    # Find your Account SID and Auth Token at twilio.com/console
    # and set the environment variables. See http://twil.io/secure
    account_sid = "AC9058d4c11bfc88ac1c6b4ba33b1f9b4f"
    auth_token = "31505a33bd7b6ca3ce9afb438d627c94"
    client = Client(account_sid, auth_token)

    message = client.messages.create(body=message, from_="+15616930249", to=to)
    print("Message SID: {}".format(message.sid))


def check_pod_status(r, pwd="Nebula123$%^"):
    logging.info("%s" % r)
    logging.info("=" * 100)
    try:
        out = ssh_cmd(ip=r, cmd='docker ps -a |grep -v "Up\|CONTAINER" | wc -l', pwd=pwd)
        if out == "0\n":
            logging.info("check pod status success: all pods is ok")
            # print("ok")
            return True
        else:
            logging.info("check pod status fail: not all pods is ok")
            return False
    except:
        logging.info("connection failure")


def activate_license(ipaddress, type):
    # python3 run.py -i 10.151.5.205 -t t4 -s test_nebula_tools_111_upload_license -r 1 > /tmp/active_license.log 2>&1
    path = "/root/nebulatest"
    option = "-T"
    if ipaddress in config.standalone_ip[type]:
        cmd = f"cd {path}; PYTHONIOENCODING=utf-8 python3 run.py -i {ipaddress} -t {type} {option} upload_standalone_license -r 1 -o 1 -p /tmp/active  > /tmp/active_{ipaddress}_license.log 2>&1"
        run_cmd(cmd)
    else:
        cmd = f"cd {path}; PYTHONIOENCODING=utf-8 python3 run.py -i {ipaddress} -t {type} {option} upload_cloud_license -r 1 -o 1 -p /tmp/active > /tmp/active_{ipaddress}_license.log 2>&1"
        run_cmd(cmd)
    result = get_active_result(ipaddress)
    return result


def get_active_result(ipaddress):
    filepath = f"/tmp/active_{ipaddress}_license.log"
    with open(filepath, "r") as file:
        file_contents = file.readlines()
        for content in file_contents:
            if "OK" in content:
                return True


class Robot:
    URL = {"AI": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=4c0703fa-0cd3-4276-ad8b-e4c753ebbf57",
           "meet": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=b333e02b-ffec-4ec3-8dd3-88bf1af90a97",
           "ToB产品-2022":"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ed9b847b-02fe-460e-baa8-3519dc8b0a2c",
            "泛金融与企业数字化产品部":"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=d27f3c77-2696-43d0-9c98-c130dc4793d2",
            "22Y H2 产品周会":"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=49920d52-385d-4235-8a88-4275bc36b226",}

    def __init__(self, name):
        self.name = name

    def send_content(self, content):
        url = Robot.URL[self.name]
        headers = {"Content-type": "application/json"}
        data = {
            "msgtype": "text",
            "text": {
                "content": content,
                "mentioned_list": ["@all"]  # "513c2f38-b462-434a-9b36-0b63c35c75d5"
            }
        }
        requests.post(url=url, json=data, headers=headers)

    def deployment(self, ip, result=None, msg=None, package=None):
        url = Robot.URL[self.name]
        jenkins_url = "[点击访问](http://jenkins.infra.sensetime.com/)"
        if result == "部署失败" or result == "激活失败":
            color = "warning"
        else:
            color = "info"
        if package is None:
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "content": f"""Nebula-1.2.0-deployment<font color="{color}"> **{result}** </font>
                    > 服务器:<font color="comment"> {ip}</font>
                    > 部署Jenkins:<font color="comment"> {jenkins_url}</font>
                    > msg:<font color="comment"> {msg}</font>"""
                }
            }
        else:
            data = {
                "msgtype": "markdown",
                "markdown": {
                    "content": f"""Nebula-1.2.0-deployment<font color="{color}"> **{result}** </font>
                                > 服务器:<font color="comment"> {ip}</font>
                                > 全量包:<font color="comment"> {package}</font>
                                > 部署Jenkins:<font color="comment"> {jenkins_url}</font>
                                > msg:<font color="comment"> {msg}</font>"""
                }
            }
        requests.request("post",
                         url=url,
                         json=data)
