'''
Searches Twitter for shared secret.ly URLs, visits the URLs,
pulls out the data, makes the data seachable and voteable.
Should run every 30 seconds
'''

import twitter
import bitly_api
import requests
import bs4
import os
import sys
from secretkeeper.models import get_secrets, put_secret, secret_exists, \
                                increment_positive_count

BITLY_ACCESS_TOKEN = os.environ['BITLY_ACCESS_TOKEN']
TWITTER_CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
TWITTER_CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
TWITTER_ACCESS_TOKEN_KEY = os.environ['TWITTER_ACCESS_TOKEN_KEY']
TWITTER_ACCESS_TOKEN_SECRET = os.environ['TWITTER_ACCESS_TOKEN_SECRET']


# init twitter and bitly
api = twitter.Api(consumer_key=TWITTER_CONSUMER_KEY,
                  consumer_secret=TWITTER_CONSUMER_SECRET,
                  access_token_key=TWITTER_ACCESS_TOKEN_KEY,
                  access_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

bitly = bitly_api.Connection(access_token=BITLY_ACCESS_TOKEN)

# Clean up and normalize URLs
def clean_url(gross_url):    
    if 'bit.ly' in gross_url:
        gross_url = expand_bitly(gross_url)

    if 'http://' in gross_url:
        gross_url = gross_url.replace('http://','https://')

    if '//secret.ly'in gross_url:
        gross_url = gross_url.replace('//secret.ly','//www.secret.ly')

    cleaned_url = gross_url.encode('ascii', 'ignore')
    cleaned_url = cleaned_url.split('?')[0]

    return cleaned_url

# Expand bit.ly URLs
def expand_bitly(bitly_url):
    expanded_url = bitly.expand(shortUrl=bitly_url)
    long_url = expanded_url[0][u'long_url']
    return long_url    

# Store last tweet id
def store_last_tweetid(tweetid):
    f = open('tweetstorage', 'w')
    f.write(str(tweetid))
    f.close()

# Retrieve last tweet id
def retrieve_last_tweetid():
    f = open('tweetstorage', 'r')
    tweet_id = f.read()
    return int(tweet_id)

# Search Twitter for secret.ly URLs
def twitter_search():
    results = api.GetSearch(term='secret.ly/p/', result_type='recent', \
                            count=30, since_id=retrieve_last_tweetid())
    if len(results) > 0:
        store_last_tweetid(results[-1].id)
        links = []
        for result in results:
            this_url = result.urls[0].expanded_url
        
            this_url = clean_url(this_url)

            links.append(this_url)
    else:
        links = ['No new tweets']

    return links

# Visit URL, retrieve html
def get_html(secret_url):
    response = requests.get(secret_url)
    html = response.text
    return html

# Parse html for data
def parse_html(html):
    data = bs4.BeautifulSoup(html)
    text = data.find_all('p', class_='secret-message')[0].get_text()
    text = text.strip()
    return text

# Database magic
def database_magic(link):
    if secret_exists(link):
        pass
    else:
        sys.stdout.write(str(link))
        text = parse_html(get_html(link))
        if text != '':
            put_secret(link, text)   

def main():
    links = twitter_search()
    if links[0] == 'No new tweets':
        sys.stdout.write(str(links[0]))
    else:
        for link in links:
            if 'secret.ly' in link:
                database_magic(link)



if __name__ == '__main__':
    main()
