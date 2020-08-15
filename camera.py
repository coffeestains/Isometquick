import bpy
from .functions import move_iso_objects

class ISOQ_OT_True_Camera(bpy.types.Operator):
    """Generates isometric camera which is 35.264 to the horizontal axes"""

    bl_idname = "object.isocamera1_operator"
    bl_label = "True Isometric Camera"
    bl_options = {'REGISTER', 'UNDO'}
    
    true_iso_cam_ortho: bpy.props.FloatProperty(
        name='Orthographic Scale',
        default = 9.5
    )
    
    true_iso_cam_height: bpy.props.FloatProperty(
        name='Ajust Height',
        default = 0
    )
    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        iso_tool = context.scene.iso_tool
        bpy.ops.object.camera_add(align='VIEW', location=(25,-25,self.true_iso_cam_height+iso_tool.default_iso_cam_height), rotation=(0.954695, 6.98132e-08, 0.785398))
        bpy.context.object.data.type = 'ORTHO'
        bpy.context.object.name = "Isometric Camera"
        bpy.context.object.data.ortho_scale = self.true_iso_cam_ortho

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                break
        move_iso_objects()
        return {"FINISHED"}
    
    
class ISOQ_OT_Game_Camera(bpy.types.Operator):
    """Generates game isometric camera which is 30° to the horizontal axes"""

    bl_idname = "object.isocameragame_operator"
    bl_label = "Game Isometric Camera"
    bl_options = {'REGISTER', 'UNDO'}
    
    game_iso_cam_ortho: bpy.props.FloatProperty(
        name='Orthographic Scale',
        default = 9.5
    )
    
    game_iso_cam_height: bpy.props.FloatProperty(
        name='Adjust Height',
        default = -4.65
    )

    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        iso_tool = context.scene.iso_tool
        bpy.ops.object.camera_add(align='VIEW', location=(25,-25,self.game_iso_cam_height+iso_tool.default_iso_cam_height), rotation=(1.0472, 6.98132e-08, 0.785398))
        bpy.context.object.data.type = 'ORTHO'
        bpy.context.object.name = "Isometric Game Camera"
        bpy.context.object.data.ortho_scale = self.game_iso_cam_ortho

        for area in bpy.context.screen.areas:
            if area.type == 'VIEW_3D':
                area.spaces[0].region_3d.view_perspective = 'CAMERA'
                break
        move_iso_objects()
        return {"FINISHED"}


class ISOQ_OT_set_resolution(bpy.types.Operator):
    """Generates game isometric camera which is 30° to the horizontal axes"""

    bl_idname = "object.isoset_resolution"
    bl_label = "Set resolution"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        iso_tool = context.scene.iso_tool
        res = iso_tool.select_iso_res.split("x")
        bpy.context.scene.render.resolution_x = int(res[0])
        bpy.context.scene.render.resolution_y = int(res[1])
        return {"FINISHED"}


