#!/usr/bin/env python3
# coding: utf-8
#
# explodeCmd.py
#
# Explode assembly

import os
from PySide import QtGui, QtCore
import FreeCADGui as Gui
import FreeCAD as App
from FreeCAD import Console as FCC

import libAsm4 as Asm4



observer = None

"""
    +-----------------------------------------------+
    |                  main class                   |
    +-----------------------------------------------+
"""
class explodeCmd(QtGui.QDialog):
    def __init__(self):
        super(explodeCmd,self).__init__()

    def GetResources(self):
        return {"MenuText": "Explode the assembly",
                "ToolTip": "Explode the assembly",
                "Pixmap" : os.path.join( Asm4.iconPath , 'Asm4_enableLinkSelection.svg')
                }

    def IsActive(self):
        # Will explode only for the Assembly4 model
        if Asm4.getSelection() or Asm4.getModelSelected():
            return True
        return False

    def Activated(self):
        Explode()
        return


"""
    +-----------------------------------------------+
    |                Functionality                  |
    +-----------------------------------------------+
"""

def Explode():
    # Freeze the computation of the current document objects
    App.ActiveDocument.RecomputesFrozen = True

    model = Asm4.getModelSelected()
    if model:
        explodeFromCenter = App.Vector(0,0,0)
    else:
        sel = Gui.Selection.getSelection()
        if len(sel) != 1:
            FCC.PrintMessage('One object should be selected')
            return
        explodeFromCenter = GetBoundBox(sel[0]).Center

    print('Explode from: ' + str(explodeFromCenter))

    model = App.ActiveDocument.getObject('Model')
    for objName in model.getSubObjects():
        ExplodeObject(model.getSubObject(objName, 1), explodeFromCenter)


def ExplodeObject(obj, explodeFrom):
    explodableObjects = ['App::Link', 'Part::FeaturePython']    # Fasters are 'Part::FeaturePython' type

    print('Exploding ' + obj.Name + ' = ' + obj.TypeId)

    if obj.TypeId in explodableObjects:
        box = GetBoundBox(obj)
        # Some objects don't have visible bodies, skip them
        if box is not None:
            objCenter = box.Center.add(obj.Placement.Base)
            print(obj.Name + ' was ' + str(objCenter) + ' Placement: ' + str(obj.Placement.Base))
            v = objCenter.sub(explodeFrom).multiply(0.2)
            print('Adding ' + str(v))
            obj.Placement.move(v)
            print('Now ' + str(GetBoundBox(obj).Center) + ' Placement: ' + str(obj.Placement.Base))

    # Explode sub-objects
    for objName in obj.getSubObjects():
        ExplodeObject(obj.getSubObject(objName, 1), explodeFrom)



# Shape property can be trusted only for a visible part's faces
# Get BoundBox of all visible objects. Central point can be extracted from it.
def GetBoundBox(obj):
    # Special handling for 'Part::FeaturePython' screws
    if obj.TypeId == 'Part::FeaturePython':
        return obj.Shape.BoundBox

    # For other types, search for a visible container types
    box = None
    for objName in obj.getSubObjects():
        subObj = obj.getSubObject(objName, 1)
        if (subObj.TypeId in Asm4.containerTypes or subObj.TypeId == 'Part::Feature') and subObj.Visibility == True:
            print("SubObj: " + subObj.Name + " = " + subObj.TypeId)
            if box is None:
                box = App.BoundBox(subObj.Shape.BoundBox)
            else:
                box = box.intersected()


    return box


"""
    +-----------------------------------------------+
    |       add the command to the workbench        |
    +-----------------------------------------------+
"""
Gui.addCommand( 'Asm4_explodeCmd', explodeCmd() )

