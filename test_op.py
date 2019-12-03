import bpy

class UE4_OT_Operator(bpy.types.Operator):
    bl_idname = "view3d.cursor_center"
    bl_label = "Simple operator"
    bl_description = "Center 3d cursor"

    def execute(self, context):
        #bpy.ops.view3d.snap_cursor_to_center()

        addon_prefs = context.preferences.addons[__package__].preferences
        info = ("Test %s" % addon_prefs.skeletal_prefix_export_name)
        self.report({'INFO'}, info)
        #print(info)
        #print("Hello")
        return {'FINISHED'}