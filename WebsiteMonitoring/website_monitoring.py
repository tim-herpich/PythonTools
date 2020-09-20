import requests
import time
from bs4 import BeautifulSoup
import smtplib
from email.message import EmailMessage

def recipient_list(): # list of e-mail addresses receiving update notfications
    return [
        # 'time.herpich@gmail.com',
            'tim.herpich@yandex.com']

def main():
    check_interval = 1  # in seconds
    url = "https://sites.google.com/view/na-wedding/pandemic-update"
    current_content = download_and_parse_html(url)
    time.sleep(check_interval)

    while True:

        new_content = download_and_parse_html(url)

        if current_content == new_content:
            print('No Changes.')
            time.sleep(check_interval)

        else:
            msg = EmailMessage()
            msg.set_content(
                'Dear all,\n\nWe just provided some updates regarding our wedding: https://sites.google.com/view/na-wedding/pandemic-update.\n\nKind regards,\nAsima & Nijat')
            msg['From'] = 'n.and.a.wedding.update@gmail.com'
            msg['To'] = recipient_list()
            msg['Subject'] = 'N&A wedding | Pandemic Update'
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login('n.and.a.wedding.update@gmail.com', '1234_abcd') # allow access from unsecure apps in google account settings
            server.send_message(msg)
            server.quit()
            current_content = new_content
            time.sleep(check_interval)

def download_and_parse_html(url):
    html = requests.get(url).content # retrieve html from url
    soup = BeautifulSoup(html, "html.parser") # parse html
    text = soup.find_all(text=True) # select text
    output = ''
    blacklist = ['[document]','html','span','style','div','script'] # blacklist unwanted items. Full list: set([t.parent.name for t in text])
    for item in text:
        if item.parent.name not in blacklist:
            output += '{} '.format(item)
    return output

if __name__ == '__main__':
    main()

