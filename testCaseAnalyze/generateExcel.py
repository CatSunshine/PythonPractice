import xlwings as xw
from analyzeLog import AnalyzeLog
def titleStyle(rng):
    rng.api.Font.size = 16
    rng.api.Font.Bold = True
    rng.api.Font.Color = 0x0000ff

def suiteStype(rng):
    rng.api.Font.size = 14
    rng.api.Font.Bold = True
    rng.api.Font.Color = 0xff00ff

def classStype(rng):
    rng.api.Font.size = 10
    rng.api.Font.Bold = False
    rng.api.Font.Color = 0x00ff00

def addNewTitle(sht, rows, wantedCase):
    sht.range('A'+str(rows)).value = wantedCase.testSuite
    sht.range('B'+str(rows)).value = wantedCase.radioType + ' Terminal ' + str(wantedCase.terminal)
    rows += 1
    sht.range('A'+str(rows)).value = wantedCase.className
    rows += 1
    #sht.range('A'+str(rows)).value = wantedCase.caseName
    print(r'https://ki81fw4.rnd.ki.sw.ericsson.se'+wantedCase.link)
    sht.range('A'+str(rows)).add_hyperlink(r'https://ki81fw4.rnd.ki.sw.ericsson.se'+wantedCase.link, wantedCase.caseName,'')
    sht.range('B'+str(rows)).value = wantedCase.errorMsg
    return rows+1

def addNewClass(sht, rows, wantedCase):
    sht.range('A'+str(rows)).value = wantedCase.className
    rows += 1
    #sht.range('A'+str(rows)).value = wantedCase.caseName
    sht.range('A'+str(rows)).add_hyperlink(r'https://ki81fw4.rnd.ki.sw.ericsson.se'+wantedCase.link, wantedCase.caseName,'')
    sht.range('B'+str(rows)).value = wantedCase.errorMsg
    return rows+1

def addNewCase(sht, rows, wantedCase):
    #sht.range('A'+str(rows)).value = wantedCase.caseName
    print(r'https://ki81fw4.rnd.ki.sw.ericsson.se'+wantedCase.link)
    sht.range('A'+str(rows)).add_hyperlink(r'https://ki81fw4.rnd.ki.sw.ericsson.se'+wantedCase.link, wantedCase.caseName,'')
    sht.range('B'+str(rows)).value = wantedCase.errorMsg
    return rows+1

def saveSections(wantedCases, sht):
    rows = 1
    rng = sht.range('A' + str(rows))
    rng.value = 'Pass to Fail'
    titleStyle(rng)
    #rng.autofit()
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
    #sht.range('A1:A'+rows).api.height = 200
    
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
                print("first add new title, row = ", rows)
            elif prevLevelOneType != wantedCase.levelOneType: #different xml and TP
                rows = addNewTitle(sht, rows, wantedCase)
                prevLevelOneType = wantedCase.levelOneType
                prevLevelTwoType = wantedCase.levelTwoType
                print("add new title, row = ", rows)
            elif prevLevelTwoType != wantedCase.levelTwoType: #different class
                rows = addNewClass(sht, rows, wantedCase)
                print("add new class, row = ", rows)
            else:
                rows = addNewCase(sht, rows, wantedCase)
                print("add new class, row = ", rows)
    return rows
                    
def generateExcel():
    print('start!')
    app = xw.App(visible=False, add_book=False)
    wb = app.books.add()
    sht = wb.sheets['sheet1']
    #sht.range('A1:B1').api.width = 400
    
    wantedCases = getResult()
    print('get result finished!')
    saveSections(wantedCases, sht)
    
    wb.save('result.xlsx')
    wb.close()
    app.quit()
    print('finished!')

def getResult():
    analyzeLog = AnalyzeLog()
    analyzeLog.process()
    wantedCases = []
    for testcase in analyzeLog.testcaseList:
        if testcase.rightStatus != 'r_pass':
            wantedCases.append(testcase)
    return wantedCases


generateExcel()
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
