# -*- coding: utf-8 -*-

import feedparser
from HTMLParser import HTMLParser
from utils import Cache
from facebook import FacebookNotifier
from config import GMAIL_USER, GMAIL_PASSWORD, FB_GROUPID

class FeedContentParser(HTMLParser):
    ENTITIES = {
        'agrave': u'à', 'acirc':  u'â', 
        'eacute': u'é', 'egrave': u'è', 'ecirc': u'ê',
        'icirc': u'î' , 'ocirc':  u'ô', 'ucirc': u'û',
        'ccedil': u'ç', 'rsquo': u"'",  'mdash': u'--'
    }

    def __init__(self):
        HTMLParser.__init__(self)
        self.text = u''

    def handle_endtag(self, tag):
        if tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'div', 'p', 'br'):
           if self.text[-1] != '\n':
                self.text += '\n'

    def handle_data(self, text):
        self.text += text

    def handle_entityref(self, name):
        self.text += self.ENTITIES.get(name, '')

if __name__ == '__main__':
    with Cache('infof209-feeds.json') as cache:
        for i in range(1,3):
            feedurl = "http://infof209.weebly.com/%d/feed"%(i)
            feed = feedparser.parse(feedurl)
            if not feedurl in cache:
                cache[feedurl] = []
            for item in feed['entries']:
                link = item['link']
                if link not in cache[feedurl]:
                    parser = FeedContentParser()
                    parser.feed(item['content'][0]['value'])
                    message = parser.text + '\n' + link
                    fb = FacebookNotifier(GMAIL_USER, GMAIL_PASSWORD)
                    fb.post_to_group(FB_GROUPID, message)
                    cache[feedurl].append(link)
                    print link