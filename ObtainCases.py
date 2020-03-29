import requests
import json
import math
from Judgment import Judgment
import logging

URL = 'https://api.unicourt.com/rest/v1/search/?token='
TOKEN = '55ebc2e70236ad95b0f8cc6263223dc143a02737'
TIMEOUT_TIME = 5

logger = logging.getLogger('siphon_application.ObtainCases') 

#Is this where I want to store the state of the request.
DOCKER_START_DATE = "2019-03-01"
DOCKET_END_DATE = "2019-03-31"
CURRENT_PAGE = 1
MAX_PAGES = 100

def getCases():
    global CURRENT_PAGE
    allCases = []
    if CURRENT_PAGE < MAX_PAGES:
        logger.debug('Page: ' + str(CURRENT_PAGE))
        payload = buildRequest()
        jsonData = makeRequest(payload)
        for case in parseReponse(jsonData):
            allCases.append(case)
        CURRENT_PAGE = CURRENT_PAGE + 1
        return allCases
    else:
        return None
    

#Currently request payload is stored in a json file
#is there a more elegant solution to this?
#Need to be able to:
#  change pages
#  change dates
def buildRequest():
    logger.debug("Building Request")
    with open('Requests/searchRequest.json') as queryRequest:
        payload = json.load(queryRequest)
        payload['page'] = CURRENT_PAGE
    #filters = payload['filters']
    #print(json.dumps(payload, indent=4))
    #print(json.dumps(filters, indent=4))
        return payload
    
#Sends the request to unicourt.
#add error handling
def makeRequest(payload):
    apiEndpoint = URL + TOKEN
    logger.debug("Sending Request to: " + apiEndpoint)
    #print(type(payload))
    #mocks for downstream function
    with open('Requests/searchResponse.json') as inputFile:
        return json.load(inputFile)
    # Actual sending of request. Fix error handling logic
    # Not sure if that has required coverage.
    # try:
    #     response = requests.post(url = apiEndpoint, json=payload, timeout=TIMEOUT_TIME)
    #     response.raise_for_status()
    #     if (response.status_code != 200):
    #         responseBody = response.json()
    #         logger.error(str(response.status_code) + ': ' + responseBody['message'])
    #     else:
            
    #         return response.responseBody
    
    # except(requests.ConnectionError, requests.Timeout) as e:
    #     logger.error("Connection Error occurered")
    #     raise e



#Determine how many total matches
#On first request determine how many total pages for time period
#Return the cases
def parseReponse(jsonData):
    logger.debug("Parsing unicourt response....")
    global MAX_PAGES
    if CURRENT_PAGE == 1:
        #This will let us know how many pages to iterate through
        total_matches_for_query = int(jsonData['data']['total_matches'])
        MAX_PAGES = math.ceil(total_matches_for_query/10)

    #parse for caseId and CaseNumber
    innerData = jsonData['data']['result']
    cases = []
    for case in innerData:
        caseInfo = case['case']
        #print(json.dumps(caseThing, indent=4))
        judge = Judgment(caseInfo['case_id'], caseInfo['case_number'])
        cases.append(judge)
    return cases
