import os
import tkMessageBox
import traceback

for globalFile in os.listdir("globals"):
    if not globalFile.startswith("__init__"):
        if globalFile.endswith(".py") or globalFile.endswith(".pyc"):
            if globalFile.find("-") != -1 or globalFile.find(" ") != -1:
                tkMessageBox.showerror("Global Importer", "Error for \"" + globalFile + "\":\nInvalid Character(s) in Global File Name")
            else:
                importModule = True
                if globalFile.endswith(".py"):
                    globalFile = globalFile.replace(".py", "")
                if globalFile.endswith(".pyc"):
                    globalFile = globalFile.replace(".pyc", "")
                    if not os.path.isfile(globalFile + ".py") == True: importModule = False
                if importModule == True:
                    formatTupple = (os.path.basename("globals"), globalFile)
                    try: exec("from %s import %s" % formatTupple)
                    except: tkMessageBox.showerror("Global Importer", "Error for \"" + globalFile + "\":\n" + traceback.format_exc())
