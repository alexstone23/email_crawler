#!/home/spartan/PycharmProjects/page_parser/bin/python3.5
# -*-coding:utf-8 -*-
import sys
import optparse
from lxml import etree
import urllib.request


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

if __name__ == '__main__':
    c = Crawler()