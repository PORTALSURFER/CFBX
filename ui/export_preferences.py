# Copyright UHX, No rights reserved.
# https: //www.blender.org/about/license/

import bpy
from ..properties import UHXporterProperties, UHXporterUIProperties
from ..functions import graphics
# from ..functions import utilities

class ExportPreferences(UHXporterProperties, UHXporterUIProperties, bpy.types.AddonPreferences):
    """
    Settings interface class
    """
    bl_idname = __package__.split('.')[0]

    def draw(self, context, properties=None):

        layout = self.layout

        if not properties:
            properties = self

        layout.label(text="test")

        row = layout.row()
        row.prop(properties, 'options_type', expand=True)

        if properties.options_type == 'paths':

            row = layout.row()
            row.prop(bpy.context.view_layer.active_layer_collection.collection.UHXporter_settings,
                     'should_export', text="Should Export")
            row.prop(bpy.context.view_layer.active_layer_collection.collection.UHXporter_settings,
                     'export_name_prefix', text="Prefix")

            row = layout.row()
            row.prop(bpy.context.view_layer.active_layer_collection.collection.UHXporter_settings,
                     'fbx_folder_path', text="Export Path")
