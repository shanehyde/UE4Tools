import bpy
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "UE4Tools",
    "author" : "Shane Hyde",
    "description" : "UE4 Tools",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "View3D",
    "warning" : "",
    "category" : "Export"
}

import bpy

from . test_op import UE4_OT_Operator
from . test_panel import UE4_PT_Panel
from . prefs import UE4_AP_AddonPreferences
from . origin_op import UE4_OT_SetOriginToBase
from . export_armature_op import UE4_OT_ExportArmature
from . export_static import UE4_OT_ExportMesh

classes = (
    UE4_OT_Operator, 
    UE4_PT_Panel,
    UE4_AP_AddonPreferences,
    UE4_OT_SetOriginToBase,
    UE4_OT_ExportMesh,
    UE4_OT_ExportArmature)

register, unregister = bpy.utils.register_classes_factory(classes)

 