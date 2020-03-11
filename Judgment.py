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

    def addDocket(self, docketData):
        self.docket = docketData

    def addParties(self, parties):
        self.parties = parties