from utils import Robot

if __name__ == '__main__':
    robot = Robot("AI")
    content = "会议即将开始，请大家上线了!会议号:9000934712"
    robot.send_content(content)
