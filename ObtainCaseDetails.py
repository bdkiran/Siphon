import requests
import json
import Judgment
import logging
from collections import namedtuple


logger = logging.getLogger('ObtainCaseDetails') 

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
def buildRequest():
    logger.debug('Building unicourt request')

def sendRequest():
    logger.debug('Sending unicourt request')

def parseReponse():
    logger.debug("Parsing unicourt response....")
    with open('Requests/caseDetailsResponse.json') as inputFile:
        jsonData = json.load(inputFile)
        data = jsonData['data']
        #print(json.dumps(jsonData, indent = 4))

        #obtain docket token
        #where do I store this??
        docketToken = data['docket_entries_token']
        print(docketToken)

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
                    potentialAddresses.append(potentialAddress)

            person = CompleteParty(person, potentialAddresses)
            allPartiesDetials.append(person)
        
        return allPartiesDetials
