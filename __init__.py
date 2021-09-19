# Copyright (C) 2020 Noel Francis Lobo
# codellectual@gmail.com
# Created by Noel Lobo
# (codellect - instagram | coffeestains - github)
#
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
# 
#
# Have fun :)

bl_info = {
    "name": "Isometquick",
    "author": "Noel Francis Lobo (Github:@coffeestains Instagram:@codellect)",
    "description": "Creates an isometric room model and appropriate cameras",
    "location": "N-Panel",
    "blender": (2, 80, 0),
    "version": (1, 0, 0),
    "location": "",
    "wiki_url": "https://github.com/coffeestains",
    "warning": "",
    "category": "Add Mesh",
}

import bpy
from .settings import ISOQ_settings
from .camera import ISOQ_OT_True_Camera, ISOQ_OT_Game_Camera, ISOQ_OT_set_resolution
from .UI import ISOQ_PT_IsometricPanel, ISOQ_PT_CameraPanel
from .operators import ISOQ_OT_StructGen

isoq_classes = (
ISOQ_OT_StructGen,
ISOQ_PT_IsometricPanel,
ISOQ_PT_CameraPanel,
ISOQ_OT_True_Camera,
ISOQ_OT_Game_Camera,
ISOQ_settings,
ISOQ_OT_set_resolution
)

def register():
    for each_class in isoq_classes:
        bpy.utils.register_class(each_class)
    bpy.types.Scene.iso_tool = bpy.props.PointerProperty(type=ISOQ_settings)

def unregister():
    for each_class in isoq_classes:
        bpy.utils.unregister_class(each_class)


if __name__ == "__main__":
    register()
