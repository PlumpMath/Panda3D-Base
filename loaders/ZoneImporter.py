import os
import tkMessageBox
import traceback

for zone in os.listdir("zones"):
    if not zone.startswith("__init__"):
        if zone.endswith(".py") or zone.endswith(".pyc"):
            if zone.find("-") != -1 or zone.find(" ") != -1:
                tkMessageBox.showerror("Zone Importer", "Error for \"" + zone + "\":\nInvalid Character(s) in Zone Name")
            else:
                importModule = True
                if zone.endswith(".py"):
                    zone = zone.replace(".py", "")
                if zone.endswith(".pyc"):
                    zone = zone.replace(".pyc", "")
                    if not os.path.isfile(zone + ".py") == True: Import = False
                if importModule == True:
                    formatTupple = (os.path.basename("zones"), zone)
                    try: exec("from %s import %s" % formatTupple)
                    except: tkMessageBox.showerror("Zone Importer", "Error for \"" + zone + "\":\n" + traceback.format_exc())
