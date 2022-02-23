from dataclasses import dataclass, field, InitVar
import pandas as pd
    
if __name__ == '__main__':
    from ..controlFunctions import tools, constants
else:
    from controlFunctions import tools, constants

#Formatting Variables
TEAM = constants.TEAM
HOURS = constants.HOURS
ABSTRACTS = constants.ABSTRACTS
PAYMENTS = constants.PAYMENTS

@dataclass
class sheetContainer(object):
    teamInfo: pd.DataFrame
    hoursInfo: pd.DataFrame
    abstractsInfo: pd.DataFrame
    paymentInfo: pd.DataFrame
    uniqueVolunteers: list[str]= field(init=False, default_factory=list)
    uniqueCampaigns: list[str] = field(init=False, default_factory=list)
    campaign: str = 'all'

    def __post_init__(self):
        if self.campaign == 'all':
            self.uniqueCampaigns = tools.returnUniqueValues(self.hoursInfo,constants.campaign())
            self.uniqueVolunteers = tools.returnUniqueValues(self.hoursInfo, constants.id())

    def parse_campaign(self, campaignToParse):
        if campaignToParse=='all':
            return self

        output = sheetContainer(
        self.teamInfo,
        self.hoursInfo.loc[self.hoursInfo[constants.campaign()] == campaignToParse],
        self.abstractsInfo.loc[self.abstractsInfo[constants.campaign()] == campaignToParse],
        self.paymentInfo.loc[self.paymentInfo[constants.campaign()] == campaignToParse],
        )

        return output

def create_sheet(filename):
    teamInfo = tools.loadSheetAsDf(filename, constants.team())
    hoursInfo = tools.loadSheetAsDf(filename, constants.hours())
    abstractsInfo = tools.loadSheetAsDf(filename, constants.abstracts())
    paymentInfo = tools.loadSheetAsDf(filename, constants.payments())   

    output = sheetContainer(teamInfo, hoursInfo, abstractsInfo, paymentInfo)

    return output