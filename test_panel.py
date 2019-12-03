import bpy
from . util import GetAssetType

class UE4_PT_Panel(bpy.types.Panel):
    bl_idname = "UE4_PT_Panel"
    bl_label = "UE4 Tools"
    bl_category = "UE4 Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('ue4tools.set_origin_to_base', text="Set Origin", icon='EMPTY_AXIS')
        row = layout.row()
        row.scale_y = 1.5
        row.operator('ue4tools.export_armature', text="Export Armature", icon='EXPORT')
        row = layout.row()
        row.scale_y = 1.5
        row.operator('ue4tools.export_mesh', text="Export Mesh", icon='EXPORT')