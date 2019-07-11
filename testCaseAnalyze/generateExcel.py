import xlwings as xw
from analyzeLog import AnalyzeLog
def titleStyle(rng):
    rng.api.Font.size = 16
    rng.api.Font.Bold = True
    rng.api.Font.Color = 0x0000ff


def suiteStype(rng):
    rng.api.Font.size = 14
    rng.api.Font.Bold = True
    rng.api.Font.Color = 0x000000
    
def classStype(rng):
    rng.api.Font.size = 12
    rng.api.Font.Bold = False
    rng.api.Font.Color = 0x000000

def addNewTitle(sht, rows, wantedCase):
    sht.range('A'+str(rows)).value = wantedCase.testSuite
    suiteStype(sht.range('A'+str(rows)))
    sht.range('B'+str(rows)).value = wantedCase.radioType + ' Terminal ' + str(wantedCase.terminal)
    suiteStype(sht.range('B'+str(rows)))
    rows += 1
    sht.range('A'+str(rows)).value = wantedCase.className
    classStype(sht.range('A'+str(rows)))
    rows += 1
    #sht.range('A'+str(rows)).value = wantedCase.caseName
    print(r'https://ki81fw4.rnd.ki.sw.ericsson.se'+wantedCase.link)
    sht.range('A'+str(rows)).add_hyperlink(r'https://ki81fw4.rnd.ki.sw.ericsson.se'+wantedCase.link, wantedCase.caseName,'')
    sht.range('B'+str(rows)).value = ''.join(wantedCase.errorMsg)
    return rows+1

def addNewClass(sht, rows, wantedCase):
    sht.range('A'+str(rows)).value = wantedCase.className
    classStype(sht.range('A'+str(rows)))
    rows += 1
    #sht.range('A'+str(rows)).value = wantedCase.caseName
    sht.range('A'+str(rows)).add_hyperlink(r'https://ki81fw4.rnd.ki.sw.ericsson.se'+wantedCase.link, wantedCase.caseName,'')
    sht.range('B'+str(rows)).value = ''.join(wantedCase.errorMsg)
    return rows+1

def addNewCase(sht, rows, wantedCase):
    #sht.range('A'+str(rows)).value = wantedCase.caseName
    print(r'https://ki81fw4.rnd.ki.sw.ericsson.se'+wantedCase.link)
    sht.range('A'+str(rows)).add_hyperlink(r'https://ki81fw4.rnd.ki.sw.ericsson.se'+wantedCase.link, wantedCase.caseName,'')
    sht.range('B'+str(rows)).value = ''.join(wantedCase.errorMsg)
    return rows+1

def saveSections(wantedCases, sht):   
    a1 = sht.range('A1')
    a1.column_width = 50
    b1 = sht.range('B1')
    b1.column_width = 100

    #sht.range("A1:A20").columns.autofit()
    rows = 1
    
    rng = sht.range('A' + str(rows))
    rng.value = 'Pass to Fail'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_pass', 'r_fail', wantedCases, sht, rows)
    
    
    rng = sht.range('A' + str(rows))
    rng.value = 'Pass to Error'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_pass', 'r_error', wantedCases, sht, rows)

    rng = sht.range('A' + str(rows))
    rng.value='Pass to not Executed'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_pass', 'r_missing', wantedCases, sht, rows)

    rng = sht.range('A' + str(rows))
    rng.value='Fail to Fail'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_fail', 'r_fail', wantedCases, sht, rows)

    rng = sht.range('A' + str(rows))
    rng.value='Error to Error'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_error', 'r_error', wantedCases, sht, rows)
    
    rng = sht.range('A' + str(rows))
    rng.value='Error to Fail'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_error', 'r_fail', wantedCases, sht, rows)
    
    rng = sht.range('A' + str(rows))
    rng.value='Fail to Error'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_fail', 'r_error', wantedCases, sht, rows)

    rng = sht.range('A' + str(rows))
    rng.value='not Executed to Fail'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_missing', 'r_fail', wantedCases, sht, rows)

    rng = sht.range('A' + str(rows))
    rng.value='not Executed to Error'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_missing', 'r_error', wantedCases, sht, rows)

    rng = sht.range('A' + str(rows))
    rng.value='Error to not Executed'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_error', 'r_missing', wantedCases, sht, rows)

    rng = sht.range('A' + str(rows))
    rng.value='Fail to not Executed'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_fail', 'r_missing', wantedCases, sht, rows)
    
def saveSection(left, right, wantedCases, sht, rows):    
    print("rows = ", rows)
    flag = False
    prevLevelOneType = 0
    prevLevelTwoType = 0
    for wantedCase in wantedCases:
        if wantedCase.leftStatus == left and wantedCase.rightStatus == right:
            print(wantedCase.toString())
            if not flag:                
                rows = addNewTitle(sht, rows, wantedCase)
                prevLevelOneType = wantedCase.levelOneType
                prevLevelTwoType = wantedCase.levelTwoType                
                flag = True
                #print("first add new title, row = ", rows)
            elif prevLevelOneType != wantedCase.levelOneType: #different xml and TP
                rows = addNewTitle(sht, rows, wantedCase)
                prevLevelOneType = wantedCase.levelOneType
                prevLevelTwoType = wantedCase.levelTwoType
                #print("add new title, row = ", rows)
            elif prevLevelTwoType != wantedCase.levelTwoType: #different class
                rows = addNewClass(sht, rows, wantedCase)
                prevLevelTwoType = wantedCase.levelTwoType
                #print("add new class, row = ", rows)
            else:
                rows = addNewCase(sht, rows, wantedCase) #different case
                #print("add new case, row = ", rows)
    return rows

def generateRerunCmd():
    wantedCases = getResult()
    generateCmd(wantedCases)
    
#generateTestSuite -t sbpsC2_TC3_L -a 40
def generateCmd(wantedCases):
    outCmd = open('rerunCmd.txt', 'w')
    prevLevelOneType = wantedCases[0].levelOneType
    prevTerminal = wantedCases[0].terminal
    suite = wantedCases[0].testSuite
    caseStr = ' -t ' + wantedCases[0].caseName.strip()
    caseCount = 1
    for wantedCase in wantedCases[1:]:
        if wantedCase.levelOneType == prevLevelOneType: #same TP and xml suite
            caseStr += ' -t ' + wantedCase.caseName.strip()
            caseCount += 1
        else:
            if caseCount < 10:
                outCmd.write('generateTestSuite' + caseStr + ' -a ' + str(prevTerminal))
                outCmd.write('\n')
            else:
                outCmd.write('more than 10 cases failed, suggest to rerun ' + suite +  ' on terminal ' + str(prevTerminal))
                outCmd.write('\n')
            prevLevelOneType = wantedCase.levelOneType
            prevTerminal = wantedCase.terminal
            caseStr = ' -t ' + wantedCase.caseName.strip()
            caseCount = 1
            suite = wantedCase.testSuite
    if caseCount < 10:
        outCmd.write('generateTestSuite' + caseStr + ' -a ' + str(prevTerminal))
        outCmd.write('\n')
    else:
        outCmd.write('more than 10 cases failed, suggest to rerun ' + suite +  ' on terminal ' + str(prevTerminal))
        outCmd.write('\n')
    outCmd.close()   
    
def generateExcel(wantedCases):
    print('start!')
    app = xw.App(visible=False, add_book=False)
    wb = app.books.add()
    sht = wb.sheets['sheet1']
    sht.autofit()
        
    print('get result finished!')
    saveSections(wantedCases, sht)
    
    wb.save('result.xlsx')
    wb.close()
    app.quit()
    print('finished!')

def getResult():
    analyzeLog = AnalyzeLog()
    analyzeLog.process()
    return analyzeLog.testcaseList

wantedCases = getResult()
#generateExcel(wantedCases)
generateCmd(wantedCases)

#todo:different xml suite set different case count
#todo:no-matching part
#todo:add TR number and link

'''
app = xw.App(visible=False, add_book=False)
wb = app.books.add()
sht = wb.sheets['sheet1']
rng = sht.range('A1')

#rng.value = 'Pass to Fail'
titleStyle(rng)
rng.resize(600)
rng.add_hyperlink('www.baidu.com','baidu', '')
rng.columns.autofit()


wb.save('result.xlsx')
wb.close()
app.quit()
'''
