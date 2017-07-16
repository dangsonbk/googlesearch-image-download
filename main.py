
# coding: utf-8

# In[ ]:

#Searching and Downloading Google Images/Image Links

#Import Libraries

#coding: UTF-8

import time       #Importing the time library to check the time of code execution
import sys    #Importing the System Library
import os
import urllib2
from urllib2 import Request, urlopen
from urllib2 import URLError, HTTPError
import re

########### Edit From Here ###########

#This list is used to search keywords. You can edit this list to search for google images of your choice. You can simply add and remove elements of the list.
search_keyword = ['giang mai']
search_limit = 4
GOOGLESEARCHLINK = 'https://www.google.com/search?q={}&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
########### End of Editing ###########

#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    try:
        headers = {}
        headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
        req = urllib2.Request(url, headers = headers)
        response = urllib2.urlopen(req)
        page = response.read()
        return page
    except:
        return"Page Not found"

#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        return content_raw, end_content

# Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            regex = re.search("[-\w\.]+\.(?:jpg|png)", item)
            if regex:
                items.append(item)      # Append all the links in the list named 'Links'
            page = page[end_content:]
    return items

############## Main Program ############
def main():
    for keyword in search_keyword:
        items = []
        print ("Searching with keyword: {}".format(keyword))

        # create search keyword directory
        outputFoler = keyword.replace(" ", "")
        try:
            os.makedirs(outputFoler)
        except OSError, e:
            if e.errno != 17:
                raise
            pass

        keyword = keyword.replace(' ','%20')

        raw_html =  (download_page(GOOGLESEARCHLINK.format(keyword)))
        time.sleep(0.1)
        items = items + (_images_get_all_items(raw_html))
        print ("Total Image Links = "+str(len(items)))

        info = open('{}.txt'.format(outputFoler), 'w')
        for _item in items:
            info.write(_item + "\n")
        info.close()

        print ("Starting Download...")

        for _item in items[:search_limit]:

            try:
                regex = re.search("[-\w\.]+\.((?:jpg|png))", _item)
                if regex:
                    r = urllib2.urlopen(_item)
                    f = open('{}/{}'.format(outputFoler, regex.group(0)), 'wb')
                    f.write(r.read())
                    f.close()
                    print("Downloaded: " + regex.group(0))

            except IOError:
                print("IOError on image ")
            except HTTPError as e:
                print("HTTPError"+str(k))
            except URLError as e:
                print("URLError "+str(k))

    print("Everything downloaded!")

if __name__ == '__main__':
    main()