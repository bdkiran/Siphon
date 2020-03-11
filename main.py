import requests
import Judgment
import ObtainCases
import json
import ObtainCaseDetails
import logging

URL = 'https://api.unicourt.com/rest/v1/search/?token='
TOKEN = '55ebc2e70236ad95b0f8cc6263223dc143a02737'

logging.basicConfig(level=logging.INFO)

def main():
    baseJudgments = ObtainCases.getCases()
    for baseJudgment in baseJudgments:
        party = ObtainCaseDetails.parseReponse(baseJudgment.unicourtCaseId)
        baseJudgment.addParties(party)
        print(json.dumps(baseJudgment.__dict__, indent=4))

def getDocketData():
    print("Get docket data called.")

if __name__ == "__main__":
    main()