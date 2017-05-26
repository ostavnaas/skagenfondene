#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import re
import csv
import os
from lxml import html


class skagen:
    def __init__(self, feed, **fond):
        self.fond = fond
        self.fond['investment'] = int(self.fond['investment'])
        self.fond['share'] = float(self.fond['share'])
        self.marked_value = self.valueFromHTML(feed.content)
        self.marked_value_share = self.marked_value * self.fond['share']
        self.return_value = self.marked_value_share - self.fond['investment']
        self.return_rate = (self.return_value / self.fond['investment']) * 100

    def toFloat(self, feed):
        feedSub = re.sub(r'\xa0', '', feed[0])
        m_value = re.findall(r"\d{1,10}\,\d{0,10}", feedSub)[0]
        return float(m_value.replace(',', '.'))

    def valueFromHTML(self, feed):
        tree = html.fromstring(feed)
        pGlobal = '//div[@data-isin="NO0008004009"]//p[@class="price"]/text()'
        pKonToki = '//div[@data-isin="NO0010140502"]//p[@class="price"]/text()'
        pVekst = '//div[@data-isin="NO0008000445"]//p[@class="price"]/text()'
        if self.fond['fond'] == 'SKAGEN Global A':
            value = tree.xpath(pGlobal)
        elif self.fond['fond'] == 'SKAGEN Kon-Tiki A':
            value = tree.xpath(pKonToki)
        elif self.fond['fond'] == 'SKAGEN Vekst A':
            value = tree.xpath(pVekst)
        return self.toFloat(value)

    def markedValue(self):
        return self.marked_value_share

    def returnValue(self):
        return self.marked_value_share

    def investValue(self):
        return self.fond['investment']

    def printOut(self):
        print 'Fond {}'.format(self.fond['fond'])
        print 'Owner {}'.format(self.fond['owner'])
        print 'Investment date: {}'.format(self.fond['date'])
        print 'Investment: ', self.fond['investment']
        print 'Value: {0:.0f}'.format(self.marked_value_share)
        print 'Return: {0:.0f}'.format(self.return_value)
        print 'Return rate {0:.4f}%'.format(self.return_rate)
        print ''


def readFromCSV():
    pwd = os.path.dirname(os.path.realpath(__file__))
    csvfile = '{}/fonds.csv'.format(pwd)
    with open(csvfile, 'rb') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            yield row


r = requests.get('https://www.skagenfondene.no')
k = [skagen(r, **i) for i in readFromCSV()]
owners = set([i.fond['owner'] for i in k])
total = {}
investment = {}

for i in owners:
    total[i] = 0
    investment[i] = 0

for r in k:
    if r.fond['owner'] in owners:
        own = [ow for ow in owners if ow == r.fond['owner']]
        total[own[0]] += r.returnValue()
        investment[own[0]] += r.investValue()
    r.printOut()

for i in total.keys():
    avkastning = (((total[i] - investment[i]) / investment[i]) * 100)
    print '-'*40
    print 'Eier: {}'.format(i)
    print 'Investering: {:,} NOK'.format(investment[i])
    print 'avkastning: {0:,.0f} NOK'.format(total[i] - investment[i])
    print 'Total: {0:,.0f} NOK'.format(total[i])
    print 'Avkastning {0:.3}%'.format(avkastning)
    print ''
