import bpy
from .functions import move_iso_objects, isoq_light_hypotenuse, isoq_light_distance, isoq_plane_emission

class ISOQ_OT_StructGen(bpy.types.Operator):
    """Generate isometric floors and walls"""

    bl_idname = "object.isometric_operator"
    bl_label = "New Room"
    bl_options = {'REGISTER', 'UNDO'}

    floor_scale_value: bpy.props.FloatProperty(
        name='Floor Scale',
        default = 4,
        min = 0
    )
    
    wall_height_value: bpy.props.FloatProperty(
        name='Wall height',
        default = 4,
        min = 0
    )
    
    equal_thickness_value: bpy.props.FloatProperty(
        name='Thickness',
        default = 0.15,
        min = 0
    )
    
    wall_thickness_value: bpy.props.FloatProperty(
        name='Edit Wall Thickness',
        default = 0,
        min = 0
    )

    floor_thickness_value: bpy.props.FloatProperty(
        name='Edit Floor Thickness',
        default = 0,
        min = 0
    )
    
    x_extrude_value: bpy.props.FloatProperty(
        name='Extrude X',
        default = 0,
        min = 0
    )
    
    y_extrude_value: bpy.props.FloatProperty(
        name='Extrude Y',
        default = 0,
        min = 0
    )
            
    def add_floor(self, cursor, scale, floor_thickness, x_extrude, y_extrude):
        bpy.ops.mesh.primitive_plane_add(
                                    size=1,
                                    enter_editmode=False,
                                    align='WORLD',
                                    location=(
                                        cursor[0],
                                        cursor[1],
                                        cursor[2]
                                        )
                                    )
        bpy.ops.transform.resize(value=(scale+x_extrude, scale+y_extrude, 1), orient_type='GLOBAL')
        bpy.ops.transform.translate(value=(x_extrude/2,-(y_extrude/2), 0), orient_type='GLOBAL')
        bpy.context.object.name = "Iso Floor"
        if floor_thickness:
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.modifiers["Solidify"].thickness = floor_thickness

    def add_leftwall(self, cursor, scale, wall_thickness, wall_height, floor_thickness, y_extrude):
        bpy.ops.mesh.primitive_plane_add(size=1,
                                    enter_editmode=False,
                                    align='WORLD',
                                    location=(
                                        -scale/2+cursor[0],
                                        cursor[1],
                                        wall_height/2+cursor[2]
                                        )
                                    )
        bpy.context.object.rotation_euler[1] = 1.5708
        bpy.ops.transform.resize(value=(1, scale+y_extrude, wall_height+floor_thickness))
        bpy.ops.transform.translate(value=(0, -y_extrude/2, -floor_thickness/2), orient_type='GLOBAL')
        bpy.context.object.name = "Iso Left Wall"
        if wall_thickness:
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.modifiers["Solidify"].thickness = wall_thickness

    def add_rightwall(self, cursor, scale, wall_thickness, wall_height, floor_thickness, x_extrude, offset):
        bpy.ops.mesh.primitive_plane_add(size=1,
                                    enter_editmode=False,
                                    align='WORLD',
                                    location=(
                                        -offset/2+cursor[0],
                                        scale/2+cursor[1],
                                        wall_height/2+cursor[2]))
        bpy.context.object.rotation_euler[0] = 1.5708
        bpy.ops.transform.resize(value=(scale+offset+x_extrude, 1, wall_height+floor_thickness))
        bpy.ops.transform.translate(value=(x_extrude/2, 0, 0-floor_thickness/2), orient_type='GLOBAL')
        bpy.context.object.name = "Iso Right Wall"
        if wall_thickness:
            bpy.ops.object.modifier_add(type='SOLIDIFY')
            bpy.context.object.modifiers["Solidify"].thickness = wall_thickness

    def add_hidden_ceiling(self, cursor, scale, height, x_extrude, y_extrude):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(cursor[0], cursor[1], height+cursor[2]))
        bpy.ops.transform.resize(value=(scale+x_extrude, scale+y_extrude, 1), orient_type='GLOBAL')
        bpy.ops.transform.translate(value=(x_extrude/2, -y_extrude/2, 0), orient_type='GLOBAL')
        bpy.context.object.name = "Hidden Ceiling"
        bpy.context.object.cycles_visibility.camera = False
        bpy.ops.object.hide_view_set(unselected=False)


    def add_hidden_leftwall(self, cursor, scale, height, x_extrude, y_extrude):
        bpy.ops.mesh.primitive_plane_add(
                                    size=1,
                                    enter_editmode=False,
                                    align='WORLD',
                                    location=(
                                        x_extrude/2+cursor[0],
                                        -1*scale/2-y_extrude+cursor[1],
                                        height/2+cursor[2]
                                        )
                                    )
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL')
        bpy.ops.transform.resize(value=(scale + x_extrude, 1, height), orient_type='GLOBAL')
        bpy.context.object.name = "Hidden Left Wall"
        bpy.context.object.cycles_visibility.camera = False
        bpy.ops.object.hide_view_set(unselected=False)
    
    def add_hidden_rightwall(self, cursor, scale, height, x_extrude, y_extrude):
        bpy.ops.mesh.primitive_plane_add(
                                    size=1,
                                    enter_editmode=False,
                                    align='WORLD',
                                    location=(
                                        scale/2+x_extrude+cursor[0],
                                        -y_extrude/2+cursor[1],
                                        height/2+cursor[2]
                                        )
                                    )
        bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL')
        bpy.ops.transform.resize(value=(1, scale + y_extrude, height), orient_type='GLOBAL')
        bpy.context.object.name = "Hidden Right Wall"
        bpy.context.object.cycles_visibility.camera = False
        bpy.ops.object.hide_view_set(unselected=False)

    def add_left_light(self, cursor, scale, height, wall_thickness, y_extrude):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(cursor[0], cursor[1], cursor[2]))
        bpy.context.object.name = "ISO Emission Left"
        bpy.ops.transform.translate(value=(-1*isoq_light_distance(scale, height, wall_thickness), -y_extrude/2, height/2), orient_type='GLOBAL')
        bpy.ops.transform.resize(value=(isoq_light_hypotenuse(height), scale+y_extrude, 1), orient_type='GLOBAL')
        bpy.ops.transform.rotate(value=-0.785398, orient_axis='Y', orient_type='GLOBAL')
        bpy.context.object.cycles_visibility.camera = False

    def add_right_light(self, cursor, scale, height, wall_thickness, x_extrude):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(cursor[0], cursor[1], cursor[2]))
        bpy.context.object.name = "ISO Emission Right"
        bpy.ops.transform.translate(value=(x_extrude/2, isoq_light_distance(scale, height, wall_thickness), height/2), orient_type='GLOBAL')
        bpy.ops.transform.resize(value=(scale+x_extrude, isoq_light_hypotenuse(height), 1), orient_type='GLOBAL')
        bpy.ops.transform.rotate(value=-0.785398, orient_axis='X', orient_type='GLOBAL')
        bpy.context.object.cycles_visibility.camera = False
    
    @classmethod
    def poll(cls, context):
        return context.area.type == "VIEW_3D"

    def execute(self, context):
        cursor = bpy.context.scene.cursor.location
        iso_tool = context.scene.iso_tool
        floor_scale = self.floor_scale_value
        floor_thickness = self.floor_thickness_value+self.equal_thickness_value
        wall_thickness = self.wall_thickness_value+self.equal_thickness_value
        x_extrude = self.x_extrude_value
        y_extrude = self.y_extrude_value
        wall_height = self.wall_height_value
        
        if iso_tool.create_left_wall:
            self.add_leftwall(cursor, floor_scale, wall_thickness, wall_height, floor_thickness, y_extrude)
        
        if iso_tool.create_right_wall and iso_tool.create_left_wall:
            self.add_rightwall(cursor, floor_scale, wall_thickness, wall_height, floor_thickness, x_extrude, wall_thickness)
        elif iso_tool.create_right_wall:
            self.add_rightwall(cursor, floor_scale, wall_thickness, wall_height, floor_thickness, x_extrude, 0)
        
        if iso_tool.create_floor:
            self.add_floor(cursor, floor_scale, floor_thickness, x_extrude, y_extrude)
        
        if iso_tool.create_right_light:
            self.add_right_light(cursor, floor_scale, wall_height, wall_thickness, x_extrude)

        if iso_tool.create_left_light:
            self.add_left_light(cursor, floor_scale, wall_height, wall_thickness, y_extrude)
        
        if iso_tool.create_hidden_ceiling:
            self.add_hidden_ceiling(cursor, floor_scale, wall_height, x_extrude, y_extrude)
        
        if iso_tool.create_hidden_rightwall:
            self.add_hidden_rightwall(cursor, floor_scale, wall_height, x_extrude, y_extrude)
        
        if iso_tool.create_hidden_leftwall:
            self.add_hidden_leftwall(cursor, floor_scale, wall_height, x_extrude, y_extrude)


        move_iso_objects()
        isoq_plane_emission()
        return {"FINISHED"}
