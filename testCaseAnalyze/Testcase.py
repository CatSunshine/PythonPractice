class Testcase:
    '''define a testcase.'''
    def __init__(self):
        self.className = ''
        self.link = ''
        self.leftStatus = ''
        self.rightStatus=''
        self.errorMsg = ''
        self.testSuite = ''
        self.terminal = 0
        self.radioType = ''
        self.caseName=''
        self.trNum = ''
        self.trlink = ''
        self.levelOneType = 0
        self.levelTwoType = 0
    def toString(self):
        print('testSuite:',self.testSuite,'terminal:',self.terminal,'radioType:',self.radioType,
              'className:',self.className,'leftStatus:', self.leftStatus,'rightStatus:',self.rightStatus,
              'link:',self.link,'caseName:',self.caseName,'errorMsg:',self.errorMsg, 'trNum:',self.trNum,
              'trlink:', self.trlink,'levelOneType:',self.levelOneType, 'levelTwoType:',self.levelTwoType)
'''
tc1 = Testcase()
tc1.className='DlCarrierCombiner'
tc1.link='/resultweb/logs/5832714/tree?expand=257952748'
tc1.leftStatus='pass'
tc1.rightStatus='fail'
tc1.errorMsg='Issue: Assertion failed: te log error: [The te log for RU: WMDefault_ru_1 contains error trace(s)., Paam Communication Unlocked failed.&quot; }, com_ericsson_trithread:ERROR: { 1 }, { &quot;EquipCtrl&quot;, &quot;tddSwitchSrv75.cc:353&quot;, &quot;Failed to enable DP carrier:deviceProcEvcPaa'
tc1.testSuite='ElvisRegression.xml'
tc1.terminal=70
tc1.radioType= 'AIR 5121 B257A, R1A'

print(tc1.toString())
'''
