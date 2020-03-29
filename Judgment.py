from decimal import Decimal

class Judgment:
    
    #Data model
    #===========
    #unicourt Case Id
    #Case Numer
    #Clients[s]
    #Judgement Ammount
    #Judgment Issued Date
    ##Name
    ##Address
    #Debtor[s]
    ##Name
    ##Address
    #Docket

    def __init__(self, unicourtCaseId, caseNumber):
        self.unicourtCaseId = unicourtCaseId
        self.caseNumber = caseNumber

    def addDocketToken(self, docketToken):
        self.docketToken = docketToken

    def addParties(self, parties):
        self.parties = parties

    def addJudmentDetails(self, judgmentAmount, judgmentDate):
        self.judgmentDate = judgmentDate
        if isinstance(judgmentAmount, Decimal):
            self.judgmentAmount = float(judgmentAmount)  

    def addDocket(self, docketData):
        self.docket = docketData