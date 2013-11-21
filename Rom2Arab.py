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


class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        pass

    def onLoad(self):
        #~ puts code for box initialization here
        pass

    def onUnload(self):
        #~ puts code for box cleanup here
        pass

    def onInput_onStart(self, line):
        #line = line.decode("utf-8")
        #line = 'VII fjghflowri XIV vii xii i ii i xiv fjkdls привет'
        pattern = u'(?i)(\sm{0,3}(d?c{0,3}|c[dm])(i?x{0,3}|x[ic])(v?I{0,3}|i[ix])\s)|(^m{0,3}(d?c{0,3}|c[dm])(i?x{0,3}|x[ic])(v?I{0,3}|i[ix]))\s'
        #pattern = '^m{0,3}(cm|cd|d?c{0,3})(xc|xl|l?x{0,3})(ix|iv|v?i{0,3})$'
        #pattern = 'm?m?m?(cm|cd|d?c?c?c?)(xc|xl|l?x?x?x?)(ix|iv|v?i?i?i?)$'
        #pattern = '\s*i*v*x*v*i\s'
        p = re.compile(pattern, re.I+re.U)
        romanList = re.findall(p, line.decode("utf-8"))
        self.log(romanList)
        newList = []    
        
        for romanNum in romanList:    
            for n in romanNum:                 
                if (n != '  ' and n !=''):      #костыль     
                    n = ''.join(n.split())
                    newList.append(n)                    
        self.log(newList)
        
        newList = [item.lower() for item in newList]
        newList = list(set(newList))
        newList.sort(key=len, reverse=True)
        self.log(newList)
        
        for n in newList:#TODO:в начале строки не видит
            #n = n.encode("utf-8")   
            #line = line.encode("utf-8")                
            thisStr = '(^|\W)' + str(n) + '($|\W)'
            line = re.sub(thisStr, ' ' + roman_to_arab(str(n)) + ' ', line, flags=re.I)
            self.log(line)
        self.onStopped(line) #~ activate output of the box
        pass

    def onInput_onStop(self):
        self.onUnload() #~ it is recommended to call onUnload of this box in a onStop method, as the code written in onUnload is used to stop the box as well
        pass
