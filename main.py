#!/usr/bin/python3.5
# -*-coding:utf-8 -*-
import optparse
import urllib.request
from urllib.error import HTTPError, URLError
import re
import threading
import datetime

try:
    from lxml import etree
except ImportError:
    from lxml import etree
    message = '''
    Please intall lxml first!
    For python v2 -- pip install lxml
    For python v3 -- pip3 install lxml
    '''
    exit(message)


class Colors:
    blue = '\033[94m'
    green = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    end = '\033[0m'
    bold = '\033[1m'
    underline = '\033[4m'


# Checking options parameters
class DataChecker():

    def __init__(self):
        self.option_parser = optparse.OptionParser('usage %script -u <target_link> -l <parsing_level>')
        # Adding parser's options
        self.option_parser.add_option('-u', dest='target_link', type='string')
        self.option_parser.add_option('-l', dest='parsing_level', type='int')
        # Setting up option variables
        (self.options, self.args) = self.option_parser.parse_args()
        self.target_link = self.options.target_link.lower()
        self.parsing_level = self.options.parsing_level

        # Checking for empty parameters
        self.check = (self.target_link, self.parsing_level)
        if not all(self.check):
            print(self.option_parser.usage)
            exit(0)
        self.url_data = self.target_link.split('/')

        # Extracting protocol amd domain name
        self.protocol = self.url_data[0]
        self.domain = self.url_data[2]


class Crawler():

    '''
        Main class
        Methods:
        1) link_checker -- checks absolute/relative links existence, modify relative links to absolute
        2) link_extractor -- extract all links via html page
        3) recursive_link_crawler -- recursive link crawler/collector
        4) email_crawler -- collect emails and prints them out
    '''

    def __init__(self):
        self.check = DataChecker()
        self.protocol = self.check.protocol
        self.domain = self.check.domain
        self.extracted_links = []
        self.extracted_emails = []
        self.target_url = self.check.target_link
        self.level = 1
        self.max_level = self.check.parsing_level
        self.email_regex = re.compile(r'[\w\-][\w\-\.]+@[\w\-][\w\-]+\.+[a-zA-Z]{1,4}', re.MULTILINE | re.IGNORECASE)
        self.ignored_ext = ['jpg', 'png', 'ico', 'css', 'js', 'css', 'rss']

    # Checking absolute/relative links existence, modifying relative links to absolute
    def link_checker(self, url):
        input_url = url.split('/')
        if input_url[0] != 'https:':
            if input_url[0] != 'http:':
                mod_url = "%s//%s%s" % (self.protocol, self.domain, url.strip('\\'))
                return mod_url
            else:
                return url
        else:
            return url

    # Method for link extraction
    def link_extractor(self, link):
        # Ignoring links with extensions from list
        try:
            # Sending fake headers to prevent blocking
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
            d = urllib.request.Request(link, None, headers=headers)
            u = urllib.request.urlopen(d, timeout=10)
            # Decoding from binary ignoring unsupported symbols
            page = u.read().decode('utf-8', errors='ignore')
            try:
                # Parsing page with etree
                e = etree.HTML(page)
                # Extracting all links with xpath
                h = e.xpath('//*[@href]')
                # Using generator for link check/recording
                arr = [self.link_checker(link.attrib.get('href', None)) for link in h if not link.attrib.get('href', None).split('.')[-1] in self.ignored_ext]
                # Removing duplicates returning clear list
                return set(arr)
            except (AttributeError, ValueError):
                pass
        except (HTTPError, URLError, ConnectionResetError):
            # Page not found error
            print('%s: not found' % link)
            pass

    # Recursive page crawling
    def recursive_link_crawler(self, url, level, max_level):
        # Extracting links from a page
        url_list = self.link_extractor(url)
        # Checking crawling level
        if level <= max_level:
            if url_list:
                for l in url_list:
                    # Checking duplicates existence
                    if l not in self.extracted_links:
                        print(l)
                        # Recording links to list
                        self.extracted_links.append(l)
                        # Moving on next node
                        self.recursive_link_crawler(l, level+1, max_level)
            else:
                print(Colors.warning + 'There are no links on this page...skipping' + Colors.end)
                pass

    # Extracting e-mails from html pages
    def email_crawler(self, url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
        try:
            d = urllib.request.Request(url, None, headers=headers)
            u = urllib.request.urlopen(d, timeout=10)
            page = u.read().decode('utf-8', errors='ignore')
            for l in page.split('\n'):
                email = re.findall(self.email_regex, l)
                if email:
                    for em in email:
                        email_data = em.split('.')
                        if not email_data[-1] in self.ignored_ext:
                            if em not in self.extracted_emails:
                                self.extracted_emails.append(em)
                                print(Colors.bold + 'Found: ' + Colors.end + Colors.blue + em + ' ' + Colors.end + 'at ' + str(datetime.datetime.now()))
        except (HTTPError, URLError, ConnectionResetError):
            pass


# Executor class
class Executor():
    def __init__(self):
        c = Crawler()
        c.recursive_link_crawler(c.target_url, c.level, c.max_level)
        # Creating threads
        threads = [threading.Thread(target=c.email_crawler, args=(url,)) for url in c.extracted_links]
        try:
            [th.start() for th in threads]
            [th.join() for th in threads]
        except:
            print(Colors.warning + 'Unexpected thread error' + Colors.end)

if __name__ == '__main__':
    e = Executor()

