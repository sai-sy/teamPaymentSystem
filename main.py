from pandas import DataFrame, Series
from controlFunctions import tools, constants
from objects import config, volunteer, dataContainer
from datetime import date

def build_campaign( data: dataContainer.sheetContainer, campaign: str, config: config.Config):
    dataParsed = data.parse_campaign(campaign)

    allVolunteersInCampaign = []

    output = []

    for id in dataParsed.uniqueVolunteers:
        v = volunteer.Volunteer(id, config, dataParsed.teamInfo, dataParsed.hoursInfo, dataParsed.abstractsInfo, dataParsed.paymentInfo)
        allVolunteersInCampaign.append(v)
    firstRow = []
    add = ['~']
    # First row in output
    # ~ andrea ~ rana

    for uniqueCampaign in dataParsed.uniqueCampaigns:
        firstRow.append('~')
        firstRow.append(uniqueCampaign)
        firstRow.append('~')

        add.append('earned')
        add.append('paid')
        add.append('owed')

    output.append(firstRow)
    output.append(add)

    for uniqueVolunteer in allVolunteersInCampaign:
        row = [uniqueVolunteer.id]
        for uniqueCampaign in dataParsed.uniqueCampaigns:
            try:
                row.append(round(uniqueVolunteer.earned[uniqueCampaign], 2))                
            except KeyError:
                row.append(0)
                continue
            try:
                row.append(round(uniqueVolunteer.paid[uniqueCampaign], 2))
            except KeyError:
                row.append(0)
                continue
            try:
                row.append(round(uniqueVolunteer.owed[uniqueCampaign], 2))
            except KeyError:
                row.append(0)
                continue
        output.append(row)
            

    for row in output:
        pass

    for x in output:
        print(*x, sep=' ')

def main():

    '''Main Function'''
    tools.setWorkingDirectoryToSelf()
    _configData = config.Config(constants.config_file())

    #Load Total Data
    print('-------------------------------')
    print('Loading Total Data...')
    totalData = dataContainer.create_sheet(_configData.teamDataFilename)
    print('Total Data Loaded')
    print('-------------------------------')
    while(True):
        
        print('\n- Build a report | build\n- View one persons data | view\n- Exit the program | quit')
        userChoice = input('What would you like to do: ')
        if userChoice == 'build' or 'b' or 'Build':
            while(True):
                userChoice = input('\nWhich campaign would you want to report or all: ')
                build_campaign(totalData, userChoice, _configData)
        elif userChoice == 'view' or 'v' or 'View':
            pass
        elif userChoice == 'quit' or 'q' or 'Quit':
            break
        else:
            print('Error Invalid Input | Please select one of the given values\n\n')

def test():
    pass
    
if __name__ == '__main__':
    '''script head'''
    today = date.today()
    print(f'main.py | Team Management System | {today}\n-----------------------------------------------\nStarting...')
    main()
    print('Complete')