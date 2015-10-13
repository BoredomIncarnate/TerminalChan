#!/bin/python

from urllib.request import urlopen
import urllib.request
import argparse
import os
import json
import re
import sys

''' todos
    1. make helper objects
    2. make replies and posts in different arrays
'''

''' Methods
    1.  main
    2.  GetCatalog
    3.  GetMainPosts
    4.  GetTims
    5.  GetFilenames
    6.  GetExtensions
    7.  GetComments
    8.  DownloadImgs
    9.  ShowPostsWithImgs
    10. FormatStr
    11. ShowImg
    12. ShowAllImgs
    13. ClearTmp
    14. ViewCatalog
    15. ViewPage
'''

#global variables
pages     = []
mainPosts = []
tims      = []
filenames = []
exts      = []
comments  = []

#parser options
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--board", help="board you wish to lurk")
    parser.add_argument("-p", "--page", help="page you wish to visit")
    args = parser.parse_args()
    if args.board:
        if args.page:
            ViewPage(args.board, args.page)
        else:
            ViewCatalog(args.board)
    else:
        print("please provide a board with the flag -b <value>")
        sys.exit(1)

def GetCatalog(board):
    print("getting catalog for /{}/".format(board))
    try:
        url=urlopen("https://a.4cdn.org/{}/catalog.json"
                .format(board)).read()
    except ex:
        print("ERROR GETTING CATALOG")
        sys.exit(1)
    print("done!")
    return json.loads(url.decode())

def ViewCatalog(board):
    cat = GetCatalog(board)
    GetMainPosts(cat)
    GetTims(mainPosts)
    GetFilenames(mainPosts)
    GetExtensions(mainPosts)
    GetComments(mainPosts)
    DownloadImgs(board)
    ShowPostsWithImgs()
    ClearTmp()
    return None

def GetPage(board, page):
    print("getting page: {} on /{}/".format(page, board))
    try:
        url=urlopen("https://a.4cdn.org/{}/{}.json"
                .format(board, page)).read()
    except ex:
        print("ERROR GETTING PAGE")
        sys.exit(1)
    print("done!")
    return json.loads(url.decode())

def ViewPage(board, pageNum):
    page = GetPage(board, pageNum)
    GetPagePosts(page)
    GetTims(mainPosts)
    GetFilenames(mainPosts)
    GetExtensions(mainPosts)
    GetComments(mainPosts)
    DownloadImgs(board)
    ShowPostsWithImgs()
    ClearTmp()
    return None

def GetCatalogPosts(catalog):
    print("Fetching first major post of every thread...")
    for page in catalog:
       for post in page["threads"]:
           mainPosts.append(post)
    print("done!")
    return None

def GetPagePosts(page):
    print("Fetching page posts...")
    for thread in page["threads"]:
        for post in thread["posts"]:
            mainPosts.append(post)
            print(post)
    print("done!")
    return None

def GetTims(posts):
    # grab post["tim"] from each post
    # store in global tims[]
    print("getting img tims...")
    for post in posts:
        if 'tim' in post:
            print(post["tim"])
            tims.append(post["tim"])
        else:
            tims.append("n/a")
    print("done!")
    return None

def GetFilenames(posts):
    # grab post[filename]
    # store filename into filenames[] global
    print("getting filenames of imgs...")
    for post in posts:
        if 'filename' in post:
            filenames.append(post["filename"])
        else:
            filenames.append("n/a")
    print("done!")
    return None

def GetExtensions(posts):
    # grab post[ext]
    # store ext into exts[] global
    print("getting extensions of imgs...")
    for post in posts:
        if 'ext' in post:
            exts.append(post["ext"])
        else:
            exts.append("n/a")
    print("done!")
    return None

def GetComments(posts):
    # grab post["com"]
    # store com into comments[] global
    print("collecting comments...")
    for post in posts:
        if 'com' in  post:
            comments.append(FormatStr(post["com"]))
        else:
            comments.append("n/a")
    print("done!")
    return None

def FormatStr(raw):
    # replace <br> or <br /> with \n
    # replace &codes with their actual counter parts
    # scrub out the rest of the html tags and their attrs
    fmt = re.sub('<br>', '\n', raw)
    return fmt

def DownloadImgs(board):
    print("Downloading imgs...")
    for i in range(0, len(tims)):
        if  (
                filenames[i] != "n/a" and tims[i] != "n/a" and
                exts[i] != "n/a"
            ):
            urllib.request.urlretrieve("http://i.4cdn.org/{}/{}{}"
                    .format(board, tims[i], exts[i]),
                    "tmp/{}{}".format(filenames[i], exts[i]))
    print("done!")
    return None

def ShowImg(filename, ext):
    os.system("imgcat tmp/{}{}".format(filename, ext))
    return None

def ShowPostsWithImgs():
    # fetch comment from each post
    # fetch img associated w/ post
    # show in order as they come
    for i in range(0, len(mainPosts)):
        print(comments[i])
        ShowImg(filenames[i], exts[i])
        input("Press Enter to continue...")
    return None

def ShowAllImgs():
    for i in range(0, len(filenames)):
        ShowImg(filenames[i], exts[i])
        input("Press Enter to continue...")
    return None

def ClearTmp():
    # remove all imgs from tmp/*
    print("Clearing out tmp...")
    os.system("rm -Rfv tmp/*")
    print("done!")
    return None

if __name__ == "__main__":
    main()
