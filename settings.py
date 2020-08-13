import bpy

class ISOQ_settings(bpy.types.PropertyGroup):
    
    thickness_bool : bpy.props.BoolProperty(
        name = 'Equal thickness',
        default = True
    )

    create_right_wall : bpy.props.BoolProperty(
        name = 'Right Wall',
        default = True
    )
    
    create_left_wall : bpy.props.BoolProperty(
        name = 'Left Wall',
        default = True
    )
    
    create_floor : bpy.props.BoolProperty(
        name = 'Floor',
        default = True
    )
    
    default_iso_cam_height: bpy.props.FloatProperty(
        name='Ajust Height',
        default = 27.03
    )
    
    create_right_light : bpy.props.BoolProperty(
        name = 'Right Light',
        default = False
    )
    
    create_left_light : bpy.props.BoolProperty(
        name = 'Left Light',
        default = False
    )
    
    create_hidden_ceiling : bpy.props.BoolProperty(
        name = 'Hidden Ceiling',
        default = False
    )
    
    create_hidden_rightwall : bpy.props.BoolProperty(
        name = 'Hidden Right Wall',
        default = False
    )

    create_hidden_leftwall : bpy.props.BoolProperty(
        name = 'Hidden Left Wall',
        default = False
    )

    select_iso_res : bpy.props.EnumProperty(
        name="",
        description="Apply Res",
        items=[
            ("1024x1024", "1024 x 1024", ""),
            ("2048x2048", "2048 x 2048", ""),
            ("4096x4096", "4096 x 4096", ""),
            ("8192x8192", "8192 x 8192", ""),
            ("1280x720",  "1280 x 720", ""),
            ("1600x900",  "1600 x 900", ""),
            ("1920x1080", "1920 x 1080", ""),
            ("2560x1440", "2560 x 1440", ""),
            ("3840x2160", "3840 x 2160", ""),
            ("7680x4320", "7680 x 4320", ""),
            ],
            default='2048x2048'
        )