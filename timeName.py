import re
import textwrap
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

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
        'timeColor': '#879977',
        'xGapL': 115,
        'xGapR': 35,
        'yGapT': 10,
        'xSTime': 575,
        'xRTime': 530,
        'chatWidth': 570,
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
        chatFont = ImageFont.truetype('whatsapp_assets/Roboto-Regular.ttf', self.attrDict['fontSize'])
        timeFont = ImageFont.truetype('whatsapp_assets/Roboto-Regular.ttf', 25)

       
        if self.person == 'sender':
            txtD.text((self.attrDict['xGapL'] + self.attrDict['bufferWidth'], self.attrDict['yGapT'] + self.attrDict['bufferHeight']), self.sM, font=chatFont, fill='#000000')
            txtD.text((self.attrDict['xSTime'], self.attrDict['textHeight']-35), self.time, font=timeFont, fill=self.attrDict['timeColor'])
        else:
            txtD.text((self.attrDict['xGapR'] + self.attrDict['bufferWidth'], self.attrDict['yGapT'] + self.attrDict['bufferHeight']), self.sM, font=chatFont, fill='#000000')
            txtD.text((self.attrDict['xRTime'], self.attrDict['textHeight']-35), self.time, font=timeFont, fill=self.attrDict['timeColor'])

        return txt

    def makeChatLine(self):
        
        xGapL = self.attrDict['xGapL']
        yGapT = self.attrDict['yGapT']
        xGapR = self.attrDict['xGapR']

        im = Image.new('RGBA', (720, self.attrDict['totalHeight']), self.attrDict['backgroundColor'])
        imD = ImageDraw.Draw(im, 'RGBA')
        
        if self.person == 'sender':
            imD.rectangle([(xGapL, yGapT), (xGapL + self.attrDict['chatWidth'], yGapT + self.attrDict['chatHeight'])], self.attrDict['chatboxColor1'], self.attrDict['outlineColor'])
        else:
            imD.rectangle([(xGapR, yGapT), (xGapR + self.attrDict['chatWidth'], yGapT + self.attrDict['chatHeight'])], self.attrDict['chatboxColor2'], self.attrDict['outlineColor'])

        if self.person == 'sender':
            blueTick = Image.open('whatsapp_assets/bluetick.png')
            im.paste(blueTick, (643, self.attrDict['textHeight']-27)) #643 is the X-position, located 27 pixels from bottom of the chat snippet

        txt = self.textFormat()
        out = Image.alpha_composite(im, txt)
        # out.show()
        return out

    def getChatHeight(self):
        return self.attrDict['totalHeight']


def parseChat():

    f = open('chat.txt','r')
    appName = 'WhatsApp'

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

    stitchChat(chatHeightList, chatImgList, you, peopleList)


def findYou(peopleList):
    print "Who you?" 
    for i in range(len(peopleList)):
        dispStr = str(i+1) + ': ' + peopleList[i]
        print dispStr
    
    pN = int(raw_input("Type option number: "))
    return peopleList[pN-1]


def stitchChat(chatHeightList, chatImgList, you, peopleList):

    screenHeight = sum(chatHeightList)
    im = Image.new('RGBA', (720, 163+screenHeight+230), WhatsAppAttr['backgroundColor'])
   
    im.paste(Image.open('whatsapp_assets/top.png'), (0, 0))

    offset = [0, 163]
    i = 0

    for img in chatImgList:
        offsetTuple = tuple(offset)
        im.paste(img, offsetTuple)
        offset[1] += chatHeightList[i]
        i += 1
    
    offsetTuple = tuple(offset)
    im.paste(Image.open('whatsapp_assets/bottom.png'), offsetTuple) 

    imD = ImageDraw.Draw(im, 'RGBA')

    if len(peopleList) > 2:
        titleText = 'Group'
    else:
        for i in peopleList:
            if i != you:
                rec = i
        titleText = rec

    titleFont = ImageFont.truetype('whatsapp_assets/Roboto-Bold.ttf', 35)
    imD.text((140, 80), titleText, font=titleFont, fill='#ffffff') 
    
    dateText = datetime.now().strftime('%H:%M')
    dateFont = ImageFont.truetype('whatsapp_assets/Roboto-Regular.ttf', 30)
    imD.text((630, 6), dateText, font=dateFont, fill='#ffffff')

    im.show()


parseChat()
