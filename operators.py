import bpy
from .functions import move_iso_objects, ISOQ_light_hypotenuse, ISOQ_light_distance, ISOQ_plane_emission

class ISOQ_OT_StructGen(bpy.types.Operator):
    """Generate isometric floors and walls"""

    bl_idname = "object.isometric_operator"
    bl_label = "New Room"
    bl_options = {'REGISTER', 'UNDO'}

    floor_scale_value: bpy.props.FloatProperty(
        name='Floor Scale',
        default = 4
    )
    
    wall_height_value: bpy.props.FloatProperty(
        name='Wall height',
        default = 4
    )
    
    equal_thickness_value: bpy.props.FloatProperty(
        name='Thickness',
        default = 0.15
    )
    
    wall_thickness_value: bpy.props.FloatProperty(
        name='Edit Wall Thickness',
        default = 0
    )

    floor_thickness_value: bpy.props.FloatProperty(
        name='Edit Floor Thickness',
        default = 0
    )
    
    x_extrude_value: bpy.props.FloatProperty(
        name='Extrude X',
        default = 0
    )
    
    y_extrude_value: bpy.props.FloatProperty(
        name='Extrude Y',
        default = 0
    )
            
    def add_floor(self, scale, floor_thickness, x_extrude, y_extrude):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        bpy.context.object.name = "Iso Floor"
        bpy.ops.transform.resize(value=(scale+x_extrude, scale+y_extrude, 1), orient_type='GLOBAL')
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = floor_thickness
        bpy.ops.transform.translate(value=(x_extrude/2, -y_extrude/2, 0), orient_type='GLOBAL')

    def add_leftwall(self, scale, wall_thickness, wall_height, floor_thickness, y_extrude):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(-scale/2, 0, wall_height/2))
        bpy.context.object.name = "Iso Left Wall"
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = wall_thickness
        bpy.context.object.rotation_euler[1] = 1.5708
        bpy.ops.transform.resize(value=(1, scale+y_extrude, wall_height+floor_thickness))
        bpy.ops.transform.translate(value=(0, -y_extrude/2, -floor_thickness/2), orient_type='GLOBAL')

    def add_rightwall(self, scale, wall_thickness, wall_height, floor_thickness, x_extrude, offset):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0-offset/2, scale/2, wall_height/2))
        bpy.context.object.name = "Iso Right Wall"
        bpy.ops.object.modifier_add(type='SOLIDIFY')
        bpy.context.object.modifiers["Solidify"].thickness = wall_thickness
        bpy.context.object.rotation_euler[0] = 1.5708
        bpy.ops.transform.resize(value=(scale+offset+x_extrude, 1, wall_height+floor_thickness))
        bpy.ops.transform.translate(value=(x_extrude/2, 0, 0-floor_thickness/2), orient_type='GLOBAL')

    def add_hidden_ceiling(self, scale, height, x_extrude, y_extrude):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, height))
        bpy.ops.transform.resize(value=(scale+x_extrude, scale+y_extrude, 1), orient_type='GLOBAL')
        bpy.ops.transform.translate(value=(x_extrude/2, -y_extrude/2, 0), orient_type='GLOBAL')
        bpy.context.object.name = "Hidden Ceiling"
        bpy.context.object.cycles_visibility.camera = False
        bpy.ops.object.hide_view_set(unselected=False)


    def add_hidden_leftwall(self, scale, height, x_extrude, y_extrude):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(x_extrude/2, -1*scale/2-y_extrude, height/2))
        bpy.ops.transform.rotate(value=1.5708, orient_axis='X', orient_type='GLOBAL')
        bpy.ops.transform.resize(value=(scale + x_extrude, 1, height), orient_type='GLOBAL')
        bpy.context.object.name = "Hidden Left Wall"
        bpy.context.object.cycles_visibility.camera = False
        bpy.ops.object.hide_view_set(unselected=False)
    
    def add_hidden_rightwall(self, scale, height, x_extrude, y_extrude):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(scale/2+x_extrude, -y_extrude/2, height/2))
        bpy.ops.transform.rotate(value=1.5708, orient_axis='Y', orient_type='GLOBAL')
        bpy.ops.transform.resize(value=(1, scale + y_extrude, height), orient_type='GLOBAL')
        bpy.context.object.name = "Hidden Right Wall"
        bpy.context.object.cycles_visibility.camera = False
        bpy.ops.object.hide_view_set(unselected=False)

    def add_left_light(self, scale, height, wall_thickness, y_extrude):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        bpy.context.object.name = "ISO Emission Left"
        bpy.ops.transform.translate(value=(-1*ISOQ_light_distance(scale, height, wall_thickness), -y_extrude/2, height/2), orient_type='GLOBAL')
        bpy.ops.transform.resize(value=(ISOQ_light_hypotenuse(height), scale+y_extrude, 1), orient_type='GLOBAL')
        bpy.ops.transform.rotate(value=-0.785398, orient_axis='Y', orient_type='GLOBAL')
        bpy.context.object.cycles_visibility.camera = False

    def add_right_light(self, scale, height, wall_thickness, x_extrude):
        bpy.ops.mesh.primitive_plane_add(size=1, enter_editmode=False, align='WORLD', location=(0, 0, 0))
        bpy.context.object.name = "ISO Emission Right"
        bpy.ops.transform.translate(value=(x_extrude/2, ISOQ_light_distance(scale, height, wall_thickness), height/2), orient_type='GLOBAL')
        bpy.ops.transform.resize(value=(scale+x_extrude, ISOQ_light_hypotenuse(height), 1), orient_type='GLOBAL')
        bpy.ops.transform.rotate(value=-0.785398, orient_axis='X', orient_type='GLOBAL')
        bpy.context.object.cycles_visibility.camera = False
        
    def execute(self, context):
        iso_tool = context.scene.iso_tool
        floor_scale = self.floor_scale_value
        floor_thickness = self.floor_thickness_value+self.equal_thickness_value
        wall_thickness = self.wall_thickness_value+self.equal_thickness_value
        x_extrude = self.x_extrude_value
        y_extrude = self.y_extrude_value
        wall_height = self.wall_height_value
        
        if iso_tool.create_left_wall:
            self.add_leftwall(floor_scale, wall_thickness, wall_height, floor_thickness, y_extrude)
        
        if iso_tool.create_right_wall and iso_tool.create_left_wall:
            self.add_rightwall(floor_scale, wall_thickness, wall_height, floor_thickness, x_extrude, wall_thickness)
        elif iso_tool.create_right_wall:
            self.add_rightwall(floor_scale, wall_thickness, wall_height, floor_thickness, x_extrude, 0)
        
        if iso_tool.create_floor:
            self.add_floor(floor_scale, floor_thickness, x_extrude, y_extrude)
        
        if iso_tool.create_right_light:
            self.add_right_light(floor_scale, wall_height, wall_thickness, x_extrude)

        if iso_tool.create_left_light:
            self.add_left_light(floor_scale, wall_height, wall_thickness, y_extrude)
        
        if iso_tool.create_hidden_ceiling:
            self.add_hidden_ceiling(floor_scale, wall_height,x_extrude, y_extrude)
        
        if iso_tool.create_hidden_rightwall:
            self.add_hidden_rightwall(floor_scale, wall_height,x_extrude, y_extrude)
        
        if iso_tool.create_hidden_leftwall:
            self.add_hidden_leftwall(floor_scale, wall_height,x_extrude, y_extrude)

        move_iso_objects()
        ISOQ_plane_emission()
        return {"FINISHED"}