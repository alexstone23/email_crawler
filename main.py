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


if __name__ == '__main__':
    d = DataChecker()