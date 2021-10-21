# 文件名固定，全局有效
import pytest,configparser, os
from utils.zipfileUtil import zipDir
from config.emailConfig import EmailConfig
from email.mime.multipart import MIMEMultipart

config = configparser.ConfigParser()
config.read("./config/config.ini", encoding="utf-8")

def send_mail():
    """
    发送邮件
    :return:
    """
    e = EmailConfig()
    message = MIMEMultipart()
    e.add_content(message)
    e.add_attachment(config["filepath"]["testcase_filepath"], message)
    e.add_attachment(config["filepath"]["log_filepath"], message)

    # 压缩报告
    zipDir(r"C:\Users\zhang.sun\APItest\utils\excelUtil.py", r"C:\Users\zhang.sun\APItest\utils\excelUtil.zip")
    # 添加压缩文件
    e.add_attachment(r"C:\Users\zhang.sun\APItest\utils\excelUtil.zip", message)
    e.send_mail(message)

@pytest.fixture(scope="session", autouse=True)
def start_and_end():
    print("自动化测试开始")
    yield

    # 生成报告
    os.system("allure generate ./report/allure_results --clean -o ./report/allure_reports")

    # 发送邮件
    send_mail()
    print("自动化测试结束")
