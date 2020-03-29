import requests
import Judgment
import json
from ObtainCases import getCases
from ObtainCaseDetails import getCaseDetails
from ObtainDocket import getDocket
import logging
from collections import deque

#URL = 'https://api.unicourt.com/rest/v1/search/?token='
#TOKEN = '55ebc2e70236ad95b0f8cc6263223dc143a02737'

# create logger with 'spam_application'
logger = logging.getLogger('siphon_application')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('siphonTrace.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

#initialize queues for data processing
DQ1 = deque()
DQ2 = deque()
DQ3 = deque()

def main():
    logger.info("Starting judgment collection")
    while True: 
        baseJudgments = getCases()
        if baseJudgments == None:
            logger.info("Judgment collection completed")
            return
        for baseJudgment in baseJudgments:
            DQ1.append(baseJudgment)
        getPartyInformation()
        getJudgmentDetails()
        addJudgmentToMongo()
            
def getPartyInformation():
    while DQ1:
        judgment = DQ1.pop()
        caseDetail = getCaseDetails(judgment)
        judgment.addDocketToken(caseDetail.DocketToken)
        judgment.addParties(caseDetail.PartyInfo)
        DQ2.append(judgment)

def getJudgmentDetails():
    while DQ2:
        judgment = DQ2.pop()
        docketDetails = getDocket(judgment)
        judgment.addJudmentDetails(docketDetails.DocketAmount, docketDetails.JudgmentIssuedDate)
        judgment.addDocket(docketDetails.DocketEntries)
        DQ3.append(judgment)

def addJudgmentToMongo():
    while DQ3:
        judgment = DQ3.pop()
        #logger.info(json.dumps(judgment.__dict__, indent=4))
    
if __name__ == "__main__":
    main()
