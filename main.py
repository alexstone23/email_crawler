#!/home/spartan/PycharmProjects/page_parser/bin/python3.5
# -*-coding:utf-8 -*-
import sys
import optparse
from lxml import etree
import urllib.request
from urllib.error import HTTPError


class DataChecker():

    '''
        Checking options parameters
    '''

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
    def __init__(self):
        self.check = DataChecker()
        self.protocol = self.check.protocol
        self.domain = self.check.domain
        self.extracted_links = []
        self.target_url = self.check.target_link

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
        ignored_links = ['jpg', 'png', 'ico', 'css', 'js', 'css', 'rss']
        try:
            # Sending fake headers to prevent blocking
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'}
            d = urllib.request.Request(link, None, headers=headers)
            u = urllib.request.urlopen(d)
            # Decoding from binary ignoring unsupported symbols
            page = u.read().decode('utf-8', errors='ignore')
            try:
                # Parsing page with etree
                e = etree.HTML(page)
                # Extracting all links with xpath
                h = e.xpath('//*[@href]')
                # Using generator for link check/recording
                arr = [self.link_checker(link.attrib.get('href', None)) for link in h if not link.attrib.get('href', None).split('.')[-1] in ignored_links]
                # Removing duplicates returning clear list
                return set(arr)
            except (AttributeError, ValueError):
                pass
        except HTTPError:
            # Page not found error
            print('%s: not found' % link)
            pass

if __name__ == '__main__':
    c = Crawler()
    a = c.link_extractor(c.target_url)
    print(len(a))