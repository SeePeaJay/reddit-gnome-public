#!/usr/bin/python3.6
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

for savedItem in reddit.user.me().saved(limit=2000):
    savedItems.append(savedItem)

currentFolder = os.path.dirname(os.path.abspath(__file__))
currentFile = os.path.join(currentFolder, 'redditgnomebaseline.txt')
if os.path.isfile(currentFile):
    with open('redditgnomebaseline.txt', "r") as rgbfile:
        rgblist = rgbfile.readlines()
        for i in range(0, len(savedItems)):
            savedItemIndex = i
            if any(savedItems[i].fullname in line for line in rgblist):
                isSavedItemInBaseLine = 1
                break
            else:
                baselineUpdateItems.append(savedItems[i].fullname)
                with open('redditgnomehighlight.txt', "a") as rghfile:
                    if isinstance(savedItems[i], praw.models.Submission):
                        rghfile.write(savedItems[i].title[:10]+"... | Submission | " + savedItems[i].subreddit.display_name +
                                      " | "+"redd.it/"+savedItems[i].fullname[3:]+" | "+datetime.date.today().strftime("%m-%d-%Y")+"\n")
                    else:
                        rghfile.write(savedItems[i].body[:10].strip("\n")+"... | Comment | "+savedItems[i].subreddit.display_name +
                                      " | "+"redd.it/"+savedItems[i].fullname[3:]+" | "+datetime.date.today().strftime("%m-%d-%Y")+"\n")
    if savedItemIndex != 0 and isSavedItemInBaseLine == 1:
        with open('redditgnomebaseline.txt', "w") as rgbfile:
            for i in range(0, len(baselineUpdateItems)):
                rgbfile.write(baselineUpdateItems[i]+"\n")
else:
    with open('redditgnomehighlight.txt', "w") as rghfile:
        rghfile.write(
            "Body ........ | Saved Item Type | Subreddit | URL | Saved Date\n")
        for i in range(0, len(savedItems)):
            if isinstance(savedItems[i], praw.models.Submission):
                rghfile.write(savedItems[i].title[:10]+"... | Submission | "+savedItems[i].subreddit.display_name +
                              " | "+"redd.it/"+savedItems[i].fullname[3:]+" | "+datetime.date.today().strftime("%m-%d-%Y")+"\n")
            else:
                rghfile.write(savedItems[i].body[:10].strip("\n")+"... | Comment | "+savedItems[i].subreddit.display_name +
                              " | "+"redd.it/"+savedItems[i].fullname[3:]+" | "+datetime.date.today().strftime("%m-%d-%Y")+"\n")
    with open('redditgnomebaseline.txt', "w") as rgbfile:
        for i in range(0, len(savedItems)):
            rgbfile.write(savedItems[i].fullname+"\n")
