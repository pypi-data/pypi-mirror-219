# !/usr/bin/python
# coding=utf-8
try:
    import pymel.core as pm
except ImportError as error:
    print(__file__, error)
import mayatk as mtk
from tentacle.slots.maya import SlotsMaya


class Duplicate_maya(SlotsMaya):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def tb000_init(self, widget):
        """ """
        widget.menu.add(
            "QCheckBox",
            setText="Match Vertex Orientaion",
            setObjectName="chk001",
            setChecked=False,
            setToolTip="Attempt to match 3 points of the source to the same 3 points of the target.",
        )

    def chk010(self, state, widget):
        """Radial Array: Set Pivot"""

        global radialPivot
        radialPivot = []
        # add support for averaging multiple components.
        if state:
            selection = pm.ls(sl=True, flatten=1)
            if selection:
                vertices = pm.filterExpand(selectionMask=31)  # get selected vertices
                if (
                    vertices is not None and vertices == 1
                ):  # if a single vertex is selected, query that vertex position.
                    pivot = pm.xform(selection, q=True, translation=1, worldSpace=1)
                else:  # else, get the center of the objects bounding box.
                    bb = pm.xform(selection, q=True, boundingBox=1, worldSpace=1)
                    pivot = (
                        bb[0] + bb[3] / 2,
                        bb[1] + bb[4] / 2,
                        bb[2] + bb[5] / 2,
                    )  # get median of bounding box coordinates. from [min xyz, max xyz]
            else:
                self.sb.toggle_widgets(widget.ui, setUnChecked="chk010")
                self.sb.message_box("Nothing selected.")
                return

            # radialPivot.extend ([pivot[0],pivot[1],pivot[2]])
            radialPivot.extend(pivot)  # extend the list contents
            text = (
                str(int(pivot[0])) + "," + str(int(pivot[1])) + "," + str(int(pivot[2]))
            )
            self.sb.duplicate_radial.chk010.setText(text)
        else:
            del radialPivot[:]
            self.sb.duplicate_radial.chk010.setText("Set Pivot")

    global radialArrayObjList
    radialArrayObjList = []

    @mtk.undo
    def chk015(self, widget):
        """Radial Array: Preview"""
        setPivot = self.sb.duplicate_radial.chk010.isChecked()  # set pivot point
        instance = self.sb.duplicate_radial.chk011.isChecked()  # instance object

        if self.sb.duplicate_radial.chk015.isChecked():
            self.sb.toggle_widgets(widget.ui, setEnabled="b003")

            selection = pm.ls(sl=True, type="transform", flatten=1)
            if selection:
                if radialArrayObjList:
                    try:
                        pm.delete(
                            radialArrayObjList
                        )  # delete all the geometry in the list
                    except Exception:
                        pass
                    del radialArrayObjList[:]  # clear the list

                for obj in selection:
                    pm.select(obj)
                    objectName = str(obj)

                    numDuplicates = int(self.sb.duplicate_radial.s000.value())
                    angle = float(self.sb.duplicate_radial.s001.value())

                    x = y = z = 0
                    if self.sb.duplicate_radial.chk012.isChecked():
                        x = angle
                    if self.sb.duplicate_radial.chk013.isChecked():
                        y = angle
                    if self.sb.duplicate_radial.chk014.isChecked():
                        z = angle

                    # pm.undoInfo (openChunk=1)
                    for i in range(1, numDuplicates):
                        if instance:
                            name = objectName + "_ins" + str(i)
                            pm.instance(name=name)
                        else:
                            name = objectName + "_dup" + str(i)
                            pm.duplicate(returnRootsOnly=1, name=name)
                        if setPivot:
                            if len(radialPivot):
                                pm.rotate(
                                    x, y, z, relative=1, pivot=radialPivot
                                )  # euler=1
                            else:
                                self.sb.message_box("No pivot point set.")
                        else:
                            pm.rotate(x, y, z, relative=1)  # euler=1
                        radialArrayObjList.append(name)
                    # if in isolate select mode; add object
                    currentPanel = pm.paneLayout(
                        "viewPanes", q=True, pane1=True
                    )  # get the current modelPanel view
                    if pm.isolateSelect(currentPanel, q=True, state=1):
                        for obj_ in radialArrayObjList:
                            pm.isolateSelect(currentPanel, addDagObject=obj_)
                    # re-select the original selected object
                    pm.select(objectName)
                    # pm.undoInfo (closeChunk=1)
            else:  # if both lists objects are empty:
                self.sb.toggle_widgets(
                    widget.ui, setDisabled="b003", setUnChecked="chk015"
                )
                self.sb.message_box("Nothing selected.")
                return
        else:  # if chk015 is unchecked by user or by create button
            if create:
                originalObj = radialArrayObjList[0][
                    : radialArrayObjList[0].rfind("_")
                ]  # remove the trailing _ins# or _dup#. ie. pCube1 from pCube1_inst1
                radialArrayObjList.append(originalObj)
                pm.polyUnite(
                    radialArrayObjList, name=originalObj + "_array"
                )  # combine objects. using the original name results in a duplicate object error on deletion
                print("Result: " + str(radialArrayObjList))
                pm.delete(radialArrayObjList)
                del radialArrayObjList[:]  # delete all geometry and clear the list
                return
            try:
                pm.delete(radialArrayObjList)  # delete all the geometry in the list
            except Exception:
                pass
            del radialArrayObjList[:]  # clear the list

            self.sb.toggle_widgets(widget.ui, setDisabled="b003")

    global duplicateObjList
    duplicateObjList = []

    @mtk.undo
    def chk016(self, create=False):
        """Duplicate: Preview"""
        if self.sb.duplicate_linear.chk016.isChecked():
            self.sb.toggle_widgets(widget.ui, setEnabled="b002")

            instance = self.sb.duplicate_linear.chk000.isChecked()
            numOfDuplicates = int(self.sb.duplicate_linear.s005.value())
            keepFacesTogether = self.sb.duplicate_linear.chk009.isChecked()
            transXYZ = [
                float(self.sb.duplicate_linear.s002.value()),
                float(self.sb.duplicate_linear.s003.value()),
                float(self.sb.duplicate_linear.s004.value()),
            ]
            rotXYZ = [
                float(self.sb.duplicate_linear.s007.value()),
                float(self.sb.duplicate_linear.s008.value()),
                float(self.sb.duplicate_linear.s009.value()),
            ]
            scaleXYZ = [
                float(self.sb.duplicate_linear.s010.value()),
                float(self.sb.duplicate_linear.s011.value()),
                float(self.sb.duplicate_linear.s012.value()),
            ]
            translateToComponent = self.sb.duplicate_linear.chk007.isChecked()
            alignToNormal = self.sb.duplicate_linear.chk008.isChecked()
            componentList = [
                self.sb.duplicate_linear.cmb001.itemText(i)
                for i in range(self.sb.duplicate_linear.cmb001.count())
            ]

            try:
                pm.delete(
                    duplicateObjList[1:]
                )  # delete all the geometry in the list, except the original obj
            except Exception as error:
                print(error)

            del duplicateObjList[1:]  # clear the list, leaving the original obj
            selection = pm.ls(
                sl=True, flatten=1, objectsOnly=1
            )  # there will only be a selection when first called. After, the last selected item will have been deleted with the other duplicated objects, leaving only the original un-selected.

            if selection:
                obj = selection[0]
                duplicateObjList.insert(0, obj)  # insert at first index
            elif duplicateObjList:
                obj = duplicateObjList[0]
                pm.select(obj)
            else:
                self.sb.message_box("Nothing selected.")

                return

            # pm.undoInfo (openChunk=1)
            if translateToComponent:
                if componentList:
                    for num, component in componentList.iteritems():
                        vertexPoint = mtk.get_center_point(component)

                        pm.xform(obj, rotation=[rotXYZ[0], rotXYZ[1], rotXYZ[2]])
                        pm.xform(
                            obj,
                            translation=[
                                vertexPoint[0] + transXYZ[0],
                                vertexPoint[1] + transXYZ[1],
                                vertexPoint[2] + transXYZ[2],
                            ],
                        )
                        pm.xform(obj, scale=[scaleXYZ[0], scaleXYZ[1], scaleXYZ[2]])

                        if (
                            component != componentList[len(componentList) - 1]
                        ):  # if not at the end of the list, create a new instance of the obj.
                            name = str(obj) + "_INST" + str(num)
                            duplicatedObject = pm.instance(obj, name=name)
                        # print("component:",component,"\n", "normal:",normal,"\n", "vertexPoint:",vertexPoint,"\n")

                        duplicateObjList.append(
                            duplicatedObject
                        )  # append duplicated object to list
                else:
                    self.sb.message_box("Component list empty.")
                    self.sb.toggle_widgets(
                        widget.ui, setDisabled="b002", setChecked="chk016"
                    )
                    return
            else:
                for _ in range(numOfDuplicates):
                    if ".f" in str(obj):  # face
                        duplicatedObject = pm.duplicate(name="pExtract1")[0]

                        selectedFaces = [
                            duplicatedObject + "." + face.split(".")[1] for face in obj
                        ]  # create a list of the original selected faces numbers but with duplicated objects name

                        numFaces = pm.polyEvaluate(duplicatedObject, face=1)
                        allFaces = [
                            duplicatedObject + ".f[" + str(num) + "]"
                            for num in range(numFaces)
                        ]  # create a list of all faces on the duplicated object

                        pm.delete(
                            set(allFaces) - set(selectedFaces)
                        )  # delete faces in 'allFaces' that were not in the original obj

                    elif ".e" in str(obj):  # edge
                        duplicatedObject = pm.polyToCurve(
                            form=2, degree=3, conformToSmoothMeshPreview=1
                        )

                    elif instance:
                        duplicatedObject = pm.instance()

                    else:
                        duplicatedObject = pm.duplicate()

                    pm.xform(duplicatedObject, rotation=rotXYZ, relative=1)
                    pm.xform(duplicatedObject, translation=transXYZ, relative=1)
                    pm.xform(duplicatedObject, scale=scaleXYZ, relative=1)

                    duplicateObjList.append(
                        duplicatedObject
                    )  # append duplicated object to list
                    pm.select(duplicatedObject)
            # pm.undoInfo (closeChunk=1)

        else:  # if chk016 is unchecked by user or by create button
            if create:
                # originalObj = duplicateObjList[0][:duplicateObjList[0].rfind("_")] #remove the trailing _ins# or _dup#. ie. pCube1 from pCube1_INST1
                # duplicateObjList.append(originalObj)
                # pm.polyUnite (duplicateObjList, name=originalObj+"_array") #combine objects. using the original name results in a duplicate object error on deletion
                print("Result: " + str(duplicateObjList))
                # pm.delete(duplicateObjList) #delete all duplicated geometry
                del duplicateObjList[:]  # clear the list
                return
            pm.delete(
                duplicateObjList[1:]
            )  # delete all the geometry in the list, except the original obj
            pm.select(duplicateObjList[:1])  # re-select the original object
            del duplicateObjList[:]  # clear the list
            self.sb.toggle_widgets(widget.ui, setDisabled="b002")

    def tb000(self, widget):
        """Convert to Instances"""
        transformByVertexOrder = widget.menu.chk001.isChecked()

        selection = pm.ls(sl=1, transforms=1)
        if not selection:
            self.sb.message_box(
                "<strong>Nothing selected</strong>.<br>Operation requires an object selection."
            )
            return

        if not pm.selectPref(
            q=1, trackSelectionOrder=1
        ):  # if ordered selection is not on, turn it on. If off, the current selection is likely not ordered.
            pm.selectPref(trackSelectionOrder=1)
        self.convertToInstances(
            selection, transformByVertexOrder=transformByVertexOrder
        )

    def chk007(self, state, widget):
        """Duplicate: Translate To Components"""
        if state:
            self.sb.toggle_widgets(
                widget.ui,
                setEnabled="chk008,b034,cmb001",
                setDisabled="chk000,chk009,s005",
            )
            self.b008()
        else:
            self.sb.toggle_widgets(
                widget.ui,
                setDisabled="chk008,b034,cmb001",
                setEnabled="chk000,chk009,s005",
            )

    def chk011(self, state, widget):
        """Radial Array: Instance/Duplicate Toggle"""
        self.chk015()  # calling chk015 directly from valueChanged would pass the returned spinbox value to the create arg

    def chk012(self, state, widget):
        """Radial Array: X Axis"""
        self.sb.toggle_widgets(
            widget.ui, setChecked="chk012", setUnChecked="chk013,chk014"
        )
        self.chk015()

    def chk013(self, state, widget):
        """Radial Array: Y Axis"""
        self.sb.toggle_widgets(
            widget.ui, setChecked="chk013", setUnChecked="chk012,chk014"
        )
        self.chk015()

    def chk014(self, state, widget):
        """Radial Array: Z Axis"""
        self.sb.toggle_widgets(
            widget.ui, setChecked="chk014", setUnChecked="chk012,chk013"
        )
        self.chk015()

    def b000(self):
        """Create Instances"""
        selection = pm.ls(sl=1, transforms=1)
        if not selection:
            self.sb.message_box(
                "<strong>Nothing selected</strong>.<br>Operation requires an object selection."
            )
            return

        instances = [pm.instance(obj, name=obj.name() + "_INST") for obj in selection]

        pm.select(instances)

    def b002(self):
        """Duplicate: Create"""
        self.sb.duplicate_linear.chk016.setChecked(
            False
        )  # must be in the false unchecked state to catch the create flag in chk015
        self.chk016(create=True)

    def b003(self):
        """Radial Array: Create"""
        self.sb.duplicate_radial.chk015.setChecked(
            False
        )  # must be in the false unchecked state to catch the create flag in chk015
        self.chk015(create=True)

    def b004(self):
        """Select Instanced Objects"""
        selection = pm.ls(sl=1)

        if not selection:  # select all instanced objects in the scene.
            instances = self.getInstances()
            pm.select(instances)
        else:  # select instances of the selected objects.
            instances = self.getInstances(selection)
            pm.select(instances)

    def b005(self):
        """Uninstance Selected Objects"""
        selection = pm.ls(sl=1)

        self.unInstance(selection)

    def b006(self):
        """ """
        self.sb.parent().set_ui("duplicate_linear")
        self.sb.duplicate_linear.s002.valueChanged.connect(
            self.duplicateArray
        )  # update duplicate array
        self.sb.duplicate_linear.s003.valueChanged.connect(self.duplicateArray)
        self.sb.duplicate_linear.s004.valueChanged.connect(self.duplicateArray)
        self.sb.duplicate_linear.s005.valueChanged.connect(self.duplicateArray)
        self.sb.duplicate_linear.s007.valueChanged.connect(self.duplicateArray)
        self.sb.duplicate_linear.s008.valueChanged.connect(self.duplicateArray)
        self.sb.duplicate_linear.s009.valueChanged.connect(self.duplicateArray)
        self.sb.duplicate_linear.s010.valueChanged.connect(self.duplicateArray)
        self.sb.duplicate_linear.s011.valueChanged.connect(self.duplicateArray)
        self.sb.duplicate_linear.s012.valueChanged.connect(self.duplicateArray)

    def b007(self):
        """ """
        self.sb.parent().set_ui("duplicate_radial")
        self.sb.duplicate_radial.s000.valueChanged.connect(
            self.radialArray
        )  # update radial array
        self.sb.duplicate_radial.s001.valueChanged.connect(self.radialArray)

    def b008(self):
        """Add Selected Components To cmb001"""
        cmb = self.sb.duplicate_linear.cmb001

        selection = pm.ls(sl=True, flatten=True)
        cmb.add([str(i) for i in selection])

    def getInstances(self, objects=None, returnParentObjects=False):
        """get any intances of given object, or if None given; get all instanced objects in the scene.

        Parameters:
                objects (str/obj/list): Parent object/s.
                returnParentObjects (bool): Return instances and the given parent objects together.

        Returns:
                (list)
        """
        instances = []

        if objects is None:  # get all instanced objects in the scene.
            import maya.OpenMaya as om

            iterDag = om.MItDag(om.MItDag.kBreadthFirst)
            while not iterDag.isDone():
                instanced = om.MItDag.isInstanced(iterDag)
                if instanced:
                    instances.append(iterDag.fullPathName())
                iterDag.next()
        else:
            shapes = pm.listRelatives(objects, s=1)
            instances = pm.listRelatives(shapes, ap=1)
            if not returnParentObjects:
                [instances.remove(obj) for obj in objects]

        return instances

    @mtk.undo
    def convertToInstances(self, objects=[], transformByVertexOrder=False, append=""):
        """The first selected object will be instanced across all other selected objects.

        Parameters:
                objects (list): A list of objects to convert to instances. The first object will be the instance parent.
                append (str): Append a string to the end of any instanced objects. ie. '_INST'
                transformByVertexOrder (bool): Transform the instanced object by matching the transforms of the vertices between the two objects.

        Returns:
                (list) The instanced objects.

        Example: convertToInstances(pm.ls(sl=1))
        """
        # pm.undoInfo(openChunk=1)
        p0x, p0y, p0z = pm.xform(
            objects[0], q=True, rotatePivot=1, worldSpace=1
        )  # get the world space obj pivot.
        pivot = pm.xform(
            objects[0], q=True, rotatePivot=1, objectSpace=1
        )  # get the obj pivot.

        for obj in objects[1:]:
            name = obj.name()
            objParent = pm.listRelatives(obj, parent=1)

            instance = pm.instance(objects[0])

            self.unInstance(obj)
            pm.makeIdentity(obj, apply=1, translate=1, rotate=0, scale=0)

            if transformByVertexOrder:
                mtk.matchTransformByVertexOrder(instance, obj)
                if not mtk.is_overlapping(instance, obj):
                    print(
                        "# {}: Unable to match {} transforms. #".format(instance, obj)
                    )
            else:
                pm.matchTransform(
                    instance, obj, position=1, rotation=1, scale=1, pivots=1
                )  # move object to center of the last selected items bounding box # pm.xform(instance, translation=pos, worldSpace=1, relative=1) #move to the original objects location.

            try:
                pm.parent(
                    instance, objParent
                )  # parent the instance under the original objects parent.
            except RuntimeError:  # It is already a child of the parent.
                pass

            pm.delete(
                obj, constructionHistory=True
            )  # delete history for the object so that the namespace is cleared.
            pm.delete(obj)
            pm.rename(instance, name + append)
        pm.select(objects[1:])
        return objects[1:]
        # pm.undoInfo(closeChunk=1)

    def unInstance(self, objects):
        """Un-Instance the given objects.

        Parameters:
                objects (str/obj/list): The objects to un-instance. If 'all' is given all instanced objects in the scene will be uninstanced.
        """
        if objects == "all":
            objects = self.getInstances()

        for obj in pm.ls(objects):
            children = pm.listRelatives(obj, fullPath=1, children=1)
            parents = pm.listRelatives(children[0], fullPath=1, allParents=1)

            if len(parents) > 1:
                duplicatedObject = pm.duplicate(obj)
                pm.delete(obj)
                pm.rename(duplicatedObject[0], obj)


# module name
print(__name__)
# --------------------------------------------------------------------------------------------
# Notes
# --------------------------------------------------------------------------------------------
# b008, b009, b011


# deprecated:

# @mtk.undo
# def convertToInstances(self, objects=[], leaf=False, append=''):
#   '''The first selected object will be instanced across all other selected objects.

#   Parameters:
#       objects (list): A list of objects to convert to instances. The first object will be the instance parent.
#       leaf (bool): Instances leaf-level objects. Acts like duplicate except leaf-level objects are instanced.
#       append (str): Append a string to the end of any instanced objects. ie. '_INST'
#       transformByVertexOrder (bool): Transform the instanced object by matching the transforms of the vertices between the two objects.

#   Returns:
#       (list) The instanced objects.

#   Example: convertToInstances(pm.ls(sl=1))
#   '''
#   # pm.undoInfo(openChunk=1)
#   p0x, p0y, p0z = pm.xform(objects[0], q=True, rotatePivot=1, worldSpace=1) #get the world space obj pivot.
#   pivot = pm.xform(objects[0], q=True, rotatePivot=1, objectSpace=1) #get the obj pivot.

#   for obj in objects[1:]:

#       name = obj.name()
#       objParent = pm.listRelatives(obj, parent=1)

#       instance = pm.instance(objects[0], leaf=leaf)

#       # if transformByVertexOrder:
#       #   mtk.matchTransformByVertexOrder(instance, obj)
#       #   if not mtk.is_overlapping(instance, obj):
#       #       print ('# {}: Unable to match {} transforms. #'.format(instance, obj))
#       # else:
#       mtk.move_to(instance, obj) #source, target
#       pm.matchTransform(instance, obj, position=0, rotation=1, scale=0, pivots=0) #move object to center of the last selected items bounding box # pm.xform(instance, translation=pos, worldSpace=1, relative=1) #move to the original objects location.

#       try:
#           pm.parent(instance, objParent) #parent the instance under the original objects parent.
#       except RuntimeError as error: #It is already a child of the parent.
#           pass

#       pm.delete(obj, constructionHistory=True) #delete history for the object so that the namespace is cleared.
#       pm.delete(obj)
#       pm.rename(instance, name+append)
#   pm.select(objects[1:])
#   return objects[1:]
#   # pm.undoInfo(closeChunk=1)
