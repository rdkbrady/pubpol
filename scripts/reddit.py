import re
from datetime import datetime
import psycopg2
import praw
from dotenv import load_dotenv
from os import getenv
load_dotenv()

reddit = praw.Reddit(
     client_id=getenv('client_id'),
     client_secret=getenv('client_secret'),
     user_agent=getenv('user_agent')
)

conn = psycopg2.connect("postgres://postgres:postgres@127.0.0.1:5432/pubpol")
cursor = conn.cursor()

def parse_post(post):
    domain = re.findall('//([^/]*)/', post.url)
    if len(domain) == 0:
        return None
    else: 
        json = {
            'id': post.id,
            'subreddit': post.subreddit.display_name,
            'domain': domain[0],
            'created_at': datetime.utcfromtimestamp(post.created_utc),
            'title': post.title,
            'url': re.findall('^([^?]*)', post.url)[0],
            'score': post.score,
            'ratio': post.upvote_ratio,
            'engagement': post.num_comments,
            'permalink': ''.join(['https://www.reddit.com',post.permalink])
        }
        return json

def insert_post(post):
    query = """
    INSERT INTO reddit(
        id, 
        subreddit,
        domain, 
        created_at, 
        title, 
        url, 
        score, 
        ratio, 
        engagement, 
        permalink
    ) VALUES(
        %(id)s, 
        %(subreddit)s,         
        %(domain)s, 
        %(created_at)s,
        %(title)s,
        %(url)s,
        %(score)s,
        %(ratio)s,
        %(engagement)s,
        %(permalink)s
    ) ON CONFLICT (id)
    DO NOTHING
        
    """
    try:
        cursor = conn.cursor()
        cursor.execute(query, parse_post(post))
        conn.commit()
    except Exception as e: 
        print (e)
        print(parse_post(post))
        
def scrape_sub(subreddit):
    posts = list(reddit.subreddit(subreddit).hot(limit=1000))
    for post in posts:
        if parse_post(post):
            insert_post(post)
            
def scrape_political():
    scrape_sub('worldnews')
    scrape_sub('news')
#    scrape_sub('worldpolitics') # this sub is like 4chan now. it's not even political.
    scrape_sub('politics')
    scrape_sub('business')
    scrape_sub('Economics')
    scrape_sub('environment')
    scrape_sub('worldnews')
    scrape_sub('uspolitics')
    scrape_sub('AmericanPolitics')
    scrape_sub('Libertarian')
    scrape_sub('Anarchism')
    scrape_sub('democrats')
    scrape_sub('progressive')
    scrape_sub('conservative')
    scrape_sub('Liberal')
    scrape_sub('socialism')
    scrape_sub('Republican')
    scrape_sub('dsa')
    scrape_sub('Anarcho_Capitalism')
    scrape_sub('LibertarianLeft')
    scrape_sub('alltheleft')
    scrape_sub('Capitalism')
    scrape_sub('conservatives')
    scrape_sub('alltheleft')
    scrape_sub('neoliberal')