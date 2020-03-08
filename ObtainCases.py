import requests
import json
import Judgment
import logging

URL = 'https://api.unicourt.com/rest/v1/search/?token='
TOKEN = '55ebc2e70236ad95b0f8cc6263223dc143a02737'
TIMEOUT_TIME = 5

logger = logging.getLogger('ObtainCases') 

#Is this where I want to stroe the state.
DOCKER_START_DATE = "2019-03-01"
DOCKET_END_DATE = "2019-03-31"
CURRENT_PAGE = 1
MAX_PAGES = 100

#Currently request payload is stored in a json file
#is there a more elegant solution to this?
#Need to be able to:
#  change pages
#  change dates
def buildRequest():
    #while CURRENT_PAGE != MAX_PAGES:
    logger.debug("Building Request")

    with open('Requests/searchRequest.json') as queryRequest:
        return json.load(queryRequest)

    #payload['page'] = 
    #filters = payload['filters']
    #print(json.dumps(payload, indent=4))
    #print(json.dumps(filters, indent=4))
    
#Sends the request to unicourt.
#add error handling
def makeRequest():
    logger.debug("Sending Request")
    apiEndpoint = URL + TOKEN
    payload = buildRequest()
    #print(type(payload))
    try:
        response = requests.post(url = apiEndpoint, json=payload, timeout=TIMEOUT_TIME)
        response.raise_for_status()
    
    except(requests.ConnectionError, requests.Timeout) as e:
        logger.error("Connection Error occurered")
        raise e

    if (response.status_code != 200):
        responseBody = response.json()
        logger.error(str(response.status_code) + ': ' + responseBody['message'])

#Determine how many total matches
#On first request determine how many total pages for time period
#Return the cases
def parseReponse():
    logger.debug("Parsing unicourt response....")
    with open('Requests/searchResponse.json') as inputFile:
        jsonData = json.load(inputFile)
        #This will let us know how many pages to iterate through
        total_matches_for_query = int(jsonData['data']['total_matches'])
        print(total_matches_for_query/10)

        innerData = jsonData['data']['result']
        cases = []
        for case in innerData:
            caseThing = case['case']
            #print(json.dumps(caseThing, indent=4))
            judge = Judgment.Judgment(caseThing['case_id'], caseThing['case_number'])
            cases.append(judge)
            return cases