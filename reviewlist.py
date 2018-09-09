import requests
from datetime import datetime
from bs4 import BeautifulSoup
import csv

def retrieveAlbumLinks(text):
    soup = BeautifulSoup(text, "html.parser")
    reviewList = soup.find_all(class_="review__link")
    reviewLinkList = ["http://www.pitchfork.com" + l['href'] for l in reviewList]
    return reviewLinkList

if __name__ == '__main__':
    pagenum = 1
    url = 'http://pitchfork.com/reviews/albums/?page='
    ua ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
    masterList = []
    start = datetime.now()

    # reviewPageResponse = requests.get((url + str(pagenum)), headers=ua)
    # while reviewPageResponse.status_code == 200:
    while pagenum < 1710:
        reviewPageResponse = None
        # loop retries if a page response fails
        while reviewPageResponse is None or reviewPageResponse.status_code != 200:
            reviewPageResponse = requests.get((url + str(pagenum)), headers=ua)
            if reviewPageResponse.status_code == 404:
                print("404 at " + str(pagenum))

        reviewList = retrieveAlbumLinks(reviewPageResponse.text)
        masterList.extend(reviewList)
        pagenum = pagenum + 1
        if pagenum % 50 == 0:
            diff = datetime.now() - start
            perpage = diff / pagenum
            print(str(pagenum) + ": " + datetime.now().strftime("%H %M %S"))
            print(perpage)


    with open('reviewlinks.csv', 'w') as reviews:
        linkwriter = csv.writer(reviews, delimiter = '|')
        [linkwriter.writerow([l]) for l in masterList]

    