import bpy
import os
from bpy.props import (
		StringProperty,
		BoolProperty,
        )

class UE4_AP_AddonPreferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    skeletonRootBoneName: StringProperty(
        name='Skeleton root bone name',
		description='Name of the armature when exported.',
		default="Armature",
		)
    static_prefix_export_name: bpy.props.StringProperty(
		name = "StaticMesh Prefix",
		description = "Prefix of staticMesh",
		maxlen = 32,
		default = "SM_")

    skeletal_prefix_export_name: bpy.props.StringProperty(
		name = "SkeletalMesh Prefix ",
		description = "Prefix of SkeletalMesh",
		maxlen = 32,
		default = "SK_")

    anim_prefix_export_name: bpy.props.StringProperty(
		name = "AnimationSequence Prefix",
		description = "Prefix of AnimationSequence",
		maxlen = 32,
		default = "Anim_")

    pose_prefix_export_name: bpy.props.StringProperty(
		name = "AnimationSequence(Pose) Prefix",
		description = "Prefix of AnimationSequence with only one frame",
		maxlen = 32,
		default = "Pose_")

    anim_subfolder_name: bpy.props.StringProperty(
		name = "Animations sub folder name",
		description = "name of sub folder for animations",
		maxlen = 32,
		default = "Anim")

    export_static_file_path: bpy.props.StringProperty(
		name = "StaticMesh export file path",
		description = "Choose a directory to export StaticMesh(s)",
		maxlen = 512,
		default = os.path.join("//","ExportedFbx","StaticMesh"),
		subtype = 'DIR_PATH')

    export_skeletal_file_path: bpy.props.StringProperty(
		name = "SkeletalMesh export file path",
		description = "Choose a directory to export SkeletalMesh(s)",
		maxlen = 512,
		default = os.path.join("//","ExportedFbx","SkeletalMesh"),
		subtype = 'DIR_PATH')

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        col.prop(self, 'skeletonRootBoneName')
        col.prop(self, 'static_prefix_export_name', icon='OBJECT_DATA')
        col.prop(self, 'skeletal_prefix_export_name', icon='OBJECT_DATA')
        col.prop(self, 'anim_prefix_export_name', icon='OBJECT_DATA')
        col.prop(self, 'pose_prefix_export_name', icon='OBJECT_DATA')
        col.prop(self, 'export_static_file_path',icon='FILE_FOLDER')
        col.prop(self, 'export_skeletal_file_path',icon='FILE_FOLDER')
        #col.prop(self, 'anim_subfolder_name',icon='FILE_FOLDER')
