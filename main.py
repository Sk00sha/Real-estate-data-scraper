import helper
from scrape import *
from dataset import *
from multiprocessing import Pool

if __name__ == '__main__':
    postingData = []
    nestedListings = dict()
    # URLS of regions in our country - listings
    url = [
        "trenciansky",
        "bratislavsky",
        "trnavsky",
        "kosicky",
        "nitriansky",
        "presovsky",
        "zilinsky",
        "banskobystricky"
    ]

    with Pool(4) as p:
        nestedListings = p.map(returnNestedProperties, url)

    nestedLinks = {**nestedListings[0], **nestedListings[1], **nestedListings[2], **nestedListings[3],
                   **nestedListings[4], **nestedListings[5], **nestedListings[6], **nestedListings[7]}

    postingData = getPostingData(*nestedLinks.values())

    cleanListofDicts = []
    for dictionary in postingData:
        cleanDict={}
        for key in dictionary.keys():
            # normalize key, so we don't have duplicate keys with special characters like: price == -price (remove '-')
            cleanDict[helper.normalizeText(key)] = dictionary[key]
        cleanListofDicts.append(cleanDict)

    dataFrame = constructDataFrame(cleanListofDicts)

    # get name of our csv in timestamp format
    csvName = helper.constructtimestamp()
    # export to csv
    dataFrame.to_csv(csvName)
