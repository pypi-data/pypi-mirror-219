#!/usr/bin/env python3

# -*- coding: utf-8 -*-

name = 'tumblr_2_album'

from telegram_util import AlbumResult as Result
from bs4 import BeautifulSoup
from tumdlr import downloader
import cached_url
from contextlib import contextmanager
import sys, os

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

def getImgs(content):
    soup = BeautifulSoup(content, 'html.parser')
    has_video = False
    for item in soup.find_all('source'):
        if item.get('type') != 'video/mp4':
            continue
        if not item.get('src'):
            continue
        has_video = True
        yield item['src']
    if not has_video:
        for item in soup.find_all('img'):
            yield item['src']

def getImgsJson(content):
    for photo in content:
        yield photo['original_size']['url']

def preDownload(img):
    filename = cached_url.getFilePath(img)
    if os.path.exists(filename):
        return
    # seems this is not silent
    with suppress_stdout():
        downloader.download(img, filename, silent=True)

def getText(content):
    soup = BeautifulSoup(content, 'html.parser')
    for item in soup.find_all('a', class_='tumblr_blog'):
        item.decompose()
    for tag in ['figure', 'img']:
        for item in soup.find_all(tag):
            item.decompose()
    lines = []
    for item in soup.find_all():
        if item.name not in ['p', 'li']:
            continue
        line = item.text.strip('\u200b').strip()
        if len(line) > 2:
            lines.append(line)
    return '\n\n'.join(lines)

def getBlogNameAndPostId(url):
    blog_name = url.split('/')[2].split('.')[0]
    if blog_name == 'www':
        blog_name = url.split('/')[3]
    post_id = int(url.strip('/').split('/')[-1])
    return blog_name, post_id

def get(client, url):
    result = Result()
    result.url = url
    blog_name, post_id = getBlogNameAndPostId(url)
    content = client.posts(blog_name, id=post_id)['posts'][0]
    result.video = content.get('video_url')
    result.cap_html_v2 = getText(content.get('caption', '')) or getText(content.get('body', '')) or content['summary']
    result.imgs = list(getImgsJson(content.get('photos', []))) or list(getImgs(content.get('body', '')))
    for img in result.imgs:
        preDownload(img)
    return result