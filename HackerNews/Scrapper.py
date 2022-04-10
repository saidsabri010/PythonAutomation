import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime


class HN:
    now = datetime.datetime.now()
    content = ''
    SERVER = 'smtp.gmail.com'
    PORT = 587
    FROM = 'example@gmail.com'
    TO = 'example@gmail.com'
    PASS = '*******'

    def getUrl(self):
        html_text = requests.get('https://news.ycombinator.com/').text
        soup = BeautifulSoup(html_text, 'lxml')
        return soup

    def extract_news(self):
        temp_content = ''
        temp_content += ('<b>HN Top Stories:</b>\n' + '<br>' + '-' * 50 + '\n' + '<br>')
        soup = self.getUrl()
        title = soup.findAll('a', class_='titlelink')
        for i, tag in enumerate(title):
            temp_content += ((str(i + 1) + ' :: ' + tag.text + "\n" + '<br>') if tag.text != 'More' else '')
        return temp_content

    def fill_content(self):
        self.content += self.extract_news()
        return self.content

    def email_auth(self):
        msg = MIMEMultipart()
        msg['Subject'] = 'Top Nes Stories HN ' + ' ' + str(self.now.day) + '-' + str(self.now.year)
        msg['From'] = self.FROM
        msg['To'] = self.TO
        return msg

    def send_email(self):
        msg = self.email_auth()
        msg.attach(MIMEText(self.fill_content(), 'html'))
        print('Initiating Server...')
        server = smtplib.SMTP(self.SERVER, self.PORT)
        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(self.FROM, self.PASS)
        server.sendmail(self.FROM, self.TO, msg.as_string())
        print('Email Sent...')
        server.quit()



