import dataclasses, pandas

if __name__ == '__main__':
    import config
    from ..controlFunctions import tools
else:
    from objects import config
    from controlFunctions import tools



@dataclasses.dataclass
class Volunteer(object):
    id: str
    name: str = dataclasses.field(init=False)
    email: str = dataclasses.field(init=False)
    etransfer: str = dataclasses.field(init=False)
    phone: str = dataclasses.field(init=False)
    campaign: tuple = dataclasses.field(init=False)
    #trained: str = dataclasses.field(init=False)
    #activities: str = dataclasses.field(init=False)
    minutes: dict = dataclasses.field(init=False, default_factory=dict)
    earned: dict = dataclasses.field(init=False, default_factory=dict)
    paid: dict = dataclasses.field(init=False, default_factory=dict)
    owed: dict = dataclasses.field(init=False, default_factory=dict)
    configData: dataclasses.InitVar[config.Config]

    parsedTeam: pandas.DataFrame= dataclasses.field(init=False)
    parsedHours: pandas.DataFrame= dataclasses.field(init=False)
    parsedPayment: pandas.DataFrame= dataclasses.field(init=False)
    parsedAbstracts: pandas.DataFrame= dataclasses.field(init=False)

    teamData: dataclasses.InitVar[pandas.DataFrame]
    hoursData: dataclasses.InitVar[pandas.DataFrame]
    abstractsData: dataclasses.InitVar[pandas.DataFrame]
    paymentData: dataclasses.InitVar[pandas.DataFrame]

    def __post_init__(self, configData: config.Config, teamData: pandas.DataFrame, hoursData: pandas.DataFrame, abstractsData: pandas.DataFrame, paymentData: pandas.DataFrame):
        self.parsedTeam = teamData.loc[teamData['id']==self.id]
        self.parsedHours = hoursData.loc[hoursData['id'] == self.id]
        self.parsedPayment = paymentData.loc[paymentData['id']==self.id]
        self.parsedAbstracts = abstractsData.loc[abstractsData['id'] == self.id]
        self.name = self.parsedTeam.iloc[0]['name']
        self.email = self.parsedTeam.iloc[0]['email']
        self.etransfer = self.parsedTeam.iloc[0]['e-transfer']
        self.phone = self.parsedTeam.iloc[0]['phone']
        self.campaign = self.parsedTeam.iloc[0]['campaign']

        hoursCampaigns = tools.returnUniqueValues(hoursData, 'campaign')
        abstractCampaigns = tools.returnUniqueValues(abstractsData, 'campaign')
        paymentCampaigns = tools.returnUniqueValues(paymentData, 'campaign')
        
        temp = list(dict.fromkeys(paymentCampaigns + abstractCampaigns))
        workedOnCampaigns = list(dict.fromkeys(hoursCampaigns + paymentCampaigns + abstractCampaigns))

        for campaign in workedOnCampaigns:
            df = self.parsedHours.loc[self.parsedHours['campaign'] == campaign]
            m = df['minutes'].sum()
            self.minutes[campaign] = m
            if not campaign in self.earned.keys():
                self.earned[campaign] = 0
            self.earned[campaign] += m * (configData.get_hourly_rate() / 60) 
            
        for campaign in workedOnCampaigns:
            df = self.parsedAbstracts.loc[self.parsedAbstracts['campaign'] == campaign]
            if not campaign in self.earned.keys():
                self.earned[campaign] = 0
            self.earned[campaign] += df['amount'].sum()

        for campaign in workedOnCampaigns:
            df = self.parsedPayment.loc[self.parsedPayment['campaign'] == campaign]
            if not campaign in self.paid.keys():
                self.paid[campaign] = 0
            self.paid[campaign] += df['amount'].sum()

        if campaign in configData.commission_tracker:
            if self.id == configData.commission_tracker[campaign][0]:
                iso_campaign = hoursData.loc[hoursData['campaign'] == campaign]
                self.earned[campaign] += int(configData.commission_tracker[campaign][1]) / 60  * iso_campaign['minutes'].sum()

        totalOwed = 0
        for campaign, value in self.earned.items():
            owedCalc = self.earned[campaign] - self.paid[campaign]
            if owedCalc < 0:
                owedCalc = 0
            self.owed[campaign] = owedCalc
            totalOwed += owedCalc

        self.owed['total'] = totalOwed

def main():
    '''Main Function'''
    v = Volunteer('sai', 'adjnsk')
    print(v.id)

if __name__ == '__main__':
    '''Script Head'''
    print('volunteer.py start...')
    main()
    print('...volunteer.py complete')