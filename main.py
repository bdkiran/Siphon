import requests
import Judgment
import ObtainCases
import ObtainCaseDetails
import logging

URL = 'https://api.unicourt.com/rest/v1/search/?token='
TOKEN = '55ebc2e70236ad95b0f8cc6263223dc143a02737'

logging.basicConfig(level=logging.DEBUG)

def getCaseDetailsToken():      
    #make get request to get details enpoint.
    #save the token off.
    print("Get details token called.")
    requests.get(URL)

def getDocketData():
    print("Get docket data called.")

def main():
    #ObtainCases.parseReponse()
    ObtainCaseDetails.parseReponse()
 

if __name__ == "__main__":
    main()