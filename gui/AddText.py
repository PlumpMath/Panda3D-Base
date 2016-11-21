from pandac.PandaModules import *

def load(text, parent = None, color = None, pos = (0, 0, 0), scale = (1, 1, 1), hpr = (0, 0, 0), wrap = None,
            font = None, nodeName = None, shadow = None, shadowColor = (0, 0, 0, 1), leftAlign = False):
    if color == None: color = base.MainGlobals.DefaultTextFg
    if parent == None: parent = base.currentAspect2d
    if nodeName == None: nodeName = "text: %s" % text
    if font == None: font = base.Fonts.Default
    textLoad = TextNode(nodeName)
    textLoad.setText(text)
    if leftAlign == False: textLoad.setAlign(TextNode.ACenter)
    textLoad.setTextColor(color)
    textLoad.setFont(font)
    if not wrap == None: textLoad.setWordwrap(wrap)
    if not shadow == None:
        textLoad.setShadow(shadow)
        textLoad.setShadowColor(shadowColor)
    textCardDemen = str(textLoad.getCardActual())[11:-1]
    textCardHeight = str(float(textCardDemen.split(", ")[2]) * -1 + 1)
    if float(textCardDemen.split(", ")[2]) * -1 <= 0:
        textCardHeight = 0
    else:
        textCardHeight = int(textCardHeight[:textCardHeight.find(".")])
        heightIncreaseNumbers = ([x for x in range(1, 41) if x % 5 == 4])
        for x in heightIncreaseNumbers:
            if textCardHeight > x:
                textCardHeight -= 1

    text = parent.attachNewNode(textLoad)
    text.setPos(pos)
    text.setScale(scale)
    text.setHpr(hpr)
    text.setTag("cardHeight", str(textCardHeight))
    return text
    