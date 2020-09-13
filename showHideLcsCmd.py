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
        global processedLinks
        processedLinks = []

        global sos, so, vis
        sos = 0
        so = 0
        vis = 0
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
        print("Activated vis = " + str(vis))
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
        global processedLinks
        processedLinks = []

        model = Asm4.getModelSelected()
        if model:
            for objName in model.getSubObjects():
                ShowChildLCSs(model.getSubObject(objName, 1), False)
        else:
            ShowChildLCSs(Asm4.getSelection(), False)


sos = 0
so = 0
vis = 0

processedLinks = []

# Show/Hide the LCSs in the provided object and all linked children
def ShowChildLCSs(obj, show):
    global sos, so, vis
    global processedLinks

    if obj.TypeId == 'App::Link' and obj.Name not in processedLinks:
        processedLinks.append(obj.Name)
        for linkObj in obj.LinkedObject.Document.Objects:
            ShowChildLCSs(linkObj, show)
    else:
        if obj.TypeId in Asm4.containerTypes:
            sos = sos+1
            for subObjName in obj.getSubObjects():
                so = so+1
                subObj = obj.getSubObject(subObjName, 1)    # 1 for returning the real object
                if subObj != None:
                    if subObj.TypeId in Asm4.datumTypes:
                        vis = vis+1
                        subObj.Visibility = show


"""
    +-----------------------------------------------+
    |       add the command to the workbench        |
    +-----------------------------------------------+
"""
Gui.addCommand( 'Asm4_showLcs', showLcsCmd() )
Gui.addCommand( 'Asm4_hideLcs', hideLcsCmd() )

