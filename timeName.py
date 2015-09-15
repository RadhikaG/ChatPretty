import re
import textwrap
from PIL import Image, ImageDraw, ImageFont

WhatsAppAttr = {
        'fontSize': 32, 
        # 'lineHeight': 55,
        'lineHeight': 60, 
        'bufferHeight': 5,
        # 'bufferHeight': 10, 
        'bufferWidth': 11, 
        'backgroundColor': '#efe7de', 
        'outlineColor': '#c5bfb6',
        'chatboxColor1': '#e1ffc7',
        'chatboxColor2': '#ffffff',
        'xGapL': 115,
        'xGapR': 35,
        'yGapT': 10,
        'maxWidth': 570,
}

class Message:
    def __init__(self, appName, time, person, message):
        
        self.time = time
        self.person = person
        self.message = message
        retList = self.processMessage()
        self.sM = retList[0]
        self.lenLines = retList[1]

        if appName == 'WhatsApp':
            global WhatsAppAttr
            self.attrDict = WhatsAppAttr

        self.attrDict['chatHeight'] = self.attrDict['lineHeight'] * self.lenLines 
        self.attrDict['textHeight'] = self.attrDict['bufferHeight'] + self.attrDict['chatHeight'] + self.attrDict['bufferHeight']
        self.attrDict['totalHeight'] = self.attrDict['bufferHeight'] + self.attrDict['chatHeight'] + self.attrDict['bufferHeight']
        
        # self.makeVariables()

    # def makeVariables(self):
        # for key in self.attrDict.keys():
            # varName = 'self.' + key
        
    def processMessage(self):
        
        lines = textwrap.wrap(self.message, width=40)

        sM = ''
        for line in lines:
            sM += line
            sM += '\n'
        
        returnList = [sM, len(lines)]
        return returnList


    def textFormat(self): #tested only with WhatsApp

        txt = Image.new('RGBA', (720, self.attrDict['textHeight']), (255, 255, 255, 0))
        txtD = ImageDraw.Draw(txt, 'RGBA')
        chatFont = ImageFont.truetype('Roboto-Regular.ttf', self.attrDict['fontSize'])
        timeFont = ImageFont.truetype('Roboto-Regular.ttf', 25)

       
        if self.person == 'sender':
            txtD.text((self.attrDict['xGapL'] + self.attrDict['bufferWidth'], self.attrDict['yGapT'] + self.attrDict['bufferHeight']), self.sM, font=chatFont, fill='#000000')
            # txtD.text((575, self.attrDict['textHeight']), self.time, font=timeFont, fill='#879977')
            txtD.text((580, self.attrDict['textHeight']-35), self.time, font=timeFont, fill='#879977')
        else:
            txtD.text((self.attrDict['xGapR'] + self.attrDict['bufferWidth'], self.attrDict['yGapT'] + self.attrDict['bufferHeight']), self.sM, font=chatFont, fill='#000000')
            # txtD.text((550, self.attrDict['textHeight']), self.time, font=timeFont, fill='#879977')
            txtD.text((530, self.attrDict['textHeight']-35), self.time, font=timeFont, fill='#879977')

        return txt

    def makeChatLine(self):
        
        xGapL = self.attrDict['xGapL']
        yGapT = self.attrDict['yGapT']
        xGapR = self.attrDict['xGapR']

        im = Image.new('RGBA', (720, self.attrDict['totalHeight']), self.attrDict['backgroundColor'])
        imD = ImageDraw.Draw(im, 'RGBA')
        
        if self.person == 'sender':
            imD.rectangle([(xGapL, yGapT), (xGapL + self.attrDict['maxWidth'], yGapT + self.attrDict['chatHeight'])], self.attrDict['chatboxColor1'], self.attrDict['outlineColor'])
        else:
            imD.rectangle([(xGapR, yGapT), (xGapR + self.attrDict['maxWidth'], yGapT + self.attrDict['chatHeight'])], self.attrDict['chatboxColor2'], self.attrDict['outlineColor'])

        txt = self.textFormat()
        out = Image.alpha_composite(im, txt)
        # out.show()
        return out

    def getChatHeight(self):
        # print self.attrDict['totalHeight']
        return self.attrDict['totalHeight']


def parseChat():

    f = open('chat.txt','r')
    appName = 'WhatsApp'

    # tEx = re.compile(r'\[[^a-zA-Z]*\]')
    tEx = re.compile(r'(?<=[0-9] )[0-9:]+[^\]]')
    nEx = re.compile(r'(?<= )[a-zA-Z]+[^:]*')
    mEx = re.compile(r'(?<=[a-zA-Z]: ).*$')

    chatImgList = []
    chatHeightList = []
    peopleList = []
    
    for line in f.readlines():
        name = nEx.search(line).group()
        if name not in peopleList:
            peopleList.append(name)

    you = findYou(peopleList)

    f.seek(0)

    for line in f.readlines():

        time = tEx.search(line).group()
        name = nEx.search(line).group()
        message = mEx.search(line).group()

        print time
        print name
        print message
        
        if name == you:
            person = 'sender'
        else:
            person = 'receiver'

        chatLineObj = Message(appName, time, person, message) 
        out = chatLineObj.makeChatLine()

        chatHeightList.append(chatLineObj.getChatHeight())
        chatImgList.append(out)

    stitchChat(chatHeightList, chatImgList)


def findYou(peopleList):
    print "Who you?" 
    for i in range(len(peopleList)):
        dispStr = str(i+1) + ': ' + peopleList[i]
        print dispStr
    
    pN = int(raw_input("Enter you. Type option number: "))
    return peopleList[pN-1]


def stitchChat(chatHeightList, chatImgList):

    screenHeight = sum(chatHeightList)
    im = Image.new('RGBA', (720, screenHeight), WhatsAppAttr['backgroundColor'])
    
    offset = [0, 0]
    i = 0

    for img in chatImgList:
        offsetTuple = tuple(offset)
        im.paste(img, offsetTuple)
        offset[1] += chatHeightList[i]
        i += 1

    im.show()


parseChat()
