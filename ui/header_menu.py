# Copyright PORTALSURFER, No rights reserved.
# https: //www.blender.org/about/license/

import bpy
from ..functions import graphics


class TOPBAR_MT_CFBX_export(bpy.types.Menu):
    """
    This defines a new class that will be the menu "Export".
    """
    bl_idname = "TOPBAR_MT_CFBX_export"
    bl_label = "Export"

    def draw(self, context):
        self.layout.operator('wm.cbfx_export_fbx')


class TOPBAR_MT_CFBX_set_properties(bpy.types.Menu):
    """
    This defines a new class that will be the menu "Set Properties"
    """
    bl_idname = "TOPBAR_MT_CFBX_set_properties"
    bl_label = "Properties"

    def draw(self, context):
        self.layout.operator('wm.cbfx_properties_dialog')


class TOPBAR_MT_CFBX(bpy.types.Menu):
    """
    This defines a new class that will be the top most parent menu, "CFBX".
    All the other action menu items are children of this.
    """
    bl_idname = "TOPBAR_MT_CFBX"
    bl_label = "CFBX"

    def draw(self, context):
        pass


def cfbx_menu(self, context):
    """
    This function creates the CFBX menu item.
    This will be referenced in other functions as a means of appending and removing it's contents from the top bar editor class definition.

    :param object self: this refers to the enu class definition that this function will append to.
    :param object context: This parameter will take the current blender context by default, or can be passed an explicit context.
    """

    self.layout.menu(TOPBAR_MT_CFBX.bl_idname)


def export_menu(self, context):
    """
    This function creates the export menu item.
    This will be referenced in other functions as a means of
    appending and removing it's contents from the top bar editor class definition.
    """
    self.layout.menu(TOPBAR_MT_CFBX_export.bl_idname)


def properties_menu(self, context):
    """
    This function creates the properties menu item.
    This will be referenced in other functions as a means of
    appending and removing it's contents from the top bar editor class definition.
    """
    self.layout.menu(TOPBAR_MT_CFBX_set_properties.bl_idname)


def statusbar_info(self, context):
    # TODO properly comment this function

    layout = self.layout

    row = layout.row(align=True)
    row.alignment = 'RIGHT'
    row.scale_x = 8
    # row.split(align=False, factor=0.1)

    if context.view_layer.active_layer_collection.collection.CFBX_settings.should_export:
        row.prop(context.view_layer.active_layer_collection.collection.CFBX_settings,
                 'fbx_folder_path', emboss=True, text="", expand=False, icon="SNAP_VOLUME")
        row.scale_x = 1
        row.operator("hexporter.path_selector", text="",
                     icon='FILE_FOLDER')

    active_collection = context.view_layer.active_layer_collection

    icon_draw_handler = 'ICON_DRAW_HANDLER'

    # create a handler if set to true
    if active_collection.collection.CFBX_settings.should_export:
        # print(str(active_collection.name) + " Is ON")
        # check if a handler does not yet exists
        if not icon_draw_handler in globals():
            # create a new handler
            # print("New handle created for " + str(active_collection.name))
            globals()[icon_draw_handler] = bpy.types.SpaceOutliner.draw_handler_add(
                graphics.draw_callback, (self, context), 'WINDOW', 'POST_PIXEL')
    else:
        # else remove the handler if it existed
        # print(str(active_collection.name) + " Is OFF")
        # check if handler exists
        if icon_draw_handler in globals():
            # print("Handle exists for " + str(active_collection.name))
            bpy.types.SpaceOutliner.draw_handler_remove(
                globals()[icon_draw_handler], 'WINDOW')
            del globals()[icon_draw_handler]


def collection_menu(self, context):
    layout = self.layout
    if bpy.context.view_layer.active_layer_collection.collection.CFBX_settings.should_export:
        layout.operator("wm.cbfx_export_fbx",
                        text="Export Collection", icon='EXPORT')
    layout.prop(bpy.context.view_layer.active_layer_collection.collection.CFBX_settings,
                'should_export', text="CFBX object")
    layout.separator()


def add_menus():
    """This function adds the parent "CFBX" menu item by appending the CFBX_menu()
    function to the top bar editor class definition.
    """
    bpy.types.OUTLINER_MT_collection.prepend(collection_menu)

    # bpy.types.STATUSBAR_HT_header.draw = test
    bpy.types.STATUSBAR_HT_header.append(statusbar_info)

    if not hasattr(bpy.types, TOPBAR_MT_CFBX.bl_idname):
        bpy.utils.register_class(TOPBAR_MT_CFBX)
        bpy.types.TOPBAR_MT_editor_menus.append(cfbx_menu)

    try:
        bpy.types.TOPBAR_MT_CFBX.remove(export_menu)
        bpy.types.TOPBAR_MT_CFBX.remove(properties_menu)

    finally:
        bpy.types.TOPBAR_MT_CFBX.append(export_menu)
        bpy.types.TOPBAR_MT_CFBX.append(properties_menu)


def remove_menus():
    """This function removes the Parent "CFBX" menu item by removing the CFBX_menu() function
    from the top bar editor class definition
    """
    if hasattr(bpy.types, TOPBAR_MT_CFBX.bl_idname):
        bpy.utils.unregister_class(TOPBAR_MT_CFBX)

    bpy.types.TOPBAR_MT_editor_menus.remove(cfbx_menu)

    bpy.types.STATUSBAR_HT_header.remove(statusbar_info)

    bpy.types.OUTLINER_MT_collection.remove(collection_menu)
