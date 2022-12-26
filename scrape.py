from bs4 import BeautifulSoup
import requests
from helper import *


def returnNestedProperties(region: str) -> dict:
    """
    Function scrapes main page of region and returns all links to most recent postings

    returns: dict w. values in lists
    """

    eligibleLinks = dict()
    eligibleLinks[region] = []
    response = requests.get(constructAddress(region))

    soup = BeautifulSoup(response.text, "html.parser")

    specificdata = soup.findAll("a")

    for website in specificdata:
        if (len(website.find_all(class_="offer-title crop-text mb-1 mb-sm-0")) != 0):
            eligibleLinks[region].append(f"http://reality.sk{website['href']}")

    return eligibleLinks


def constructAddress(region: str) -> str:
    """
    Function constructs main page containing all listings for input region

    returns: url string
    """

    address = f"https://www.reality.sk/{region}-kraj/virtualne-prehliadky/?order=created_date-newest"
    return address


def reacreateArray(dataStr: str) -> str:
    """
    Function returns string if it's not empty

    returns: string
    """
    if (dataStr != ""):
        return dataStr


def getPostingData(*links) -> list:
    """
    Function that calls post scraping and appends original url to lists

    returns: list of dictionaries(used to create final dataframe)
    """

    arrayOfDicts = []
    for item in links:
        for url in item:
            postingData = scrapePosting(url)
            postingData[0].append("Address")
            postingData[1].append(url)
            arrayOfDicts.append(dict(zip(postingData[0], postingData[1])))

    return arrayOfDicts


def getMonetaryData(soup) -> str:
    """
    Function scrapes values(cost) of housing from posts

    returns: (price) string if price was posted, else returns empty string
    """

    try:
        price = soup.find(class_="contact-title big")
        price = price.text.split(' ')
        return price[0] + price[1]
    except Exception as e:
        return ""


def scrapePosting(address: str) -> list:
    """
    Function scrapes the actual site containing all the posting information

    returns: list of lists
    """

    data = requests.get(address)

    soup = BeautifulSoup(data.text, "html.parser")

    params = soup.findAll(class_="row no-gutters content-preview mt-1")[0]
    price = getMonetaryData(soup)

    # just cleaning data because of format on original webpage
    parsedData = '-'.join(params.text.replace(' ', '-').split('\n')).replace('--', ' ').split(' ')

    # filter list, cleanse from empty strings
    dataList = list(filter(reacreateArray, parsedData))

    values = dataList[1::2]
    values.append(price)

    # normalize text before adding to return value list
    values = [normalizeText(i) for i in values]
    headers = dataList[::2]
    headers.append("Cena")
    return [headers, values]
