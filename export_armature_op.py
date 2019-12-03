import bpy
import os
import mathutils

from . util import *

class UE4_OT_ExportArmature(bpy.types.Operator):

    bl_idname = "ue4tools.export_armature"
    bl_description = "Export Armature to UE4"
    bl_label = "Export Armature to UE4"

    @classmethod
    def poll(cls, context):
        #print (context.active_object.type)
        return context.active_object and context.active_object.type == "ARMATURE"

    def execute(self, context):

        preferences = bpy.context.preferences
        addon_prefs = preferences.addons['UE4Tools'].preferences
        #print(addon_prefs)

        #tempScene = bpy.context.scene.copy()
        #tempScene.name = "ue4-export-temp"

        #bpy.context.window.scene = tempScene

        scene = bpy.context.scene

        activeObj = bpy.context.active_object
        #print("Original active object = %s" % activeObj.name)
        filename_prefix = addon_prefs.skeletal_prefix_export_name
        filename = filename_prefix + activeObj.name + ".fbx"

        dirpath = addon_prefs.export_skeletal_file_path
        absdirpath = bpy.path.abspath(dirpath)
        absdirpath = os.path.join( absdirpath , activeObj.name)
        if not os.path.exists(absdirpath):
            os.makedirs(absdirpath)
        fullpath = os.path.join( absdirpath ,  filename )

        bpy.ops.object.select_hierarchy(direction='CHILD', extend=True)
        #for obj in bpy.context.selected_objects:
        #    print(obj.name)
        #activeObj = bpy.context.active_object
        #print(activeObj.name)
        #bpy.context.scene.objects.active = activeObj
        bpy.context.view_layer.objects.active = activeObj
        #activeObj = bpy.context.active_object
        #print(activeObj.name)

        bpy.ops.object.duplicate()
        #print("Duplicating ----")

        armatureObj = bpy.context.active_object
        armatureObj.name = addon_prefs.skeletonRootBoneName
        #print("New active name = %s" % armatureObj.name)
    
        #for obj in bpy.context.selected_objects:
        #    print(obj.name)

        ApplyNeededModifierToSelect()
        RemoveMaterialsFromSelectedObjects()

        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True )
        bpy.ops.transform.resize(value=(100,100,100))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True )
        bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=False) 
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True )
        bpy.ops.object.select_hierarchy(direction='PARENT', extend=False) 
        
        bpy.context.view_layer.objects.active = armatureObj
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=True) 

        newMatrix = armatureObj.matrix_world @ mathutils.Matrix.Translation((0,0,0))
        saveScale = armatureObj.scale * 1
        mat_trans = mathutils.Matrix.Translation((0,0,0))
        mat_rot = newMatrix.to_quaternion().to_matrix()
        newMatrix = mat_trans @ mat_rot.to_4x4()
        
        armatureObj.matrix_world = newMatrix
        armatureObj.scale = saveScale

        #print(fullpath)

        actionList = []
        armatureBones = {bone.name for bone in armatureObj.data.bones}
        for action in bpy.data.actions:
            actionBones = {group.name for group in action.groups}
            if not armatureBones.isdisjoint(actionBones):
                actionList.append(action)

        #print(actionList)

        savedAction = armatureObj.animation_data.action #Save current action
        savedAction_extrapolation = armatureObj.animation_data.action_extrapolation
        savedAction_blend_type = armatureObj.animation_data.action_blend_type
        savedAction_influence = armatureObj.animation_data.action_influence

        if armatureObj.animation_data is None:
            armatureObj.animation_data_create()

        if (bpy.context.scene.is_nla_tweakmode == True):
            armatureObj.animation_data.use_tweak_mode = False

        for action in actionList:
            if action.frame_range.y - action.frame_range.x == 1:
                actionType = "Pose"
                action_prefix = addon_prefs.pose_prefix_export_name
            else:
                actionType = "Action"
                action_prefix = addon_prefs.anim_prefix_export_name


            filename_prefix = action_prefix
            action_filename = filename_prefix + activeObj.name+"_"+action.name + ".fbx"
            action_path = os.path.join( absdirpath ,  action_filename )

            #print(action_path)

            #bpy.ops.pose.transforms_clear()

            armatureObj.animation_data.action = action #Apply desired action and reset NLA
            armatureObj.animation_data.action_extrapolation = 'HOLD'
            armatureObj.animation_data.action_blend_type = 'REPLACE'
            armatureObj.animation_data.action_influence = 1

            if armatureObj.AnimStartEndTimeEnum == "with_keyframes":
                startTime = action.frame_range.x #GetFirstActionFrame
                endTime = action.frame_range.y #GetLastActionFrame
            elif armatureObj.AnimStartEndTimeEnum == "with_sceneframes":
                startTime = scene.frame_start
                endTime = scene.frame_end
            elif armatureObj.AnimStartEndTimeEnum == "with_customframes":
                startTime = armatureObj.AnimCustomStartTime
                endTime = armatureObj.AnimCustomEndTime

            startTime += armatureObj.StartFramesOffset
            endTime += armatureObj.EndFramesOffset

            scene.frame_start = startTime
            scene.frame_end = endTime

            bpy.ops.export_scene.fbx(
                filepath=action_path,
                check_existing=False,
                use_selection=True,
                #global_scale=GetObjExportScale(obj),
                object_types={'ARMATURE'},
                use_custom_props=False,
                add_leaf_bones=False,
                use_armature_deform_only=True,
                bake_anim=True,
                bake_anim_use_nla_strips=False,
                bake_anim_use_all_actions=False,
                bake_anim_force_startend_keying=True,
                #bake_anim_step=GetAnimSample(obj),
                #bake_anim_simplify_factor=obj.SimplifyAnimForExport,
                use_metadata=False,
                primary_bone_axis = 'X',
                secondary_bone_axis = '-Y',	    
                axis_forward = 'X',
                axis_up = 'Z',
                bake_space_transform = False
            )

            #bpy.ops.pose.transforms_clear()
        armatureObj.animation_data.action = savedAction #Resets previous action and NLA
        armatureObj.animation_data.action_extrapolation = savedAction_extrapolation
        armatureObj.animation_data.action_blend_type = savedAction_blend_type
        armatureObj.animation_data.action_influence = savedAction_influence
                
        bpy.ops.export_scene.fbx(
            filepath=fullpath,
            check_existing=False,
            use_selection=True,
            #global_scale=GetObjExportScale(active),
            object_types={'ARMATURE', 'MESH'},
            use_custom_props=False,
            mesh_smooth_type="FACE",
            add_leaf_bones=False,
            use_armature_deform_only=True,
            bake_anim=False,
            use_metadata=False,
            primary_bone_axis = 'X',
            secondary_bone_axis = '-Y',	
            axis_forward = 'X',
            axis_up = 'Z',
            bake_space_transform = False
        )


        bpy.ops.object.delete()
        
        #print("New active name = %s" % activeObj.name)
        bpy.context.view_layer.objects.active = activeObj
        activeObj.select_set(True)
        #bpy.context.window.scene = savedScene
        #bpy.data.scenes.remove(tempScene)
        
        return {'FINISHED'}
