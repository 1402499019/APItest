import smtplib, os, time, configparser
from utils.excelUtil import Excel
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from email.mime.application import MIMEApplication

config = configparser.ConfigParser()
config.read("./config.ini", encoding="utf-8")


class EmailConfig:
    sender = "1402499019@qq.com"  # 发件人邮箱
    receiver = "553497396@qq.com"  # 收件人

    # 发送邮件
    def send_mail(self, message):
        try:
            # 发件人邮箱，用于登录
            username = "1402499019@qq.com"
            # 密码为授权码，而非qq密码
            password = "sdrvutrlcxtrbaaf"

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)
            # server.connect()
            server.login(username, password)
            server.sendmail(self.sender, [self.receiver,], message.as_string())  # 发件人、收件人、内容
            server.quit()  # 关闭连接
        except smtplib.SMTPException:
            print("发送邮件失败！")

    # 添加正文
    def add_content(self, message):
        # 主题
        message["Subject"] = Header("测试报告", "utf-8")
        message["From"] = self.sender
        message["To"] = self.receiver

        # 主体内容， 这里是HTML格式，可插图片
        body = f"""<h3>Dear all</h3>
                    机器人盘点专家{time.strftime("%Y-%m-%d")}测试结果：
                    <br><img src="cid:image1"></br>
                    
                """
        mail_body = MIMEText(body, _subtype="html", _charset="utf-8")
        message.attach(mail_body)
        excel = Excel(config["filepath"]["testcase_filepath"])

        # 结果截图
        screenshot = excel.excel_screenshot()

        # 读取图片，将图片添加到正文中
        with open(screenshot, "rb") as image:
            images = MIMEImage(image.read())
        images.add_header("Content-ID","<image1>")
        message.attach(images)

    # 添加附件
    def add_attachment(self, attachment, message):
        with open(attachment, "rb") as f:
            attach = MIMEApplication(f.read())
            attach.add_header("Content-Disposition", "attachment", filename=os.path.basename(attachment))
        message.attach(attach)


if __name__ == '__main__':
    e = EmailConfig()
    message = MIMEMultipart()
    e.add_content(message)
    e.add_attachment(config["filepath"]["testcase_filepath"], message)
    e.send_mail(message)