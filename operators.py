# Copyright UHX, No rights reserved.
# https: //www.blender.org/about/license/

import bpy
from .functions import export, utilities, graphics
from .ui import export_preferences


class Export(bpy.types.Operator):
    """
    Export the current active collection to target fbx file
    """
    bl_idname = "wm.uhx_export_fbx"
    bl_label = "Export collection to FBX"

    def execute(self, context):
        export.export(self, context)
        return {'FINISHED'}


class PropertiesDialog(bpy.types.Operator):
    """
    Open settings dialog
    """
    bl_idname = "wm.uhx_properties_dialog"
    bl_label = "Opens the properties"

    def execute(self, context):
        properties = bpy.context.preferences.addons[__package__].preferences
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def draw(self, context):
        properties = bpy.context.preferences.addons[__package__].preferences
        export_preferences.ExportPreferences.draw(self, context, properties)


class UpdateDrawUHXCollectionIcon(bpy.types.Operator):
    """
    Draws an graphic in the collection menu to inform if the selected collection is export ready
    """
    bl_idname = "object.uhx_update_collection_graphic"
    bl_label = "UHXCollection graphic"
    bl_description = "Operator for collection graphic"
    bl_options = {'REGISTER'}

    def execute(self, context):
        print("invoke icon update")

        return {'FINISHED'}
