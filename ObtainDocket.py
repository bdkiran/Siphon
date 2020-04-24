import requests
import json
import logging
import re
from decimal import Decimal
from collections import namedtuple

logger = logging.getLogger('siphon_application.ObtainDocket') 

URL = "https://api.unicourt.com/rest/v1/case/"
TOKEN = "55ebc2e70236ad95b0f8cc6263223dc143a02737"

DocketCaseDetials = namedtuple('DocketCaseDetials', [
    'DocketAmount',
    'JudgmentIssuedDate',
    'DocketEntries'
])

def getDocket(judgment):
    logger.debug('Get docket called.')
    endpoint = buildRequest(judgment.unicourtCaseId, judgment.docketToken)
    unicourtResponse = sendRequest(endpoint)
    return parseResponse(unicourtResponse)
    #endpoint = buildRequest(judgment.unicourtCaseId, judgment.docketToken)
    #sendRequest(endpoint)

def buildRequest(caseId, docketToken):
    logger.debug('Building Request object')
    #https://api.unicourt.com/rest/v1/case/FJCRSHJPIAYUUFQTHRKGNB26MBFQ40902/docketEntries/?token=55ebc2e70236ad95b0f8cc6263223dc143a02737&docket_entries_token=6a8e1eb81373f7099d3f7abdea6d4889ba6348fe&sort=DESC
    endpoint = URL + caseId + "/?token=" + TOKEN + "&docket_entries_token=" + docketToken + "&sort=DESC"
    return endpoint

def sendRequest(endpoint):
    logger.debug('Sending request to: ' + endpoint)
    with open('Requests/docketEntriesResponse.json') as inputFile:
        jsonData = json.load(inputFile)
        return jsonData


def parseResponse(response):
    logger.debug('Parsing unicourt response....')
    docketEntries = response['data']['docket_entries']
    #Gets the docket entries object containing the following string
    filteredList = filter(lambda x: 'Court orders judgment entered' in x['text'], docketEntries)
    #Gets first item of the filtered list
    docketEntry = next(filteredList)

    #Regex to get monetary ammount from string
    dockeEntryString = (docketEntry['text'])
    moneyInDocketString= re.findall(r"(?:[\$]{1}[,\d]+.?\d*)", dockeEntryString)
    
    #Turns monetary amounts into decimals, then grabs the greatest amount.
    maxAmount = 0
    for m in moneyInDocketString:
        value = Decimal(re.sub(r'[^\d.]', '', m))
        if maxAmount < value:
            maxAmount = value

    docketDetails = DocketCaseDetials(maxAmount, docketEntry['date'], docketEntries)
    return docketDetails

            