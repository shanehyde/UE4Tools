import bpy
import mathutils

class UE4_OT_SetOriginToBase(bpy.types.Operator):
    bl_idname = "ue4tools.set_origin_to_base"
    bl_description = "Set Origin to base of object"
    bl_label = "Set Origin to Base"

    @classmethod
    def poll(cls, context):
        #print (context.active_object.type)
        return context.active_object and context.active_object.type == "MESH"

    def execute(self, context):
        active = bpy.context.active_object
        location = bpy.context.scene.cursor.location.copy()
        #print(location)
        
        if active.type == "MESH":
            #print(active.data)
            mesh = active.data
            minz = 100000
            totalx = 0
            totaly = 0
            ix = 0
            for v in mesh.vertices:
                #print(v.co)
                worldv = active.matrix_world @ v.co
                #print(worldv)
                if worldv[2] < minz: 
                    minz = worldv[2]
                totalx += worldv[0]
                totaly += worldv[1]
                ix += 1
            
            V = mathutils.Vector((totalx /ix, totaly / ix, minz))
            #print(V)
            bpy.context.scene.cursor.location = V
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR')

        #print(location)
        bpy.context.scene.cursor.location = location

        return {'FINISHED'}
