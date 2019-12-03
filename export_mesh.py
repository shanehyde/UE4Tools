import bpy

from . util import RemoveMaterialsFromSelectedObjects, ValidFilenameForUnreal

def ExportSingleFbxMesh():
    scene = bpy.context.scene
    preferences = bpy.context.preferences
    addon_prefs = preferences.addons['UE4'].preferences

    if	bpy.ops.object.mode_set.poll():
		bpy.ops.object.mode_set(mode = 'OBJECT')

    bpy.ops.object.duplicate()
    
    # Collect all the objects
    currentObjName = []
	for objScene in bpy.context.scene.objects:
		currentObjName.append(objScene.name)

    # actually duplicate
    bpy.ops.object.duplicates_make_real(use_base_parent=True, use_hierarchy=True)

    # find the new objects
    for objScene in bpy.context.scene.objects:
		if objScene.name not in currentObjName:
			objScene.select_set(True)
			pass

    RemoveMaterialsFromSelectedObjects()

    absdirpath = bpy.path.abspath(dirpath)
    fullpath = os.path.join( absdirpath , filename )

    if(active.type == "MESH"):
        object_types = {'MESH'}

    if(active.type == "ARMATURE):
        object_types = {'MESH', 'ARMATURE'}

    bpy.ops.export_scene.fbx(
		filepath=fullpath,
		check_existing=False,
		use_selection=True,
		global_scale=GetObjExportScale(active),
		object_types=object_types,
		use_custom_props=addon_prefs.exportWithCustomProps,
		mesh_smooth_type="FACE",
		add_leaf_bones=False,
		use_armature_deform_only=active.exportDeformOnly,
		bake_anim=False,
		use_metadata=addon_prefs.exportWithMetaData,
		primary_bone_axis = active.exportPrimaryBaneAxis,
		secondary_bone_axis = active.exporSecondaryBoneAxis,	
		axis_forward = active.exportAxisForward,
		axis_up = active.exportAxisUp,
		bake_space_transform = False
		)

    # delete the duped object
    bpy.ops.object.delete()