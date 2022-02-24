from dataclasses import InitVar, dataclass, field

@dataclass
class Config(object):

    teamDataFilename: str = field(init=False)
    hourly_rate: int = field(init=False)
    minute_rate: int = field(init=False)
    commission_tracker: dict = field(init=False, default_factory=dict)
    filename: InitVar[str]

    def __post_init__(self, filename):
        '''
        Load Config Info for the file

        configInfo.txt format:
        _______________________
        data path from main,py:
        Campaign, Hourly, Commission ID, Commission Amount:
 
        '''
        with open(filename, 'r') as file:
            lineArr = file.read().splitlines()

        #self.commission_tracker = []
        for index, line in enumerate(lineArr):          
            if index == 0:
                self.teamDataFilename = line
            else:
                splitLine = lineArr[index].split()
                self.hourly_rate = int(splitLine[1])
                self.commission_tracker[splitLine[0]] = tuple(splitLine[2:])

    def get_hourly_rate(self):
        return self.hourly_rate