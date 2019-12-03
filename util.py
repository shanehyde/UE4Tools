import bpy
import fnmatch
import os


def GetAssetType(obj):

    if obj.type == "ARMATURE" and obj.ForceStaticMesh == False:
        return "SkeletalMesh"

    return "StaticMesh"

def ApplyNeededModifierToSelect():
    activeObj = bpy.context.view_layer.objects.active
    for obj in bpy.context.selected_objects:
        for mod in [m for m in obj.modifiers if m.type != 'ARMATURE']:
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_apply(modifier=mod.name)
            print("mod")    
    bpy.context.view_layer.objects.active = activeObj

def RemoveMaterialsFromSelectedObjects():
    # save actgive object
    activeObj = bpy.context.view_layer.objects.active 

    for matobj in bpy.context.selected_objects:
        if matobj.type == 'MESH' and True:
            bpy.context.view_layer.objects.active = matobj

            for i in reversed(range(len(matobj.material_slots))):
                if matobj.material_slots[i].name[0:4] != 'Mat_':
                    matobj.active_material_index = i
                    bpy.ops.object.material_slot_remove()
    bpy.context.view_layer.objects.active = activeObj

def ValidFilenameForUnreal(filename):
    # valid file name for unreal assets
    extension = os.path.splitext(filename)[1]
    newfilename = ValidFilename(os.path.splitext(filename)[0])
    return (''.join(c for c in newfilename if c != ".")+extension)


def GetChilds(obj):
    #Get all direct childs of a object

    ChildsObj = []
    for childObj in bpy.data.objects:
        pare = childObj.parent
        if pare is not None:
            if pare.name == obj.name:
                ChildsObj.append(childObj)

    return ChildsObj
    
def GetRecursiveChilds(obj):
    #Get all recursive childs of a object

    saveObjs = []

    def tryAppend(obj):
        if obj.name in bpy.context.scene.objects:
            saveObjs.append(obj)

    for newobj in GetChilds(obj):
        for childs in GetRecursiveChilds(newobj):
            tryAppend(childs)
        tryAppend(newobj)
    return saveObjs

def GetExportDesiredChilds(obj, d = False):
    #Get only all child objects that must be exported with parent object

    DesiredObj = []
    for child in GetRecursiveChilds(obj):
        if child.ExportEnum != "dont_export":
                DesiredObj.append(child)
            
    return DesiredObj


def SelectParentAndDesiredChilds(obj):
    #Selects only all child objects that must be exported with parent object
    selectedObjs = []
    bpy.ops.object.select_all(action='DESELECT')
    for selectObj in GetExportDesiredChilds(obj):
        if selectObj.name in bpy.context.view_layer.objects:
            if GetAssetType(obj) == "SkeletalMesh":
                #With skeletal mesh the socket must be not exported, ue4 read it like a bone
                if not fnmatch.fnmatchcase(selectObj.name, "SOCKET*"):
                    selectObj.select_set(True)
                    selectedObjs.append(selectObj)
            else:
                selectObj.select_set(True)
                selectedObjs.append(selectObj)
    obj.select_set(True)
    selectedObjs.append(obj)
    bpy.context.view_layer.objects.active = obj
    return selectedObjs

def ApplyNeededModifierToSelect():
	
	activeObj = bpy.context.view_layer.objects.active
	for obj in bpy.context.selected_objects:
		for mod in [m for m in obj.modifiers if m.type != 'ARMATURE']:
			bpy.context.view_layer.objects.active = obj
			print("mod = %s" % mod.name)
			bpy.ops.object.modifier_apply(modifier = mod.name)
			
	bpy.context.view_layer.objects.active = activeObj