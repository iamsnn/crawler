# -*- coding: utf-8 -*-
import json
import re
import random

import requests
from bs4 import BeautifulSoup
import warnings

warnings.filterwarnings('ignore')


class cached_property(object):
    """A property that is only computed once per instance and then replaces itself
    with an ordinary attribute. Deleting the attribute resets the property.
    """

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        if obj is None:
            return self
        value = obj.__dict__[self.func.__name__] = self.func(obj)
        return value


class Header(object):
    """Generate header dict for request"""

    @staticmethod
    def get_header():
        USER_AGENT_LIST = [
            'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.12 Safari/535.11',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
            'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6',
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
            ]
        header = {
            'User-Agent': random.choice(USER_AGENT_LIST),
            'Host': "www.goodreads.com",
            'Origin': "https://www.goodreads.com",
        }
        return header


class Book(object):
    def __init__(self, url, page=1):
        type_str = url.split('/')[-3].title()
        constructor = globals()[type_str]
        self.deputy = constructor(url, page=page)

    @cached_property
    def titles(self):
        return self.deputy.get_titles()

    @cached_property
    def authors(self):
        return self.deputy.get_authors()

    @cached_property
    def avg_ratings(self):
        return self.deputy.get_avg_ratings()

    @cached_property
    def rating_counts(self):
        return self.deputy.get_rating_counts()

    @cached_property
    def published_year(self):
        return self.deputy.get_published_year()

    @cached_property
    def book_img(self):
        return self.deputy.get_bookImg()

    @cached_property
    def book_shelvedNumber(self):
        return self.deputy.get_shelvedNumber()

    @cached_property
    def book_detailLink(self):
        return self.deputy.get_detailLink()

    @cached_property
    def book_detail(self):
        return self.deputy.get_bookDetails()


# all the thing you can get from the main page
class Shelf(object):

    def __init__(self, url=None, genre=None, page=1):
        if url:
            url = url.rsplit('?page')[0]
        if genre:
            url = 'https://www.goodreads.com/shelf/show/' + genre
        self.url = url + '?page=' + str(page)
        self.page = page
        self.genre = genre

    def _get_content(self):
        r = requests.get(self.url, headers=Header.get_header(), verify=False)
        return BeautifulSoup(r.content)

    @cached_property
    def book_units(self):
        soup = self._get_content()
        units = soup.select(".leftContainer .elementList")
        return units

    def get_titles(self):
        for soup in self.book_units:
            title = soup.find("a", {"class": "bookTitle"}).text
            title = title[0:title.find('(') - 1]
            yield title

    def get_authors(self):
        for soup in self.book_units:
            author = soup.find("span", {"itemprop": "name"}).text
            try:
                yield author
            except IndexError:
                yield None

    def get_avg_ratings(self):
        for soup in self.book_units:
            extra_info = soup.find(
                "span", {"class": "greyText smallText"}).text
            try:
                yield re.findall(r"rating.(.+?)\s", extra_info)[0]
            except IndexError:
                yield None

    def get_rating_counts(self):
        for soup in self.book_units:
            extra_info = soup.find(
                "span", {"class": "greyText smallText"}).text
            try:
                yield re.findall(r"(?<=\s).+?(?=ratings)", extra_info)[0].strip().replace(',', '')
            except IndexError:
                yield None

    def get_published_year(self):
        for soup in self.book_units:
            extra_info = soup.find(
                "span", {"class": "greyText smallText"}).text
            try:
                yield re.findall(r"published.(.+?)\s", extra_info)[0]
            except IndexError:
                yield None

    def get_bookImg(self):
        for soup in self.book_units:
            img = soup.find('img')['src'][:-10:1] + 'jpg'
            yield img

    def get_detailLink(self):
        for soup in self.book_units:
            dLink = 'https://www.goodreads.com' + soup.find("a", {"class": "bookTitle"})['href']
            yield dLink

    def get_shelvedNumber(self):
        for soup in self.book_units:
            info = soup.find('a', {"class": "smallText"}).text
            yield info.split(' ')[1]

    def get_bookDetails(self):
        for link in self.get_detailLink():
            yield BookDetail(url=link)


class BookDetail(object):
    def __init__(self, url):
        self.bookurl = url

    @cached_property
    def book_units(self):
        r = requests.get(self.bookurl, headers=Header.get_header(), verify=False)
        soup = BeautifulSoup(r.content, from_encoding="utf-8")

        units = soup.select("#bookDataBox .clearFloats")

        decription = soup.select("#description")
        generes = soup.find_all('a', {"class": 'actionLinkLite bookPageGenreLink'})

        reviews1 = soup.find_all('span', {"id": re.compile(r'^freeText[0-9]')})
        reviews2 = soup.find_all('span', {"id": re.compile(r'^freeTextContainer[0-9]')})

        link = soup.find('a', {"class": 'actionLink right seeMoreLink'})
        author = soup.find_all('span', {"itemprop": 'name'})
        title = soup.find('h1', {"id": 'bookTitle'}).text

        score = soup.find('span', {"itemprop": 'ratingValue'}).text
        year = soup.find('div', {"class": 'uitext darkGreyText'}).find_all('div', {"class": 'row'})

        rating = soup.find('meta', {"itemprop": 'ratingCount'}).text
        reviewers = soup.find('meta', {"itemprop": 'reviewCount'}).text
        img = soup.find('img', {"id": 'coverImage'})

        return [units, decription, generes, [reviews1, reviews2], link, author, title, score, year, rating, reviewers,
                img]

    def get_isbn(self):
        for soup in self.book_units[0]:
            if soup.find('div', {'class': 'infoBoxRowTitle'}).text == "ISBN":
                isbn = soup.find('div', {'class': 'infoBoxRowItem'}).text.lstrip().split(' ')[0]
                return isbn

    def get_decription(self):
        for soup in self.book_units[1]:
            if len(soup.find_all('span')) != 1:
                for s in soup.find_all('span', {'style': 'display:none'}):
                    return s.text.encode("utf-8")
            else:
                return soup.text.encode("utf-8")

    def get_bookGenre(self):
        for item in self.book_units[2]:
            yield item.text

    def get_review(self):

        if len(list(self.book_units[3][0])) < 5:
            for item in self.book_units[3][1]:
                yield item.text
        else:
            for item in self.book_units[3][0]:
                yield item.text

    def get_recommend(self):
        if self.book_units[4] != None:
            return self.book_units[4]['href']
        return None

    def get_author(self):
        if len(list(self.book_units[5])) > 1:
            return self.book_units[5][1].text
        else:
            return self.book_units[5][0].text

    def get_title(self):
        return self.book_units[6].strip()

    def get_score(self):
        return self.book_units[7].strip() + ''

    def get_year(self):
        if len(self.book_units[8]) != 1:
            return re.findall('\d{4}', self.book_units[8][1].text)[0] + ''
        else:
            tag = self.book_units[8][0].find('nobr', {"class": 'greyText'})
            if tag != None:
                return re.findall('\d{4}', tag.text)[0] + ''
            else:
                return None

    def get_rating(self):
        return self.book_units[9].strip().split(" ")[0].replace(",", "")

    def get_reviewers(self):
        return self.book_units[10].strip().split(" ")[0].replace(",", "")

    def get_img(self):
        if self.book_units[11] != None:
            return self.book_units[11]['src']
        else:
            return None

    def finalResult(self):
        p = {}
        p["isbn"] = self.get_isbn()
        p["description"] = self.get_decription()

        res = []
        for gen in self.get_bookGenre():
            item = {}
            item['g'] = gen
            res.append(item)
        p["genre"] = res

        res = []
        for rev in self.get_review():
            item = {}
            item['r'] = rev
            res.append(item)
        p["review"] = res

        p["recommend"] = self.get_recommend()
        p["author"] = self.get_author()
        p["title"] = self.get_title()
        p["score"] = self.get_score()
        p["year"] = self.get_year()
        p["rating"] = self.get_rating()
        p["reviewers"] = self.get_reviewers()
        p["img"] = self.get_img()
        p["url"] = self.bookurl
        return p


if __name__ == '__main__':

    f = open("links", "r")
    lines = f.readlines()
    f.close()
    i = 1
    file = open('result.json', 'a+')
    for line in lines:
        if i < 50:
            b = BookDetail(line)
            try:
                print i
                tmpData = {}
                tmpData = json.dumps(b.finalResult())
                file.writelines(json.dumps({"index": {"_id": i}}) + "\n")
                file.writelines(tmpData + "\n")
            except:
                print line + "wrong"
                continue
            i += 1
        else:
            break

file.close()