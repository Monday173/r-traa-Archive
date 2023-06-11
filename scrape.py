import praw
from praw.models import MoreComments
import sqlite3

CLIENT_ID = "6Q1o70efL87xwkivTYYpMg"
CLIENT_SECRET = "OPszAramvnbpu12RaXm134DqGjPDpA"

reddit_connection = praw.Reddit(client_id = CLIENT_ID,
                                client_secret = CLIENT_SECRET,
                                user_agent = "r/traa Archival Project (Testing version 1.0) | u/Monday_173")

sub = reddit_connection.subreddit("traaaaaaannnnnnnnnns")

conn = sqlite3.connect("r.traa.db")
cur = conn.cursor()

def setup_db():
    cur.execute("CREATE TABLE posts(ID, Title, Text, NumComments, Score, URL)")
    conn.commit()

def get_post_by_id(id):
    res = cur.execute(f"SELECT * FROM posts WHERE ID='{id}'")
    return res.fetchone()

def insert_post(post):
    if get_post_by_id(post["ID"]):
        print(f"Post {post['ID']} already in database, updating...")
        cur.execute(f"UPDATE posts SET Title=\"{post['Title']}\", Text=\"{post['Text']}\", NumComments={post['NumComments']}, Score={post['Score']}, URL=\"{post['URL']}\" WHERE ID='{post['ID']}'")
        conn.commit()
    else:
        print(f"Inserting {post['ID']} into database.")
        # print(f"INSERT INTO posts VALUES ('{post['ID']}', '{post['Title']}', '{post['Text']}', {post['NumComments']}, {post['Score']}, '{post['URL']}')")
        cur.execute(f"INSERT INTO posts VALUES (\"{post['ID']}\", \"{post['Title']}\", \"{post['Text']}\", {post['NumComments']}, {post['Score']}, \"{post['URL']}\")")
        conn.commit()

def print_sub_info(sub):
    print(f"Name:        {sub.display_name}")
    print(f"Title:       {sub.title}")
    print(f"Description: {sub.description}")

def get_top(sub):
    res = []

    for post in sub.top(time_filter="year"):
        res.append(post)

    return res

def get_hot(sub):
    res = []

    for post in sub.hot(limit=1000):
        res.append(post)

    return res

def get_comments(post_id):
    submission = reddit_connection.submission(id=post_id)
    res = []

    comments = submission.comments[:]

    while comments:
        comment = comments.pop(0)
        res.append(comment.body)

        comments.extend(comment.replies)

    return res

def to_dict(post):
    res = {}
    res["Title"] = post.title.replace("'", "&#39;").replace('"', "&#34;")
    res["Text"] = post.selftext.replace("'", "&#39;").replace('"', "&#34;")
    res["ID"] = post.id
    res["NumComments"] = post.num_comments
    res["Score"] = post.score
    res["URL"] = post.url.replace("'", "&#39;").replace('"', "&#34;")

    return res

res = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='posts'")
if res.fetchone() == None:
    setup_db()

posts = get_hot(sub)
for post in posts:
    insert_post( to_dict(post) )

# print(posts[0])
# print( get_comments( to_dict(posts[0])["ID"] ) )

print("Scrape complete.")