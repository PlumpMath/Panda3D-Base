from direct.gui.DirectGui import OkDialog, YesNoDialog
from direct.task import Task

base.dialogLock = False

def destroyDialog():
    base.ignore("enter-up")
    base.currentDialogue.destroy()
    base.changeZoneDisabled = False
    base.clickDisabled = False
    base.commandLock = False
    base.dialogLock = False

def prepareShow():
    base.dialogLock = True
    base.clickDisabled = True
    base.changeZoneDisabled = True

def loadDialogImage():
    return base.loadModel("phase_3/models/gui/tt_m_gui_ups_panelBg.bam")

def loadButtonImage():
    return base.loadModel("phase_3/models/gui/dialog_box_buttons_gui.bam")

def okSend(button = None, command = None, destroy = True):
    if isinstance(command, list):
        extraArgs = command
        try: command = extraArgs[0]
        except: command = None
        try: destory = extraArgs[1]
        except: destory = True

    if destroy == True: destroyDialog()
    if not command == None:
        base.removeZoneExempt = True
        exec(command)

def yesNoSend(button, yesCommand = None, noCommand = None, destroy = True):
    if destroy == True: destroyDialog()
    if button == True:
        if not yesCommand == None: exec(yesCommand)
    else:
        if not noCommand == None: exec(noCommand)

def dialog(text, extraArgs = [], scale = 1):
    if not base.dialogLock == True:
        prepareShow()
        buttonImage = loadButtonImage()
        base.currentDialogue = OkDialog(image = loadDialogImage(), text = text, command = okSend,
                                extraArgs = extraArgs, sidePad = 0.15, topPad = 0.1, midPad = -0.03, scale = scale,
                                buttonGeomList = [buttonImage.find('**/ChtBx_OKBtn_UP')], button_relief=None,
                                button_text_pos = (0, -0.105))
        base.currentDialogue.find("**/DirectButton-*").removeNode()
        return base.currentDialogue

def okDialog(text, extraArgs = [], scale = 1):
    if not base.dialogLock == True:
        prepareShow()
        buttonImage = loadButtonImage()
        base.currentDialogue = OkDialog(image = loadDialogImage(), text = text, command = okSend,
                                extraArgs = extraArgs, sidePad = 0.15, topPad = 0.1, scale = scale,
                                buttonGeomList = [buttonImage.find('**/ChtBx_OKBtn_UP')], button_relief=None,
                                button_text_pos = (0, -0.105))
        def keyboardEnter(): okSend(None, extraArgs)
        taskMgr.doMethodLater(0.001, base.accept, "addDialog_enterHotkeyDelay", extraArgs = ["enter-up", keyboardEnter])
        return base.currentDialogue

def yesNoDialog(text, extraArgs = [], scale = 1):
    if not base.dialogLock == True:
        prepareShow()
        buttonImage = loadButtonImage()
        base.currentDialogue = YesNoDialog(image = loadDialogImage(), text = text, command = yesNoSend,
                                extraArgs = extraArgs, sidePad = 0.15, topPad = 0.1, scale = scale,
                                buttonGeomList = [buttonImage.find('**/ChtBx_OKBtn_UP'), buttonImage.find('**/CloseBtn_UP')], button_relief=None,
                                button_text_pos = (0, -0.105))
        return base.currentDialogue