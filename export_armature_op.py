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

        scene = bpy.context.scene

        activeObj = bpy.context.active_object
        filename_prefix = addon_prefs.skeletal_prefix_export_name
        filename = filename_prefix + activeObj.name + ".fbx"

        dirpath = addon_prefs.export_skeletal_file_path
        absdirpath = bpy.path.abspath(dirpath)
        absdirpath = os.path.join( absdirpath , activeObj.name)
        if not os.path.exists(absdirpath):
            os.makedirs(absdirpath)
        fullpath = os.path.join( absdirpath ,  filename )

        # select all the children of the Armature
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=True)
        #make sure Armature is active object again
        bpy.context.view_layer.objects.active = activeObj

        #duplicate it all
        bpy.ops.object.duplicate()

        # Rename the newly created Armature so that UE4 will not add an extra root bone
        armatureObj = bpy.context.active_object
        armatureObj.name = addon_prefs.skeletonRootBoneName

        # Appply all modifiers except Armature to the mesh
        ApplyNeededModifierToSelect()

        #remove all materials from the the mesh except those starting with Mat_
        RemoveMaterialsFromSelectedObjects()

        # This trickery causes the armature to have a scale of 0.01 and the mesh to have a scale of 1.0
        # this means that when UE4 imports the mesh and mistakenly scales the skeleton by 100 then everything is 
        # right
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True )
        bpy.ops.transform.resize(value=(100,100,100))
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True )
        bpy.ops.transform.resize(value=(0.01, 0.01, 0.01))

        #after that the child mesh has a scale of 100, lets reset it to 1
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=False) 
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True )

        #select the armature again and make it active
        bpy.ops.object.select_hierarchy(direction='PARENT', extend=False) 
        bpy.context.view_layer.objects.active = armatureObj

        #reselct all the children
        bpy.ops.object.select_hierarchy(direction='CHILD', extend=True) 

        # move the object to 0,0,0 for export.  No need to worry about rotation just now
        newMatrix = armatureObj.matrix_world @ mathutils.Matrix.Translation((0,0,0))
        saveScale = armatureObj.scale * 1
        mat_trans = mathutils.Matrix.Translation((0,0,0))
        mat_rot = newMatrix.to_quaternion().to_matrix()
        newMatrix = mat_trans @ mat_rot.to_4x4()
        
        armatureObj.matrix_world = newMatrix
        armatureObj.scale = saveScale

        # lets find all actions that use a bone from this armature
        actionList = []
        armatureBones = {bone.name for bone in armatureObj.data.bones}
        for action in bpy.data.actions:
            actionBones = {group.name for group in action.groups}
            if not armatureBones.isdisjoint(actionBones):
                actionList.append(action)

        # backup some values to put back later
        savedAction = armatureObj.animation_data.action #Save current action
        savedAction_extrapolation = armatureObj.animation_data.action_extrapolation
        savedAction_blend_type = armatureObj.animation_data.action_blend_type
        savedAction_influence = armatureObj.animation_data.action_influence

        # make the data block we might need
        if armatureObj.animation_data is None:
            armatureObj.animation_data_create()

        # disable tweak mode
        if (bpy.context.scene.is_nla_tweakmode == True):
            armatureObj.animation_data.use_tweak_mode = False

        # ok do all the actions, if they have one frame, we will call it a Pose
        for action in actionList:
            if action.frame_range.y - action.frame_range.x == 1:
                actionType = "Pose"
                action_prefix = addon_prefs.pose_prefix_export_name
            else:
                actionType = "Action"
                action_prefix = addon_prefs.anim_prefix_export_name

            # construct the filename from the settings.
            filename_prefix = action_prefix
            action_filename = filename_prefix + activeObj.name+"_"+action.name + ".fbx"
            action_path = os.path.join( absdirpath ,  action_filename )

            # select the action into the action editor
            armatureObj.animation_data.action = action #Apply desired action and reset NLA
            armatureObj.animation_data.action_extrapolation = 'HOLD'
            armatureObj.animation_data.action_blend_type = 'REPLACE'
            armatureObj.animation_data.action_influence = 1

            # set the frame range
            scene.frame_start = action.frame_range.x
            scene.frame_end = action.frame_range.y

            # export only the armature and the selected animation
            bpy.ops.export_scene.fbx(
                filepath=action_path,
                check_existing=False,
                use_selection=True,
                object_types={'ARMATURE'},
                use_custom_props=False,
                add_leaf_bones=False,
                use_armature_deform_only=True,
                bake_anim=True,
                bake_anim_use_nla_strips=False,
                bake_anim_use_all_actions=False,
                bake_anim_force_startend_keying=True,
                use_metadata=False,
                primary_bone_axis = 'X',
                secondary_bone_axis = '-Y',	    
                axis_forward = 'X',
                axis_up = 'Z',
                bake_space_transform = False
            )

        # restore the saved stuff
        armatureObj.animation_data.action = savedAction #Resets previous action and NLA
        armatureObj.animation_data.action_extrapolation = savedAction_extrapolation
        armatureObj.animation_data.action_blend_type = savedAction_blend_type
        armatureObj.animation_data.action_influence = savedAction_influence
                
        # now export the armature and mesh
        bpy.ops.export_scene.fbx(
            filepath=fullpath,
            check_existing=False,
            use_selection=True,
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

        # delete the duplicated objects
        bpy.ops.object.delete()
        
        # set the active back to the original armature and select it
        bpy.context.view_layer.objects.active = activeObj
        activeObj.select_set(True)
        
        return {'FINISHED'}
