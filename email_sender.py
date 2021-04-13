#from pprint import pprint

import requests

from bs4 import BeautifulSoup

import smtplib

from email.message import EmailMessage

'''get a list of the latest news with more than 100 points'''

url = 'https://news.ycombinator.com/news'

res = requests.get(url)

soup = BeautifulSoup(res.text, 'html.parser')

links = soup.select('.storylink')

subtext = soup.select('.subtext')

hacker_news_top_list = []


def sort_stories_by_votes(hacker_news_top_list):

    return sorted(hacker_news_top_list, key=lambda k: k['votes'], reverse=True)


def create_custom_hackernews(links, subtext):

    for count, item in enumerate(links):

        title = item.getText()

        href = item.get('href', None)

        vote = subtext[count].select('.score')

        if len(vote):

            points = int(vote[0].getText().replace(' points', ''))

            if points > 99:

                hacker_news_top_list.append({'title': title, 'link': href, 'votes': points})

    return sort_stories_by_votes(hacker_news_top_list)


create_custom_hackernews(links, subtext)
''''
Replace enter_to_address with receiving email, your_username with your real email, your_password with your real password ''''

email = EmailMessage()

email['from'] = 'Smarter You'

email['to'] = 'enter_to_address'

email['subject'] = 'list  of news from hacker news website'

email.set_content(f'{hacker_news_top_list}')

with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:

    smtp.ehlo()
    
    smtp.starttls()
    
    smtp.login('your_email', 'your_password')
    
    smtp.send_message(email)
    
    print("Email send successfully")
