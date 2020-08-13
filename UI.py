import bpy

class ISOQ_PT_IsometricPanel(bpy.types.Panel):
    bl_idname = "PT_IsometricGen"
    bl_label = "Isometquick"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Iso"
    

    def draw(self, context):
        layout = self.layout
        iso_tool = context.scene.iso_tool
        
        row = layout.row()
        row.label(text="Room Settings", icon="CUBE")
        box = layout.box()
        column = box.column()
        row = column.split(factor=0.3)
        row.label(text="Toggle Parts:")
        row = row.row(align=True)
        row.prop(iso_tool, "create_left_wall", text="L Wall", toggle=True)
        row.prop(iso_tool, "create_right_wall", text="R Wall", toggle=True)
        row = column.split(factor=0.3)
        row.label(text="")
        row = row.row(align=True)
        row.prop(iso_tool, "create_floor", text="Floor", toggle=True)
        column = box.column()
        row = column.split(factor=0.3)
        row.label(text="Toggle Hidden:")
        row = row.row(align=True)
        row.prop(iso_tool, "create_hidden_ceiling", text="Hidden Ceiling", toggle=True)
        row = column.split(factor=0.3)
        row.label(text="(for shadows)")
        row = row.row(align=True)
        row.prop(iso_tool, "create_hidden_leftwall", text="Hidden L Wall", toggle=True)
        row.prop(iso_tool, "create_hidden_rightwall", text="Hidden R Wall", toggle=True)
        column = box.column()
        row = column.split(factor=0.3)
        row.label(text="Incoming Light:")
        row = row.row(align=True)
        row.prop(iso_tool, "create_left_light", text="Left", toggle=True)
        row.prop(iso_tool, "create_right_light", text="Right", toggle=True)
        column = box.column()
        row = column.split(factor=0.3)
        row.label(text="Generate:")
        row = row.row(align=True)
        row.scale_y = 1.2
        row.operator("object.isometric_operator")
        row = layout.row()

            
class ISOQ_PT_CameraPanel(bpy.types.Panel):
    bl_idname = "PT_IsometricGen2"
    bl_label = "Isometquick Camera"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Iso"
    

    def draw(self, context):
        layout = self.layout
        obj = bpy.context.object
        row = layout.row()
        iso_tool = context.scene.iso_tool


        row.label(text="Camera Settings", icon="CAMERA_DATA")
        box = layout.box()
        column = box.column()
        row = column.split(factor=0.3)
        row.label(text="Generate Cam:")
        row = row.row(align=True)
        row.scale_y = 1.2
        row.operator("object.isocamera1_operator")
        row = layout.row()
        row = column.split(factor=0.3)
        row.label(text="")
        row.scale_y = 1.2
        row.operator("object.isocameragame_operator")
        
        column = box.column()
        row = column.split(factor=0.3)
        row.label(text="Select Preset:")
        row = row.row(align=True)
        row.prop(iso_tool, "select_iso_res")
        row = layout.row()
        column = box.column()
        row = column.split(factor=0.3)
        row.label(text="")
        row = row.row(align=True)
        row.scale_y = 1.2
        row.operator("object.isoset_resolution")
        row = layout.row()

        column = box.column()
        row = column.split(factor=0.31)
        row.label(text="Custom Resolution:")
        row.prop(context.scene.render, "resolution_x")
        row.prop(context.scene.render, "resolution_y")
        row = layout.row()
        
        if obj is not None and obj.type == 'CAMERA':
            row = column.split(factor=0.3)
            row.label(text="")
            row.prop(context.object.data, "ortho_scale")