import os

def newDirectory(dirPath, skipException = False):
    if not dirPath == "":
        if not os.path.isdir(dirPath):
            os.makedirs(dirPath)
        elif not skipException:
            raise AssertionError("The directory \"%s\" already exists" % dirPath)

def newFile(filePath, skipException = False):
    if not os.path.isfile(filePath):
        dirPath = os.path.dirname(filePath)
        if not os.path.isdir(dirPath):
            newDirectory(dirPath)
        mode = "w"
        if os.path.splitext(filePath)[1] == ".exe": mode = "wb"
        fileObject = open(filePath, mode)
        fileObject.close()
    elif not skipException:
        raise AssertionError("The file \"%s\" already exists" % filePath)
    
def read(filePath, autoAdd = False):
    if os.path.isfile(filePath):
        mode = "r"
        if os.path.splitext(filePath)[1] == ".exe": mode = "rb"
        fileObject = open(filePath, mode)
        fileContents = fileObject.read()
        fileObject.close()
        return fileContents
    elif not autoAdd:
        raise AssertionError("The file \"%s\" does not exists" % filePath)
    else:
        newFile(filePath)
        return ""

def write(filePath, data, autoAdd = True):
    if not os.path.isfile(filePath):
        if not autoAdd:
            raise AssertionError("The file \"%s\" does not exists" % filePath)
        else: newFile(filePath)
    mode = "w"
    if os.path.splitext(filePath)[1] == ".exe": mode = "wb"
    fileObject = open(filePath, mode)
    fileObject.write(data)
    fileObject.close()

def append(filePath, data, autoAdd = True):
    if not os.path.isfile(filePath):
        if not autoAdd:
            raise AssertionError("The file \"%s\" does not exists" % filePath)
        else: newFile(filePath)
    fileObject = open(filePath, "a")
    fileObject.write(data)
    fileObject.close()
