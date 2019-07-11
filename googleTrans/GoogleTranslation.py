import urllib.request    
from HandleJs import Py4Js
import re
import time
    
def open_url(url):    
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}      
    req = urllib.request.Request(url = url,headers=headers)    
    response = urllib.request.urlopen(req)    
    data = response.read().decode('utf-8')    
    return data    
    
def translate(content,tk):    
    if len(content) > 4891:    
        print("翻译的长度超过限制！！！")    
        return     
        
    content = urllib.parse.quote(content)    
        
    url = "http://translate.google.cn/translate_a/single?client=t"+ "&sl=en&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca"+"&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1"+"&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s"%(tk,content)    
        
    #返回值是一个多层嵌套列表的字符串形式，解析起来还相当费劲，写了几个正则，发现也很不理想，  
    #后来感觉，使用正则简直就是把简单的事情复杂化，这里直接切片就Ok了    
    result = open_url(url)
    #print(url)
    #print(result)
    end = result.find("\",")    
    if end > 4:    
        return (result[4:end])

def readContent(fileName):
    content = ''
    fileHandler = open(fileName)
    lines = fileHandler.readlines()

    for line in lines:
        content += line
    fileHandler.close()
    return content

def getSentences(content):
    sentences = re.split('[.!?]+', content)
    for sentence in sentences:
        print(sentence)
    return sentences
    
def main():    
    js = Py4Js()    
        
    #while 1:    
    #   content = input("输入待翻译内容：")    
            
     #   if content == 'q!':    
      #      break    
    content = readContent('.\\source.txt')
    print(content)
    print(30*'*')
    sentences = getSentences(content)
    rs = open('result.txt', 'w', encoding = 'utf-8')
    for sentence in sentences:
        tk = js.getTk(sentence)
        result = translate(sentence,tk)
        print(300*'*')
        print(result)
        if result:
            rs.write(result)
        time.sleep(0.3)

    rs.close()
    
    
if __name__ == "__main__":    
    main() 
