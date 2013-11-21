import sys, os
import urllib, urllib2 
import re

def roman_to_arab(romStr):
    arab = [1, 4, 5, 9, 10, 40, 50, 90, 100, 400, 500, 900, 1000]
    roman = ['I','IV','V','IX','X','XL','L','XC','C','CD','D','CM','M']    
    romStr = romStr.decode("utf-8").upper().encode("utf-8")
    
    arabNum = 0
    i = len(arab) - 1
    pos = 0
    while (i >= 0 and pos < len(romStr)):
        if (romStr[pos:(pos+len(roman[i]))] == roman[i]):
            arabNum = arabNum + arab[i]
            pos = pos + len(roman[i])
        else:
            i = i - 1
    
    return str(arabNum)

def findRoman(line):
    pattern = u'(?i)(\sm{0,3}(d?c{0,3}|c[dm])(i?x{0,3}|x[ic])(v?I{0,3}|i[ix])\s)|(^m{0,3}(d?c{0,3}|c[dm])(i?x{0,3}|x[ic])(v?I{0,3}|i[ix]))\s'
    p = re.compile(pattern, re.I+re.U)
    romanList = re.findall(p, line.decode("utf-8"))
    newList = []    
    
    for romanNum in romanList:    
        for n in romanNum:                 
            if (n != '  ' and n !=''):      #костыль     
                n = ''.join(n.split())
                newList.append(n)                    
        
    newList = [item.lower() for item in newList]
    newList = list(set(newList))
    newList.sort(key=len, reverse=True)
       
    for n in newList:#TODO:в начале строки не видит              
        thisStr = '(^|\W)' + str(n) + '($|\W)'
        line = re.sub(thisStr, ' ' + roman_to_arab(str(n)) + ' ', line, flags=re.I)
    return line

def url_pars(words):
    #заменять в words пробелы на _    
    
    url='http://ru.m.wikipedia.org/wiki/' + words
    headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)'}
    values = {'Host' : 'whois.ripn.net', 'Whois' : 'test.ru'}
    data = urllib.urlencode(values)

    req = urllib2.Request(url, data, headers)   

    #htmlCode = urllib2.urlopen(req).getcode() 
    try:
        html = urllib2.urlopen(req).read()
    except urllib2.URLError, e: # ловим 404 ошибку, если страницы нет
        if e.code == 404:
            return 'Ничего не знаю про это. Давай позже поговорим.'
    else:
        #парсить html
        file = open('/var/persistent/home/nao/logz/test-url.txt','w') #тестовый файл с 'грязным' html
        
        #~ ifile = open('/var/persistent/home/nao/logz/test-url-ish.txt','w')
        text = html.decode("utf-8").lower().encode("utf-8") #понижаем регистр всего текста
        #~ ifile.write(text)
        #~ ifile.close()
        
        text = re.split(u'см. также(?=</span>)|примечания(?=</span>)|литература(?=</span>)|read in another language(?=</span>)',text) #удалить всё после 'см.также' или 'примечания' или 'литература' или 'ссылки' или 'read in another language' 
    
        pars = re.findall(u'<p>.*</p>|<li>.*</li>',text[0]) #найти все параграфы и пункты меню. TODO:Пункты меню обозначить особым способом, сохранить ссылки на них
        
        for n in pars: #ДОБАВИТЬ: удалить теги, кроме ahref для пунктов меню и обозначений для пунктов меню.
            a = re.sub(u'<[^>]+>', '',n) #удалить все теги
            b = re.sub(u'\[[^\]]+\]', '',a) #Удалить [], транскрипции
            c = re.sub(u'\([^\)\(]+\)', '',b)
            d = re.sub(u'т\.е\.', 'то есть',c) #Сокращения заменить на полные фразы
            e = re.sub(u'т\.д\.', 'так далее',d)
            
            #заменить римские цифры на арабские
            e = findRoman(e)           
            
            xor = '[^a-zA-ZА-Яа-я0-9\s\.,-]' #удалить все знаки, кроме a-zA-ZА-Яа-я0-9\s\.,-
            xor = xor.decode("utf-8")
            e = e.decode("utf-8")
            ee = re.sub(xor, '', e)
            ee = ee.encode("utf-8")
            
            file.write(ee + '\n') 
            
            
        file.close()
        phrase = url
        fh = open('/var/persistent/home/nao/logz/test-url.txt')
        parsText = ''
        for line in fh.readlines():                
            parsText = parsText + ' ' + line
        return parsText

            
        
class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        #~ puts code for box initialization here
        pass

    def onUnload(self):
        #~ puts code for box cleanup here
        pass

    def onInput_onStart(self, p):        
        h = url_pars(p)
        self.log(h)
        self.onStopped(h) #~ activate output of the box
        pass

    def onInput_onStop(self):
        self.onUnload() #~ it is recommanded to call onUnload of this box in a onStop method, as the code written in onUnload is used to stop the box as well
        pass
