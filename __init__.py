# Copyright UHX, No rights reserved.
# https: //www.blender.org/about/license/

import bpy
import importlib
from . import operators
from . import properties
from .functions import graphics
from .ui import header_menu, export_preferences

bl_info = {
    "name": "UHXporter",
    "author": "UHX",
    "blender": (2, 80, 0),
    "version": (0, 0, 1),
    "location": "Header -> UHXporter -> Export",
    "description": "Export active collection as FBX",
    "warning": "",
    "category": "Export"
}

modules = [
    operators,
    properties,
    export_preferences
]

classes = [
    operators.Export,
    operators.PropertiesDialog,
    operators.UpdateDrawUHXCollectionIcon,
    export_preferences.ExportPreferences,
    header_menu.TOPBAR_MT_UHX_export,
    header_menu.TOPBAR_MT_UHX_set_properties
]


class TEST(bpy.types.Panel):
    bl_idname = "OUTLINER_HT_UHXheader"
    bl_label = "UHXporter Collection Header"
    bl_space_type = 'OUTLINER'
    bl_region_type = 'WINDOW'
    bl_context = "collection"

    def __init__(self):
        print("things")

    def draw(self, context):
        print("draw panel")
        self.layout.label(text="test")


def register():
    """
    This function registers the addon classes when the addon is enabled.
    """
    # reload the submodules
    for module in modules:
        importlib.reload(module)

    # register the properties
    properties.register()

    # register the classes
    for cls in classes:
        bpy.utils.register_class(cls)

    header_menu.add_uhxporter_menu()

    bpy.utils.register_class(TEST)


def unregister():
    """
    This function unregisters the addon classes when the addon is disabled.
    """
    # remove the header menu
    header_menu.remove_parent_menu()

    bpy.utils.unregister_class(TEST)

    # unregister the classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    # unregister the properties
    properties.unregister()
