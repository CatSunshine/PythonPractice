__author__ = "Wendy.wu.a@ericsson.com"
__version__ = "1.0.1"

from bs4 import BeautifulSoup
from Testcase import Testcase
#1.open html, get bs4, get log-diff nodes



class AnalyzeLog:
    '''define tool class.'''
    def __init__(self):
        self.testcaseList = []
        self.testSuite = ''
        self.terminal = 0
        self.radioType = ''
        self.className = ''
        self.levelOneType = 0
        self.levelTwoType = 0
        
    def logDiffNodes(self):
        doc = open('log_diffs', 'r')
        soup = BeautifulSoup(doc, 'html.parser')
        #print(soup.prettify())
        divs = soup.find_all(name='div', attrs={'class':'log-diff'})
        #print(divs[1])
        nodes = []
        divXml = open('divs.html', 'w',encoding='utf-8')
        for div in divs:
            if div.find_all(name='li', attrs={'class':'tcg-diff'}):
                nodes.append(div)
                divXml.writelines(div.prettify())
        doc.close()
        divXml.close()
        print(len(nodes))
        return nodes

    #2.from log-diff nodes get testcases   
    def processNode(self, node):
        self.levelOneType += 1
        testContainer = node.find(name='ul', attrs={'class':'header test_container'})
        self.getTerminalInfo(testContainer)
        tcgDiffs = node.find_all(name='li', attrs={'class':'tcg-diff'})
        for tcgDiff in tcgDiffs:
            self.generateTestcases(tcgDiff)

    def getTerminalInfo(self, testContainer):
        lblbls = testContainer.find_all(name='li',attrs={'class':'lblbl'})
        ct = lblbls[-1].string
        lst = ct.split('-')
        self.testSuite = lst[1]
        start = lst[2].find('(')
        end = lst[2].find(')')
        self.radioType = lst[2][start+1:end]
        start = lst[2].find('Terminal')
        temp = lst[2][start:]
        templst = temp.split(' ')
        self.terminal= int(templst[1])
        #print(info)

    def generateTestcases(self, tcg):
        #print(tcg.span.string)
        self.className = tcg.span.string
        self.levelTwoType += 1
        diffContent = tcg.find(name='ul', attrs={'class':'diff-content'})
        lis = diffContent.findAll(lambda tag: tag.name=='li' and len(tag.attrs)==1)
        for li in lis:
            tc = Testcase()
            tc.testSuite = self.testSuite
            tc.radioType = self.radioType
            tc.terminal = self.terminal
            tc.className = self.className
            tc.levelOneType = self.levelOneType
            tc.levelTwoType = self.levelTwoType
            tc.leftStatus = li.a.span['class'][0]
            next_a = li.a.nextSibling
            while type(next_a)!= type(li.a):
                next_a = next_a.nextSibling
            tc.rightStatus = next_a.span['class'][0]
            if tc.rightStatus == 'r_pass': #today the case passed, not record.
                continue
            tc.link = next_a['href']
            tc.caseName = next_a.span.string
            errorlis = li.find_all(name='li')
            #print('errlist:', len(errorlis))
            if errorlis:
                for errli in errorlis:
                    errorMsg = ''
                    spans = errli.find_all(name='span')
                    #print('span len:',len(spans))
                    for span in spans:
                        #print("single span:",span)
                        if len(span.attrs) > 0 and span['class'][0] == 'known_issue':
                            errorMsg = span.a.string + '\n'
                            #tc.errorMsg += span.a.string + '\n'
                            #print('first a type:',type(span.a))
                            #print("span a:", span.a)
                            next_t = span.a.nextSibling
                            if not next_t:
                                continue
                            while type(next_t)!=type(span.a) and next_t.nextSibling:
                                next_t = next_t.nextSibling
                            #print("next:",next_t)
                            #print('second a type:',type(next_t))
                            if type(next_t)==type(span.a):
                                tc.trlink = next_t['href']
                        elif len(span.attrs) > 0 and span['class'][0] == 'tr':
                            tc.trNum = span.string
                        else:
                            errorMsg = span.string + '\n'
                            #tc.errorMsg += span.string+'\n'
                    if errorMsg not in tc.errorMsg:
                        tc.errorMsg.append(errorMsg)
            #tc.toString()
            self.testcaseList.append(tc)

    def process(self):
        nodes = self.logDiffNodes()
        i = 0
        #self.processNode(nodes[4])
        for node in nodes:
            print(i)
            self.processNode(node)
            i += 1
            
'''      
analyzeLog = AnalyzeLog()
analyzeLog.process()
for testcase in analyzeLog.testcaseList:
    testcase.toString()
'''


