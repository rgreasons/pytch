#!/usr/bin/env python
# -*- coding: UTF-8 -*- 
import re
import sys
import csv
from datetime import datetime
from bs4 import BeautifulSoup
import requests

class PitchforkReview:
    """Model to store a Pitchfork Review"""

    def __init__(self, url):
        self._url = url
        self._ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
        self._html = requests.get(self._url, headers = self._ua)
        self._soup = BeautifulSoup(self._html.text, "html.parser")
        self.retrievalTime = datetime.now()

    @property
    def elements(self):
        return len(self.scores)

    @property
    def reviewId(self):
        """Return Review ID"""
        reviewIDElement = self._soup.find(attrs={"rel": "canonical"})
        reviewLink = reviewIDElement['href']
        try:
            reviewID = int(reviewLink[37:reviewLink.find('-')])
        except:
            reviewID = None
        return reviewID

    @property
    def artistName(self):
        """Return Artist"""
        artistElement = self._soup.find(class_="artist-links")
        try:
            artist = artistElement.find("li")
            artistName = artist.text
        except:
            artistName = artistElement.text
        return artistName

    @property
    def artistId(self):
        """Return Artist ID"""
        artistElement = self._soup.find(class_="artist-links")
        try:
            artist = artistElement.find("li")
            artistHref = artist.find("a")['href']
            artistID = int(artistHref[9:artistHref.find('-')])
        except:
            artistID = 0
        return artistID 

    @property
    def albumNames(self):
        """Returns Album Name"""
        albumsElement = self._soup.find_all(class_=re.compile('review-title'))
        return([str(a.contents[0]) for a in albumsElement])

    @property
    def reviewLink(self):
        return self._soup.find(attrs={"rel": "canonical"})['href']

    @property
    def albumArtLinks(self):
        albumArtElements = self._soup.find_all(class_=re.compile('tombstone__art$'))
        return [a.find("img")['src'] for a in albumArtElements]

    @property
    def genreList(self):
        genreElement = self._soup.find(class_=re.compile("genre-list"))
        if genreElement is not None:
            genrelis = genreElement.find_all('li')
            genreList = [g.find('a').contents[0] for g in genrelis]
        else:
            genreList = []
        return genreList

    @property
    def labelList(self):
        labelsElement = self._soup.find_all("li", class_="labels-list__item")
        labelList = [l.contents[0] for l in labelsElement]
        return labelList

    @property
    def writer(self):
        writerElement = self._soup.find(class_=re.compile('display-name$'))
        return str(writerElement.contents[0])

    @property
    def writerLink(self):
        writerElement = self._soup.find(class_=re.compile('display-name$'))
        return writerElement['href']

    @property
    def scores(self):
        scoreElements = self._soup.find_all(class_="score")
        scores = [s.contents[0] for s in scoreElements]
        return scores
    
    @property
    def isBNM(self):
        bnmElement = self._soup.find(class_='bnm-txt')
        try:
            isBNM = 1 if 'music' in bnmElement.text else 0
        except:
            isBNM = 0
        return isBNM

    @property
    def isBNR(self):
        bnmElement = self._soup.find(class_='bnm-txt')
        try:
            isBNR = 1 if 'reissue' in bnmElement.text else 0
        except:
            isBNR = 0
        return isBNR

    @property
    def publishDate(self):
        publishDateElement = self._soup.find(class_="pub-date")
        try:
            pubtime = datetime.strptime(publishDateElement.contents[0], '%B %d %Y')
        except:
            pubtime = datetime.today()
            
        return pubtime

    @property
    def isReissue(self):
        yearElement = self._soup.find_all('span', class_=re.compile('meta-year$'))
        yearTexts = [i.text for i in yearElement]
        isReissue = 1 if any( '/' in year for year in yearTexts) else 0
        return isReissue

    @property
    def releaseYear(self):
        yearElement = self._soup.find_all('span', class_=re.compile('meta-year$'))
        yearTexts = [i.text for i in yearElement]

        years = []
        for y in yearTexts:    
            if '/' in y:
                releaseYear = y[y.index('•') + 2:y.index('/')]
            else:
                releaseYear = y[y.index('•') + 2:]
            
            if len(releaseYear) is 0:
                releaseYear = self.publishDate.year
            
            years.append(releaseYear)
            
        return years 

    @property
    def review(self):
        reviewContent = self._soup.find(class_='contents dropcap')
        return str(reviewContent).replace('\n', ' ')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('url required')
        sys.exit()

    url = str(sys.argv[1])
    review = PitchforkReview(url=url)
    writer = csv.writer(sys.stdout, delimiter = '|')
    for r in range(0, review.elements):
        writer.writerow([
            review.reviewId,
            review.reviewLink,
            review.artistId,
            review.artistName,
            review.albumNames[r],
            review.albumArtLinks[r],
            review.scores[r],
            review.isBNM,
            review.isBNR,
            review.genreList,
            review.labelList,
            review.releaseYear,
            review.isReissue,
            review.writer,
            review.writerLink,
            review.publishDate,
            review.review
        ])
    # print(review.review)