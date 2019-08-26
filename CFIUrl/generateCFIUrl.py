__author__ = "Wendy.wu.a@ericsson.com"
__version__ = "1.0.1"

import sys

def generateCFIUrl(urlToTest):
    if urlToTest.find('#') == -1:
        totalUrl = "https://rbs-g2.rnd.ki.sw.ericsson.se/proj/rbs-g2-tmp/proj/crbs/ennsjjn/newCfi/?" + urlToTest
        print(totalUrl)
        return totalUrl
    index = urlToTest.split('/')[-1]
    endIndex = urlToTest.find('#')
    
    url = urlToTest[:endIndex]
    unifiedUrl = url+'testcase.html?index=' + index
    totalUrl = "https://rbs-g2.rnd.ki.sw.ericsson.se/proj/rbs-g2-tmp/proj/crbs/ennsjjn/newCfi/?" + unifiedUrl
    print(totalUrl)
    return totalUrl

def SaveCFIUrl(urlToTest):
    fi = open('CFIUrl.txt', 'w', encoding = 'utf-8')
    url = generateCFIUrl(urlToTest)
    fi.write(url)
    fi.close()

def main(argv = None):
    if argv is None:
        argv = sys.argv
        if len(argv) < 2:
            print('please input the jcat URL.')
        else:
            SaveCFIUrl(argv[1])
            
#SaveCFIUrl("http://ki81fw4.rnd.ki.sw.ericsson.se/executions/1020607/results/117/xilinxUS_32xx_dev.xlf/SwCharSuite.xml/JCAT_logs/#/testcase/6")

if __name__ == '__main__':
    main()
    
