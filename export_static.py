import bpy
import os
import mathutils
import math

from . util import *

class UE4_OT_ExportMesh(bpy.types.Operator):

    bl_idname = "ue4tools.export_mesh"
    bl_description = "Export Mesh to UE4"
    bl_label = "Export Mesh to UE4"

    @classmethod
    def poll(cls, context):
        return context.active_object and context.active_object.type == "MESH"

    def execute(self, context):

        preferences = bpy.context.preferences
        addon_prefs = preferences.addons['UE4Tools'].preferences
      
        scene = bpy.context.scene

        activeObj = bpy.context.active_object
        #print("Original active object = %s" % activeObj.name)
        filename_prefix = addon_prefs.static_prefix_export_name
        filename = filename_prefix + activeObj.name + ".fbx"

        dirpath = addon_prefs.export_static_file_path
        absdirpath = bpy.path.abspath(dirpath)
        absdirpath = os.path.join( absdirpath , activeObj.name)
        if not os.path.exists(absdirpath):
            os.makedirs(absdirpath)
        fullpath = os.path.join( absdirpath ,  filename )

        #bpy.ops.object.select_hierarchy(direction='CHILD', extend=True)
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

        meshObj = bpy.context.active_object
        #print("New active name = %s" % armatureObj.name)
    
        #for obj in bpy.context.selected_objects:
        #    print(obj.name)

        ApplyNeededModifierToSelect()
        if RemoveMaterialsFromSelectedObjects():

            newMatrix = meshObj.matrix_world @ mathutils.Matrix.Translation((0,0,0))
            saveScale = meshObj.scale * 1
            mat_trans = mathutils.Matrix.Translation((0,0,0))
            mat_rot = newMatrix.to_quaternion().to_matrix()
            newMatrix = mat_trans @ mat_rot.to_4x4()
            eul = mathutils.Euler((0,0, math.radians(90.0)), 'ZXY')
            newMatrix = newMatrix @ eul.to_matrix().to_4x4()
            
            meshObj.matrix_world = newMatrix
            meshObj.scale = saveScale

            #print(fullpath)
                    
            bpy.ops.export_scene.fbx(
                filepath=fullpath,
                check_existing=False,
                use_selection=True,
                #global_scale=GetObjExportScale(active),
                object_types={'MESH'},
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
        
            bpy.context.view_layer.objects.active = activeObj
            activeObj.select_set(True)
            self.report({'INFO'}, "Exported %s successfully" % filename )
        else:
            bpy.ops.object.delete()
        
            bpy.context.view_layer.objects.active = activeObj
            activeObj.select_set(True)
            self.report({'INFO'}, "No Default Material" )
    
        return {'FINISHED'}
