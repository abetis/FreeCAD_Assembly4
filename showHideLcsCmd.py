#!/usr/bin/env python3
# coding: utf-8
#
# showHideLcsCmd.py

import math, re, os

import FreeCADGui as Gui
import FreeCAD as App

import libAsm4 as Asm4

import time

"""
    +-----------------------------------------------+
    |                  main class                   |
    +-----------------------------------------------+
"""
class showLcsCmd:
    def __init__(self):
        super(showLcsCmd,self).__init__()

    def GetResources(self):
        return {"MenuText": "Show LCS",
                "ToolTip": "Show LCS of selected part and its children",
#                "Pixmap" : os.path.join( Asm4.iconPath , 'Asm4_CoordinateSystem.svg')
                }

    def IsActive(self):
        # Will handle LCSs only for the Assembly4 model
        if Asm4.getSelection() or Asm4.getModelSelected():
            return True
        return False

    """
    +-----------------------------------------------+
    |                 the real stuff                |
    +-----------------------------------------------+
    """
    def Activated(self):
        global sos, so, doc
        sos = 0
        so = 0
        start = time.time()
        model = Asm4.getModelSelected()
        if model:
            sos = sos+1
            for objName in model.getSubObjects():
                so = so+1
                ShowChildLCSs(model.getSubObject(objName, 1), True)
        else:
            ShowChildLCSs(Asm4.getSelection(), True)
        
        end = time.time()
        print("Activated sos = " + str(sos))
        print("Activated so = " + str(so))
        print("Time (sec): " + str(end-start))
        
        doc = 0
        start = time.time()
        model = Asm4.getModelSelected()
        if model:
            doc = doc+1
            for obj in model.getSubObjectsDoc():
                ShowChildLCSsFast(obj, True)
        else:
            ShowChildLCSsFast(Asm4.getSelection(), True)

        end = time.time()
        print("Fast doc = " + str(doc))
        print("Time (sec): " + str(end-start))


class hideLcsCmd:
    def __init__(self):
        super(hideLcsCmd,self).__init__()

    def GetResources(self):
        return {"MenuText": "Hide LCS",
                "ToolTip": "Hide LCS of selected part and its children",
#                "Pixmap" : os.path.join( Asm4.iconPath , 'Asm4_CoordinateSystem.svg')
                }

    def IsActive(self):
        # Will handle LCSs only for the Assembly4 model
        if Asm4.getSelection() or Asm4.getModelSelected():
            return True
        return False

    """
    +-----------------------------------------------+
    |                 the real stuff                |
    +-----------------------------------------------+
    """
    def Activated(self):
        model = Asm4.getModelSelected()
        if model:
            for objName in model.getSubObjects():
                ShowChildLCSs(model.getSubObject(objName, 1), False)
        else:
            ShowChildLCSs(Asm4.getSelection(), False)


sos = 0
so = 0
doc = 0

# Show/Hide the LCSs in the provided object and all linked children
def ShowChildLCSs(obj, show):
    global sos, so
    lcsTypes = ["PartDesign::CoordinateSystem", "PartDesign::Line", "PartDesign::Point", "PartDesign::Plane"]

    if obj.TypeId == 'App::Link':
        for linkObj in obj.LinkedObject.Document.Objects:
            ShowChildLCSs(linkObj, show)
    else:
        sos = sos+1
        for subObjName in obj.getSubObjects():
            so = so+1
            subObj = obj.getSubObject(subObjName, 1)    # 1 for returning the real object
            if subObj != None:
                if subObj.TypeId in lcsTypes:
                    subObj.Visibility = show

def ShowChildLCSsFast(obj, show):
    global doc
    lcsTypes = ["PartDesign::CoordinateSystem", "PartDesign::Line", "PartDesign::Point", "PartDesign::Plane"]

    if obj.TypeId == 'App::Link':
        for linkObj in obj.LinkedObject.Document.Objects:
            ShowChildLCSsFast(linkObj, show)
    else:
        doc = doc+1
        for subObj in obj.getSubObjectsDoc(0, 1):
            if subObj != None:
                if subObj.TypeId in lcsTypes:
                    subObj.Visibility = show

"""
    +-----------------------------------------------+
    |       add the command to the workbench        |
    +-----------------------------------------------+
"""
Gui.addCommand( 'Asm4_showLcs', showLcsCmd() )
Gui.addCommand( 'Asm4_hideLcs', hideLcsCmd() )

