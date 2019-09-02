import os
import praw
import datetime
from notion.client import NotionClient

reddit = praw.Reddit(client_id='xxxxxxxxxxxxxx',
                     client_secret='xxxxxxxxxxxxxxxxxxxxxxxxxxx',
                     username='xxxxxxxx',
                     password='xxxxxxxx',
                     user_agent='xxxxxxxxxx')
savedItems = []
baselineUpdateItems = []
savedItemIndex = 0
isSavedItemInBaseLine = 0

client = NotionClient(
    token_v2="") #4N1
database = client.get_block("")

for savedItem in reddit.user.me().saved(limit=2000):
    savedItems.append(savedItem)

currentFolder = os.path.dirname(os.path.abspath(__file__))
currentFile = os.path.join(currentFolder, 'RedditGnome_Baseline.txt')
if os.path.isfile(currentFile):
    with open('RedditGnome_Baseline.txt', "r") as rgbfile:
        rgblist = rgbfile.readlines()
        for i in range(0, len(savedItems)):
            savedItemIndex = i
            if any(savedItems[i].fullname in line for line in rgblist):
                isSavedItemInBaseLine = 1
                break
            else:
                baselineUpdateItems.append(savedItems[i].fullname)

                row = database.collection.add_row()
                if isinstance(savedItems[i], praw.models.Submission):
                    row.body = savedItems[i].title[:10] + "..."
                    row.saved_item_type = "Submission"
                else:
                    row.body = savedItems[i].body[:10] + "..."
                    row.saved_item_type = "Comment"
                row.author = str(savedItems[i].author)
                row.date_created = datetime.datetime.utcfromtimestamp(savedItems[i].created_utc).strftime("%m-%d-%Y")
                row.subreddit = savedItems[i].subreddit.display_name
                row.url = "redd.it/" + savedItems[i].fullname[3:]
                row.date_saved = datetime.date.today().strftime("%m-%d-%Y")
    if savedItemIndex != 0 and isSavedItemInBaseLine == 1:
        with open('RedditGnome_Baseline.txt', "w") as rgbfile:
            for i in range(0, len(baselineUpdateItems)):
                rgbfile.write(baselineUpdateItems[i]+"\n")
else:
    for i in range(0, len(savedItems)):
        row = database.collection.add_row()
        if isinstance(savedItems[i], praw.models.Submission):
            row.body = savedItems[i].title[:10] + "..."
            row.saved_item_type = "Submission"
        else:
            row.body = savedItems[i].body[:10] + "..."
            row.saved_item_type = "Comment"
        row.author = str(savedItems[i].author)
        row.date_created = datetime.datetime.utcfromtimestamp(savedItems[i].created_utc).strftime("%m-%d-%Y")
        row.subreddit = savedItems[i].subreddit.display_name
        row.url = "redd.it/" + savedItems[i].fullname[3:]
        row.date_saved = datetime.date.today().strftime("%m-%d-%Y")
    with open('RedditGnome_Baseline.txt', "w") as rgbfile:
        for i in range(0, len(savedItems)):
            rgbfile.write(savedItems[i].fullname+"\n")


