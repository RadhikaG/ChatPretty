import re
import textwrap
from PIL import Image, ImageDraw, ImageFont

def processMessage(message):
    
    lines = textwrap.wrap(message, width=40)

    sM = ''
    for line in lines:
        sM += line
        sM += '\n'
    
    returnList = [sM, len(lines)]
    return returnList


def textFormat(message): #tested only with WhatsApp

    retList = processMessage(message)
    sM = retList[0]
    lenLines = retList[1] 

    #all the following are WhatsApp specific
    fontSize = 32
    lineHeight = 60 #need to devote 40 pixels for each line of text
    bufferHeight = 10
    bufferWidth = 11 
    chatHeight = lineHeight*lenLines
    textHeight = bufferHeight + chatHeight + bufferHeight


    txt = Image.new('RGBA', (720, textHeight), (255, 255, 255, 0))
    txtD = ImageDraw.Draw(txt, 'RGBA')
    font = ImageFont.truetype('Roboto-Regular.ttf', fontSize)
    
    txtD.text((115+bufferWidth, 10+bufferHeight), sM, font=font, fill='#000000')
    return txt

def makeChatLine(message):#time, name, message):
    
    xGapL = 115
    yGapT = 10
    maxWidth = 570
    xGapR = 35

    #all the following are WhatsApp specific
    bufferHeight = 10
    lineHeight = 60
    lenLines = processMessage(message)[1]
    chatHeight = lineHeight*lenLines
    totalHeight = bufferHeight + chatHeight + bufferHeight
    
    im = Image.new('RGBA', (720, totalHeight), '#fffee8') #replace totalHeight with 1280 for full screen
    imD = ImageDraw.Draw(im, 'RGBA')
    imD.rectangle([(xGapL, yGapT), (xGapL + maxWidth, yGapT + chatHeight)], '#e1ffc7')
   
    txt = textFormat(message)
    out = Image.alpha_composite(im, txt)
    out.show()

def parseChat():
    f = open('chat.txt','r')
    chatImgList = []
    
    tEx = re.compile(r'\[[^a-zA-Z]*\]')
    nEx = re.compile(r' [a-zA-Z ]*:')
    mEx = re.compile(r'(?<=[a-zA-Z]:).*$')

    for line in f.readlines():
        time = tEx.search(line)
        name = nEx.search(line)
        message = mEx.search(line)
        print time.group()
        print name.group()
        print message.group()
        makeChatLine(message.group())
        # chatLineObj = makeChatLine(time.group(), name.group(), message.group())
        # chatImgList.append(chatLineObj)


sampS = """
I like it rough, I like it mean. I like it tough, I like it lean. 
Oh, so I'm a playah', I know. I need no excuses, I know what I choose, I'm tired of you. Whiskeeey, runnin' down your chest.
I say, back down, I ain't done with you. So I'm a playah'.
"""
sampS1 = "Suddenly, I don't need to go to the bathroom anymore."
sampS2 = "I just got an offer to work with one of the maintainers of the Mozilla project."

# makeChatLine(sampS2)
parseChat()
