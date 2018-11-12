#!/usr/bin/env python
# -*-coding:utf-8-*-
import re
import requests
import json
import os.path

class Instagram(object):
    Patter = re.compile(r'<script type=\"text/javascript\">\s?window\._sharedData\s?=\s?(.*);</script>')

    def __init__(self, basePATH, url):
        self.basePath = basePATH
        self.url = url
        self.session = requests.session()

    def fetchHTML(self):
        HTMLResponse = self.session.get(self.url)
        encoding = HTMLResponse.apparent_encoding
        htmlContent = HTMLResponse.content.decode(encoding)
        return htmlContent

    def parseImageURL(self):
        content = self.fetchHTML()
        re_search = self.Patter.search(content)
        if re_search:
            string = re_search.groups()[0]
            instagram_data = json.loads(string)
            for k, v in instagram_data.items():
                if k == 'entry_data':
                    postPageList = v['PostPage']
                    if isinstance(postPageList, list):
                        for graphDict in postPageList:
                            return graphDict['graphql']['shortcode_media']['display_url']

    def fetchImage(self):
        imageURL = self.parseImageURL()
        filename = imageURL.rsplit('/', 1)[1]
        image_res = self.session.get(imageURL)
        absPath = os.path.join(self.basePath,"img", filename)
        with open(absPath, 'wb') as f:
            f.write(image_res.content)
        self.session.close()
        return absPath

if __name__ == '__main__':
    url = "https://www.instagram.com/p/BpVkCn8ncXS/?utm_source=ig_share_sheet&igshid=j394df17k2sa"
    from settings import BASEPATH
    insObj = Instagram(BASEPATH,url)
    insObj.fetchImage()