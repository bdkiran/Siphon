import requests
import json
import Judgment
import logging
from collections import namedtuple

logger = logging.getLogger('ObtainCaseDetails') 

CaseDetails = namedtuple('CaseDetails', [
    'DocketToken',
    'PartyInfo'
])

CompleteParty = namedtuple('CompleteParty', [
    'Participant',
    'Addresses'
])

Participant = namedtuple('Participant', [
    'PartyType',
    'FirstName',
    'LastName'
])

Address = namedtuple('Address', [
    'Address',
    'City',
    'State',
    'Zipcode'
])

URL = "https://api.unicourt.com/rest/v1/case/"
TOKEN = "55ebc2e70236ad95b0f8cc6263223dc143a02737"

def getCaseDetails(judgement):
    endpoint = buildRequest(judgement.caseId)
    sendRequest(endpoint)
    parseReponse(judgement.caseId)

def buildRequest(caseId):
    ##curl -X GET "https://api.unicourt.com/rest/v1/case/FZER2IJTIQ2U4GQXIBMGVC3BMJKRG0906/?token=55ebc2e70236ad95b0f8cc6263223dc143a02737"
    logger.debug('Building unicourt request')
    return URL + caseId + "/?token=" + TOKEN

def sendRequest(endpoint):
    logger.debug('Sending unicourt request to: ' + endpoint)
    #response = requests.get(endpoint)
    #return response.json

def parseReponse(caseId):
    logger.debug("Parsing unicourt response....")
    endpoint = buildRequest(caseId)
    sendRequest(endpoint)
    with open('Requests/caseDetailsResponse.json') as inputFile:
        jsonData = json.load(inputFile)
        data = jsonData['data']

        docketToken = data['docket_entries_token']
        #print(docketToken)

        #obatin plantif and defendant details
        allPartiesDetials = []
        parties = data['case']['parties']
        for party in parties:
            partyType = party['party_types'][0]['party_type']
            person = Participant(str(partyType), party['firstname'], party['lastname'])
            potentialAddresses = []
            entities = party['entities']
            for entity in entities:
                details = entity['potentials']
                for detail in details:
                    potentialAddress = Address(detail['address'], detail['city'], detail['state'], detail['zipcode'])
                    potentialAddresses.append(potentialAddress._asdict())

            person = CompleteParty(person._asdict(), potentialAddresses)
            logger.debug(person._asdict())
            allPartiesDetials.append(person._asdict())
        
        caseDetail = CaseDetails(docketToken, allPartiesDetials)

        
        return caseDetail
