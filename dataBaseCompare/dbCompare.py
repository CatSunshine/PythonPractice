import xlwings as xw

def getDbValues(file, key):
    dbValues = {}
    f = open(file, 'rb')
    for line in f.readlines():
        li = str(line).strip()
        #print(li.find('\\t'))
        lineSt = li.replace('\\t', ' ')
        lineSt = li.replace('\\r\\n', '')
        dbValue = getDbValue(lineSt, key)
        if dbValue:
            #print(dbValue)
            if dbValue[0] in dbValues:
                contents = dbValues.get(dbValue[0])
                contents[0].append(dbValue[1])
                contents[1].append(dbValue[2])
                contents[2].append(dbValue[3])
            else:
                dbValues[dbValue[0]] = [[dbValue[1]], [dbValue[2]],[dbValue[3]]]
            
    f.close()
    #print(dbValues)
    return dbValues

def getDbValue(line, key):
    ls = line.split(':')
    if len(ls) < 3:
        return None
    file = ls[0][2:] + ' +' +ls[1]
    temp = ls[2]
    s = temp.find('/*')
    if s!=-1:
        pure = temp[:s].strip()
    else:
        pure = temp.strip()
    #print(pure)
    if pure.find('/') == -1:
        return None
    key_start = pure.find(key)
    #print('key:' + key + ',start:' + str(key_start))
    key_end = pure.find(' ')
    key = pure[key_start+len(key):key_end]
    value = pure[key_end:].strip()
    dbKey = key.strip()
    key_total = pure[:key_end].strip()
    value_start = value.find(' ')
    dbValue=value.strip()[value_start:]
    return dbKey, file, dbValue, key_total

def getStrings(listValue):
    strRes = ''
    for value in listValue:
        strRes += value + '\n'
    return strRes[:len(strRes)-1]
    
def compareResult(inputLists):
    print('start!')
    key1Dic = getDbValues(inputLists[0][0], inputLists[0][1])
    key2Dic = getDbValues(inputLists[1][0], inputLists[1][1])
    app = xw.App(visible = False, add_book = False)
    wb = app.books.add()
    sht = wb.sheets['sheet1']
    sht.autofit()    

    a1 = sht.range('A1')
    a1.column_width = 30
    a1.value = 'key1_key'
    
    b1 = sht.range('B1')
    b1.column_width = 30
    b1.value = 'key2_key'
    
    c1 = sht.range('C1')
    c1.column_width = 20
    c1.value = 'key1_value'
    
    d1 = sht.range('D1')
    d1.column_width = 20
    d1.value = 'key2_value'

    e1 = sht.range('E1')
    e1.column_width = 40
    e1.value = 'key1_file'

    e1 = sht.range('F1')
    e1.column_width = 40
    e1.value = 'key2_file'
                                 
    rows = 2
    f = open('compare_result.txt', 'w')
    f.write(inputLists[0][0] + '    ' + inputLists[0][1] + '\n')
    for key in key1Dic.keys():
        if key in key2Dic:
            rng = sht.range('A' + str(rows))
            rng.value = getStrings(key1Dic[key][2])
            rng = sht.range('E' + str(rows))
            rng.value = getStrings(key1Dic[key][0])
            rng = sht.range('C' + str(rows))
            rng.value = getStrings(key1Dic[key][1])
            rng = sht.range('F' + str(rows))
            rng.value = getStrings(key2Dic[key][0])
            rng = sht.range('D' + str(rows))
            rng.value = getStrings(key2Dic[key][1])
            rng = sht.range('B' + str(rows))
            rng.value = getStrings(key2Dic[key][2])
            rows += 1
        else:
            cts = key1Dic[key]
            for i in range(len(cts[0])):
                f.write(cts[2][i] + '\n')
                f.write(cts[0][i] + '   ' + cts[1][i] + '\n')
            f.write('\n')
    f.write('\n')
    f.write('*'*80)
    f.write('\n')
    f.write(inputLists[1][0] + '    ' + inputLists[1][1] + '\n')
    for key in key2Dic.keys():
        if key in key1Dic:
            pass
        else:
            cts = key2Dic[key]
            for i in range(len(cts[0])) :
                f.write(cts[2][i] + '\n')
                f.write(cts[0][i] + '   ' + cts[1][i] + '\n')
            f.write('\n')
            
    f.close()
    wb.save('result.xlsx')
    wb.close()
    app.quit()
    print('finish!')

inputLists = [['60M_3239_db.txt', '/nrTdd600_Id17'], ['80M_3239_total_db.txt', '/nrTdd800_Id43']]
compareResult(inputLists)
