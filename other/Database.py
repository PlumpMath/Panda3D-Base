import base64
import FileIO
import os

def newFile(filePath, skipException = False):
    if not os.path.exists(filePath):
        folder = os.path.dirname(filePath)
        if not os.path.isdir(folder):
            os.makedirs(folder)
        FileIO.newFile(filePath)
    elif not skipException:
        raise AssertionError("The file \"%s\" already exists" % filePath)
    
def readFile(filePath):
    if filePath.startswith("*TEXT*"): return filePath[6:]
    else:
        fileContents = FileIO.read(filePath)
        return fileContents

def tagExists(fileContents, tag):
    if "%s:" % tag in fileContents:
        return True
    else:
        return False
   
def cleanup(filePath):
    fileContents = readFile(filePath)
    fileContents = '\n'.join([i for i in fileContents.split('\n') if len(i) > 0])
    FileIO.write(filePath, fileContents)

def get(filePath, tag, skipException = False, b64 = True):
    fileContents = readFile(filePath)
    if tagExists(fileContents, tag):
        tagStartNumber = fileContents.find("%s:" % tag)
        postTag = fileContents[tagStartNumber:]
        tcOpenNumber = postTag.find("{")
        tcCloseNumber = postTag.find("}")
        tagContents = postTag[tcOpenNumber + 1:tcCloseNumber]
        if b64: tagContents = base64.b64decode(tagContents)
        return tagContents
    elif not skipException:
        raise AssertionError("The tag \"%s\" was not found in \"%s\"" % (tag, filePath))
    else:
        return ""

def add(filePath, tag, data, skipException = False):
    fileContents = readFile(filePath)
    if not tagExists(fileContents, tag):
        formatTag = "\n%s: {%s}" % (tag, base64.b64encode(data))
        fileContents += formatTag
        FileIO.write(filePath, fileContents)
        cleanup(filePath)
    elif not skipException:
        raise AssertionError("The tag \"%s\" is already present in \"%s\"" % (tag, filePath))

def remove(filePath, tag, skipException = False):
    fileContents = readFile(filePath)
    if tagExists(fileContents, tag):
        FileContentsTMP = fileContents
        for x in range(fileContents.count("%s:" % tag)):
            tagStartNumber = FileContentsTMP.find("%s:" % tag)
            postTag = FileContentsTMP[tagStartNumber:]
            tcCloseNumber = postTag.find("}") + 1
            wholeTag = postTag[:tcCloseNumber]
            FileContentsTMP = FileContentsTMP.replace(wholeTag, "")
        fileContents = FileContentsTMP
        del FileContentsTMP
        FileIO.write(filePath, fileContents)
        cleanup(filePath)
    elif not skipException:
        raise AssertionError("The tag \"%s\" is does not exists in \"%s\"" % (tag, filePath))

def edit(filePath, tag, data, autoAdd = True):
    fileContents = readFile(filePath)
    if tagExists(fileContents, tag):
        tagStartNumber = fileContents.find("%s:" % tag)
        preTag = fileContents[:tagStartNumber]
        postTag = fileContents[tagStartNumber:]
        oldContents = get(filePath, tag)
        postTag = postTag.replace(base64.b64encode(oldContents), base64.b64encode(data), True)
        newFileContents = preTag + postTag
        FileIO.write(filePath, newFileContents)
        cleanup(filePath)
    elif autoAdd:
        add(filePath, tag, data)
    else:
        raise AssertionError("The tag \"%s\" was not found in \"%s\"" % (tag, filePath))
