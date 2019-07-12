__author__ = "Wendy.wu.a@ericsson.com"
__version__ = "1.0.1"

import xlwings as xw
from analyzeLog import AnalyzeLog
import sys

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
    return addNewClass(sht, rows, wantedCase)

def addNewClass(sht, rows, wantedCase):
    sht.range('A'+str(rows)).value = wantedCase.className
    classStype(sht.range('A'+str(rows)))
    rows += 1
    return addNewCase(sht, rows, wantedCase)

def addNewCase(sht, rows, wantedCase):
    #sht.range('A'+str(rows)).value = wantedCase.caseName
    #print(r'https://ki81fw4.rnd.ki.sw.ericsson.se'+wantedCase.link)
    sht.range('A'+str(rows)).add_hyperlink(r'https://ki81fw4.rnd.ki.sw.ericsson.se'+wantedCase.link, wantedCase.caseName,'')
    sht.range('B'+str(rows)).value = ''.join(wantedCase.errorMsg)
    if wantedCase.trlink:
        sht.range('C' + str(rows)).add_hyperlink(wantedCase.trlink, wantedCase.trNum, '')
    return rows+1

def saveSections(analyzeLog, sht):   
    a1 = sht.range('A1')
    a1.column_width = 50
    b1 = sht.range('B1')
    b1.column_width = 100
    c1 = sht.range('C1')
    c1.column_width = 10
    
    rows = 1
    print("save pass to fail")
    wantedCases = analyzeLog.testcaseList
    rng = sht.range('A' + str(rows))
    rng.value = 'Pass to Fail'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_pass', 'r_fail', wantedCases, sht, rows)
    
    print("save pass to error")
    rng = sht.range('A' + str(rows))
    rng.value = 'Pass to Error'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_pass', 'r_error', wantedCases, sht, rows)

    print("save pass to not Executed")
    rng = sht.range('A' + str(rows))
    rng.value='Pass to not Executed'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_pass', 'r_missing', wantedCases, sht, rows)

    print("save fail to fail")
    rng = sht.range('A' + str(rows))
    rng.value='Fail to Fail'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_fail', 'r_fail', wantedCases, sht, rows)

    print("save error to error")
    rng = sht.range('A' + str(rows))
    rng.value='Error to Error'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_error', 'r_error', wantedCases, sht, rows)

    print("save error to fail")
    rng = sht.range('A' + str(rows))
    rng.value='Error to Fail'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_error', 'r_fail', wantedCases, sht, rows)

    print("save fail to error")
    rng = sht.range('A' + str(rows))
    rng.value='Fail to Error'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_fail', 'r_error', wantedCases, sht, rows)

    print("save not executed to fail")
    rng = sht.range('A' + str(rows))
    rng.value='not Executed to Fail'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_missing', 'r_fail', wantedCases, sht, rows)

    print("save not executed to error")
    rng = sht.range('A' + str(rows))
    rng.value='not Executed to Error'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_missing', 'r_error', wantedCases, sht, rows)

    print("save not error to not executed")
    rng = sht.range('A' + str(rows))
    rng.value='Error to not Executed'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_error', 'r_missing', wantedCases, sht, rows)

    print("save fail to not executed")
    rng = sht.range('A' + str(rows))
    rng.value='Fail to not Executed'
    titleStyle(rng)
    rows += 1
    rows = saveSection('r_fail', 'r_missing', wantedCases, sht, rows)

    print("save left non-matching")
    rng = sht.range('A' + str(rows))
    rng.value='Non-Matching Left'
    titleStyle(rng)
    rows += 1
    rows = saveLeftNonMatch(analyzeLog.leftNonMatch, sht, rows)

    print("save right non-matching")
    rng = sht.range('A' + str(rows))
    rng.value='Non-Matching Right'
    titleStyle(rng)
    rows += 1
    rows = saveRightNonMatch(analyzeLog.rightNonMatch, sht, rows)

def saveLeftNonMatch(leftNonMatch, sht, rows):
    if len(leftNonMatch) == 0:
        return
    #print(leftNonMatch)
    flag = False
    tempTp = 0
    suites = ''
    radioType = ''
    for lst in leftNonMatch:
        Tp = lst[2]
        if not flag:
            tempTp = Tp
            suites = lst[0] + '\n'
            radioType = lst[1]
            flag = True
        else:
            if Tp == tempTp:
                suites += lst[0] + '\n'
            else: #different Tp, save previous Tp first
                sht.range('A'+str(rows)).value = suites[0:len(suites)-1]
                sht.range('B'+str(rows)).value = radioType + ' Terminal ' + str(tempTp)
                suiteStype(sht.range('B'+str(rows)))
                rows += 1
                tempTp = Tp
                suites = lst[0] + '\n'
                radioType = lst[1]
    sht.range('A'+str(rows)).value = suites[0:len(suites)-1]
    sht.range('B'+str(rows)).value = radioType + ' Terminal ' + str(tempTp)
    suiteStype(sht.range('B'+str(rows)))
    return rows + 1

def saveRightNonMatch(rightNonMatch, sht, rows):
    #print('rightNonMatch:',rightNonMatch)
    flag = False
    tempTp = 0
    for lst in rightNonMatch:
        sht.range('A'+str(rows)).add_hyperlink(r'https://ki81fw4.rnd.ki.sw.ericsson.se'+lst[3], lst[0],'')
        Tp = lst[2]
        if not flag:
            tempTp = Tp
            sht.range('B'+str(rows)).value = lst[1] + ' Terminal ' + str(tempTp)
            suiteStype(sht.range('B'+str(rows)))
            flag = True
        else:
            if Tp == tempTp:
                pass
            else: #different Tp, save new TP
                tempTp = Tp
                sht.range('B'+str(rows)).value = lst[1] + ' Terminal ' + str(tempTp)
                suiteStype(sht.range('B'+str(rows)))
        rows += 1
    return rows
    
def saveSection(left, right, wantedCases, sht, rows):    
    print("rows = ", rows)
    flag = False
    prevLevelOneType = 0
    prevLevelTwoType = 0
    for wantedCase in wantedCases:
        if wantedCase.leftStatus == left and wantedCase.rightStatus == right:
            #print(wantedCase.toString())
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
    if len(wantedCases) == 0:
        outCmd.write('no case failed, do not need to rerun. \n')
        outCmd.close()
        return
    prevLevelOneType = wantedCases[0].levelOneType
    prevTerminal = wantedCases[0].terminal
    suite = wantedCases[0].testSuite
    caseStr = ' -t ' + wantedCases[0].caseName.strip()
    caseCount = 1
    if len(wantedCases) == 1:
        outCmd.write('generateTestSuite' + caseStr + ' -a ' + str(prevTerminal))
        outCmd.close()
        return
    for wantedCase in wantedCases[1:]:
        if wantedCase.levelOneType == prevLevelOneType: #same TP and xml suite
            caseStr += ' -t ' + wantedCase.caseName.strip()
            caseCount += 1
        else:
            if caseCount < 20:
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
    
def generateExcel(analyzeLog, excelName):
    print('start!')
    app = xw.App(visible=False, add_book=False)
    wb = app.books.add()
    sht = wb.sheets['sheet1']
    sht.autofit()
        
    print('get result finished!')
    saveSections(analyzeLog, sht)
    
    wb.save(excelName + '.xlsx')
    wb.close()
    app.quit()
    print('finished!')

def getResult():
    analyzeLog = AnalyzeLog()
    analyzeLog.process()
    return analyzeLog.testcaseList

#wantedCases = getResult()
#generateExcel(wantedCases, 'R78Result')
#generateCmd(wantedCases)

def main(argv = None):
    if argv is None:
        argv = sys.argv
    if len(argv)<2:
        print('please input a excel name.')
    else:
        analyzeLog = AnalyzeLog()
        analyzeLog.process()
        generateExcel(analyzeLog, argv[1])
        generateCmd(analyzeLog.testcaseList)

if __name__ == '__main__':
    #argv = ['', 'result']
    main()
#todo:different xml suite set different case count
#todo:no-matching part --done
#todo:add TR number and link --done
#todo:optmize rerunCmd function

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
