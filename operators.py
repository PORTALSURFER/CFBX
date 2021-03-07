# Copyright PORTALSURFER, No rights reserved.
# https: //www.blender.org/about/license/

import bpy
from .functions import export, utilities, graphics
from .ui import export_preferences


class CFBX_OT_export_active_collection(bpy.types.Operator):
    """
    Export the current active collection to target fbx file
    """
    bl_idname = "wm.cbfx_export_fbx"
    bl_label = "Export collection to FBX"

    def execute(self, context):
        export.export(self, context)

        return {'FINISHED'}


class CFBX_OT_open_properties(bpy.types.Operator):
    """
    Open settings dialog
    """
    bl_idname = "wm.cbfx_properties_dialog"
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


class CFBX_OT_select_path(bpy.types.Operator):
    """Set the export path for all selected assets"""
    bl_idname = "hexporter.path_selector"
    bl_label = "Accept"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    filter_folder: bpy.props.BoolProperty(default=True, options={'HIDDEN'})
    directory: bpy.props.StringProperty(subtype='DIR_PATH')

    def execute(self, context):
        # context.active_object.select_set(True)

        context.view_layer.active_layer_collection.collection.CFBX_settings.fbx_folder_path = self.directory

        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
