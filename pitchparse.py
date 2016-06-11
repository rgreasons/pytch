def parseReview(reviewUrl):
    multiDict = []

    print('parsing ' + reviewUrl)
    r = requests.get(reviewUrl, headers=ua)
    retrievalTime = datetime.now()
    reviewSoup = BeautifulSoup(r.text, "html.parser")

    reviewIDElement = reviewSoup.find(attrs={"rel": "canonical"})
    artistElement = reviewSoup.find(class_='artists')
    writerElement = reviewSoup.find(class_='display-name')
    genreElement = reviewSoup.find(class_='genre-list')
    publishDateElement = reviewSoup.find(class_='pub-date')
    reviewContent = reviewSoup.find(class_='contents dropcap')

    reviewLink = reviewIDElement['href']
    reviewID = int(reviewLink[36:reviewLink.find('-')])

    # artistName = artistElement.find("a").contents[0]
    # artistHref = artistElement.find("a")['href']
    # artistID = int(artistHref[9:artistHref.find('-')])

    try:
        artist = artistElement.find("li")
        artistHref = artist.find("a")['href']
        artistName = artist.text
        artistID = int(artistHref[9:artistHref.find('-')])
    except:
        artistName = artistElement.text
        artistID = 0

    writer = str(writerElement.contents[0])

    genreLis = genreElement.find_all('li')
    genreList = [g.find('a').contents[0] for g in genreLis]

    timeStr = publishDateElement.contents[0]
    if "ago" in timeStr:
        publishDate = date.today()
    else:
        try:
            publishDate = datetime.strptime(timeStr, '%b %d %Y')
        except:
            publishDate = datetime.strptime(timeStr, '%B %d %Y')

    tombstoneList = reviewSoup.find_all(class_='tombstone')
    for tomb in tombstoneList:
        albumsElement = tomb.find(class_='review-title')
        albumArtElement = tomb.find(class_='album-art')
        labelsElement = tomb.find(class_='labels-and-years')
        yearElement = tomb.find(class_='year')
        bnmElement = tomb.find(class_='bnm-txt')
        scoreElement = tomb.find(class_='score')

        albumName = str(albumsElement.contents[0])

        albumArtLink = albumArtElement.contents[0]['src']

        recordLabels = labelsElement.find_all('li')
        labelList = [l.contents[0] for l in recordLabels]

        isReissue = None
        releaseYear = 0

        yearText = yearElement.contents[1].text
        if '/' in yearText:
            isReissue = 1
            releaseYear = yearText[0:yearText.index('/')]
        else:
            isReissue = 0
            releaseYear = yearText

        score = float(scoreElement.contents[0])

        try:
            isBNR = 1 if 'reissue' in bnmElement.text else 0
            isBNM = 1 if 'music' in bnmElement.text else 0
        except:
            isBNM = 0
            isBNR = 0

        print('creating dict for ' + albumName)
        print(str(publishDate))
        reviewDict = {'artistID': artistID}
        reviewDict['artistName'] = artistName
        reviewDict['reviewID'] = reviewID
        reviewDict['albumName'] = albumName
        reviewDict['reviewLink'] = reviewLink
        reviewDict['albumArtLink'] = albumArtLink
        reviewDict['genreList'] = genreList
        reviewDict['labelList'] = labelList
        reviewDict['releaseYear'] = releaseYear
        reviewDict['isReissue'] = isReissue
        reviewDict['writer'] = writer
        reviewDict['score'] = score
        reviewDict['isBNM'] = isBNM
        reviewDict['isBNR'] = isBNR
        reviewDict['publishDate'] = publishDate
        reviewDict['retrievalTime'] = retrievalTime
        reviewDict['reviewContent'] = str(reviewContent)

        multiDict.append(reviewDict)

        print(type(artistID))
        print(type(artistName))
        print(type(reviewID))
        print(type(albumName))
        print(type(reviewLink))
        print(type(albumArtLink))
        print(type(genreList))
        print(type(labelList))
        print(type(releaseYear))
        print(type(isReissue))
        print(type(writer))
        print(type(score))
        print(type(isBNM))
        print(type(isBNR))
        print(type(publishDate))
        print(type(retrievalTime))
        print(type(reviewContent))

    return multiDict

    # print('Completed parsing ' + artistName + ' - ' + albumName)

if __name__ == "__main__":
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    from datetime import datetime

    ua = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
    reviewDataFrame = pd.DataFrame()

    reviewIndexUrl = 'http://pitchfork.com/reviews/albums/?page='
    # url = 'http://pitchfork.com/reviews/albums/'
    # url = 'http://pitchfork.com/reviews/albums/21673-teens-of-denial/'
    pageNumber = 1471

    print('retrieving reviews for ' + reviewIndexUrl + str(pageNumber) + '...')
    reviewPageResponse = requests.get((reviewIndexUrl + str(pageNumber)), headers=ua)
    masterReviewList = []
    while reviewPageResponse.status_code == 200:
        reviewListSoup = BeautifulSoup(reviewPageResponse.text, "html.parser")
        reviewList = reviewListSoup.find_all(class_="album-link")
        reviewLinkList = ["http://www.pitchfork.com" + l['href'] for l in reviewList]
        print('reviews on page: ' + str(len(reviewLinkList)))
        for reviewListURL in reviewLinkList:
            parsedList = parseReview(reviewListURL)
            reviewDataFrame = reviewDataFrame.append(parsedList)

        pageNumber = pageNumber + 1
        reviewPageResponse = requests.get((reviewIndexUrl + str(pageNumber)), headers=ua)
        print(reviewPageResponse)

    reviewDataFrame.to_csv('endsample.csv', sep='|')
    reviewDataFrame.to_pickle('endSample.pkl')
    otherDataFrame = reviewDataFrame.pop('reviewContent')
    reviewDataFrame.to_pickle('contentfreeend.pkl')
    reviewDataFrame.to_csv('endSamplecontentfree.csv', sep='~')
