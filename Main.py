from direct.gui import DirectGuiGlobals
from direct.interval.IntervalGlobal import Sequence
from direct.interval.IntervalGlobal import Func
from direct.showbase.ShowBase import ShowBase
import os
from globals import MainGlobals
from panda3d.core import Filename
from panda3d.core import loadPrcFileData
from panda3d.core import Point3
from panda3d.core import VirtualFileSystem
import sys
import Tkinter
import tkMessageBox
import traceback

reload(sys)
sys.setdefaultencoding('UTF8')

loadPrcFileData("", "window-title %s" % MainGlobals.WINDOWTITLE)
loadPrcFileData("", "win-size %s" % MainGlobals.WINDOWSIZE)
loadPrcFileData("", "win-origin %s" % MainGlobals.WINDOWORIGIN)
loadPrcFileData("", "win-fixed-size %s" % MainGlobals.WINDOWFIXED)
loadPrcFileData("", "undecorated %s" % MainGlobals.WINDOWUNDECORATED)
loadPrcFileData("", "window-type %s" % MainGlobals.WINDOWSHOW)
if not MainGlobals.CACHEMODELS: loadPrcFileData("", "model-cache-dir")

tkinter = Tkinter.Tk()
tkinter.withdraw()

mf = VirtualFileSystem.getGlobalPtr()
for root, dirnames, filenames in os.walk("models"):
    for filename in filenames:
        if os.path.splitext(filename)[1] == ".mf":
            multifiles = os.path.join(root, filename)
            mf.mount(Filename(multifiles), ".", VirtualFileSystem.MFReadOnly)

class Main(ShowBase):
    def __init__(base):
        ShowBase.__init__(base)
        base.rootDirectory = os.getcwd()
        base.MainGlobals = MainGlobals
        base.tkinter = tkinter

        from gui import AddDialog
        from gui import AddText
        from loaders import FontLoader
        from loaders import GlobalsImporter
        from loaders import ZoneImporter
        from other import Database
        from other import FileIO

        base.AddDialog = AddDialog
        base.AddText = AddText
        base.Fonts = FontLoader
        base.Globals = GlobalsImporter
        base.Zones = ZoneImporter
        base.Database = Database
        base.FileIO = FileIO

        DirectGuiGlobals.setDefaultFontFunc(lambda: base.loadFont(base.MainGlobals.DefaultFontPath))
        base.setDefaultBackgroundColor()
        base.disableMouse()
        base.existsList = []
        if MainGlobals.DEBUGENABLED:
            base.commandCheck()
        base.currentZoneModule = None
        base.removeZoneExempt = False
        from other import Startup

    def commandCheck(base):
        def check(task):
            if not base.commandLock == True:
                base.commandLock = True
                try: base.currentCommand = base.FileIO.read(debugFileName)
                except:
                    if not os.path.isfile(debugFileName):
                        base.FileIO.newFile(debugFileName)
                        try: base.currentCommand = base.FileIO.read(debugFileName)
                        except: base.currentCommand = ""
                    else: base.currentCommand = ""
                if not base.currentCommand == base.lastCommand:
                    base.FileIO.write(lastCommandFileName, base.currentCommand)
                    base.lastCommand = base.currentCommand
                    try: base.execCommand(base.currentCommand)
                    except:
                        rootBasename = os.path.basename(base.rootDirectory)
                        tracebackFormatted = traceback.format_exc()
                        tracebackFormatted = tracebackFormatted.replace(base.rootDirectory, rootBasename)
                        start = tracebackFormatted.find("  File")
                        end = tracebackFormatted.find("  File \"<string>\"")
                        tracebackFormatted = tracebackFormatted[:start] + tracebackFormatted[end:]
                        print tracebackFormatted
                        tkMessageBox.showerror(base.MainGlobals.WINDOWTITLE, tracebackFormatted)
                        base.commandLock = False
                    else: base.commandLock = False
                else: base.commandLock = False
            return task.cont
        debugFileName = "Debug.py"
        lastCommandFileName = "Last Command"
        base.FileIO.newFile(lastCommandFileName, True)
        base.commandLock = False
        base.lastCommand = base.FileIO.read(lastCommandFileName)
        taskMgr.add(check, "commandCheck")
        
    def changeZone(base, newZone, extraArgs = None, sequence = True):
        if base.MainGlobals.CHANGEZONESEQUENCE and sequence and base.exists("currentNodes"):
            if not newZone == base.currentZoneModule:
                base.addExists("changeZone_runSequence")
                Sequence(base.currentAspect2d.posInterval(1, Point3(2.7, 0, 0)),\
                        Func(base.changeZone, newZone, extraArgs, False)).start()
                return
        if not base.win: base.openMainWindow()
        if not base.currentZoneModule == None: 
            if "remove" in dir(base.currentZoneModule):
                try: base.currentZoneModule.remove()
                except:
                    if not base.removeZoneExempt: raise
                    else: base.removeZoneExempt = False
        try: base.currentRender.removeNode(); del base.currentRender
        except AttributeError: pass
        try: base.currentRender2d.removeNode(); del base.currentRender2d
        except AttributeError: pass
        try: base.currentAspect2d.removeNode(); del base.currentAspect2d
        except AttributeError: pass
        try: base.currentPixel2d.removeNode(); del base.currentPixel2d
        except AttributeError: pass
        base.removeExists("currentNodes")
        base.setDefaultBackgroundColor()
        base.currentRender = render.attachNewNode("currentRender")
        base.currentRender2d = render2d.attachNewNode("currentRender2D")
        base.currentAspect2d = aspect2d.attachNewNode("currentAspect2D")
        base.currentPixel2d = pixel2d.attachNewNode("currentPixel2D")
        base.addExists("currentNodes")
        base.lastZoneModule = base.currentZoneModule
        base.currentZoneModule = newZone
        if base.exists("changeZone_runSequence"):
            base.currentAspect2d.setPos(0, 0, -2.2)
        if not extraArgs == None: newZone.show(extraArgs)
        else: newZone.show()
        if base.exists("changeZone_runSequence", True):
            Sequence(base.currentAspect2d.posInterval(1, Point3(0, 0, 0))).start()
        
    def rgb(base, r, g = None, b = None, a = 1):
        if isinstance(r, tuple):
            rgba = r
            try: a = rgba[3]
            except IndexError: a = 1
            return float(rgba[0])/float(255), float(rgba[1])/float(255), float(rgba[2])/float(255), a
        else: return float(r)/float(255), float(g)/float(255), float(b)/float(255), a
       
    def addExists(base, name):
        if not name in base.existsList:
            base.existsList.append(name)

    def removeExists(base, name):
        if name in base.existsList:
            base.existsList.remove(name)

    def exists(base, name, remove = False):
        if name in base.existsList:
            if remove == True:
                base.removeExists(name)
            return True
        else: return False

    def setDefaultBackgroundColor(base): base.setBackgroundColor(base.rgb(base.MainGlobals.DEFAULTBACKGROUNDCOLOR))
    def execCommand(base, command): exec(command)
    def loadModel(base, model): return loader.loadModel(base.panda3DFormat(model))
    def loadFont(base, font): return loader.loadFont(base.panda3DFormat(font))
    def panda3DFormat(base, path): return str(Filename.fromOsSpecific(os.path.join(os.getcwd(), path)))

try: Main = Main()
except:
    if MainGlobals.TRACEBACKMSG:
        tkMessageBox.showerror(MainGlobals.WINDOWTITLE, "Fatal Error:\n" + traceback.format_exc())
    raise
else:
    try: Main.run()
    except:
        if MainGlobals.TRACEBACKMSG:
            tkMessageBox.showerror(MainGlobals.WINDOWTITLE, "Fatal Error:\n" + traceback.format_exc())
        raise