import requests
import json
import Judgment
import logging
from collections import namedtuple

logger = logging.getLogger('siphon_application.ObtainCaseDetails') 

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
    endpoint = buildRequest(judgement.unicourtCaseId)
    unicourtResponse = sendRequest(endpoint)
    return parseReponse(unicourtResponse)

def buildRequest(caseId):
    ##curl -X GET "https://api.unicourt.com/rest/v1/case/FZER2IJTIQ2U4GQXIBMGVC3BMJKRG0906/?token=55ebc2e70236ad95b0f8cc6263223dc143a02737"
    logger.debug('Building unicourt request')
    return URL + caseId + "/?token=" + TOKEN

def sendRequest(endpoint):
    logger.debug('Sending request to: ' + endpoint)
    with open('Requests/caseDetailsResponse.json') as inputFile:
        jsonData = json.load(inputFile)
        return jsonData
    #unicourtResponse = requests.get(endpoint)
    #return unicourtResponse.json

def parseReponse(response):
    logger.debug("Parsing unicourt response....")
    
    data = response['data']

    docketToken = data['docket_entries_token']

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
        allPartiesDetials.append(person._asdict())
    
    caseDetail = CaseDetails(docketToken, allPartiesDetials)
    return caseDetail
