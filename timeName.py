import re
import textwrap
from PIL import Image, ImageDraw, ImageFont

WhatsAppAttr = {
        'fontSize': 32, 
        'lineHeight': 60, 
        'bufferHeight': 10, 
        'bufferWidth': 11, 
        'backgroundColor': '#fffee8', 
        'chatboxColor1': '#e1ffc7',
        'xGapL': 115,
        'xGapR': 35,
        'yGapT': 10,
        'maxWidth': 570,
}

class Message:
    def __init__(self, appName, message):
        self.message = message
        retList = self.processMessage()
        self.sM = retList[0]
        self.lenLines = retList[1]

        if appName == 'WhatsApp':
            global WhatsAppAttr
            self.attrDict = WhatsAppAttr

        self.attrDict['chatHeight'] = self.attrDict['lineHeight']*self.lenLines 
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
        font = ImageFont.truetype('Roboto-Regular.ttf', self.attrDict['fontSize'])
        
        txtD.text((115+self.attrDict['bufferWidth'], 10+self.attrDict['bufferHeight']), self.sM, font=font, fill='#000000')
        return txt

    def makeChatLine(self):#time, name, message):
        
        xGapL = self.attrDict['xGapL']
        yGapT = self.attrDict['yGapT']
       
        im = Image.new('RGBA', (720, self.attrDict['totalHeight']), self.attrDict['backgroundColor']) #replace totalHeight with 1280 for full screen
        imD = ImageDraw.Draw(im, 'RGBA')
        imD.rectangle([(xGapL, yGapT), (xGapL + self.attrDict['maxWidth'], yGapT + self.attrDict['chatHeight'])], self.attrDict['chatboxColor1'])
       
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

    tEx = re.compile(r'\[[^a-zA-Z]*\]')
    nEx = re.compile(r' [a-zA-Z ]*:')
    mEx = re.compile(r'(?<=[a-zA-Z]:).*$')

    chatImgList = []
    chatHeightList = []

    for line in f.readlines():

        time = tEx.search(line)
        name = nEx.search(line)
        message = mEx.search(line)

        print time.group()
        print name.group()
        print message.group()

        chatLineObj = Message(appName, message.group()) 
        out = chatLineObj.makeChatLine()

        chatHeightList.append(chatLineObj.getChatHeight())
        chatImgList.append(out)

    stitchChat(chatHeightList, chatImgList)


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


sampS = """
I like it rough, I like it mean. I like it tough, I like it lean. 
Oh, so I'm a playah', I know. I need no excuses, I know what I choose, I'm tired of you. Whiskeeey, runnin' down your chest.
I say, back down, I ain't done with you. So I'm a playah'.
"""
sampS1 = "Suddenly, I don't need to go to the bathroom anymore."
sampS2 = "I just got an offer to work with one of the maintainers of the Mozilla project."

# makeChatLine(sampS2)
parseChat()
