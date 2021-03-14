# Copyright PORTALSURFER, No rights reserved.
# https: //www.blender.org/about/license/

import bpy
from .functions import utilities, graphics


class CFBXProperties:
    """
    This class holds the variables for the addon.
    """
    module_name = __package__

    error_message: bpy.props.StringProperty(default='')


class CFBXUIProperties:
    """
    This class holds the UI variables for the addon
    """
    # import dialog interface properties

    # addon preferences user interface properties
    options_type: bpy.props.EnumProperty(
        items=[
            ('paths', 'Paths', '', '', 0),
            ('extras', 'Extras' '', '', 1)
        ],
        default="paths",
        description="Select which preferences you want to edit"
    )
    path_mode: bpy.props.EnumProperty(
        name='Path Mode',
        items=[
            ('send_to_unreal', 'Send to Unreal', '', '', 0),
            ('export_to_disk', 'Export to Disk', '', '', 1),
            ('both', 'Both', '', '', 2)
        ],
        default='send_to_unreal',
        description="Select which type of paths you want to export to"
    )


class CFBXWindowManagerPropertyGroup(bpy.types.PropertyGroup, CFBXProperties):
    """
    This class defines a property group that stores constants in the window manager context.
    """


class CFBXCollectionProperties:
    """
    This class holds the variables for the Collections
    """

    # export_path = "/"

    should_export: bpy.props.BoolProperty(
        default=False,
        # update=graphics.export_toggle,
    )
    export_name_prefix: bpy.props.StringProperty(
        name='Prefix to add to the  export name',
        description="Export Name Prefix",
    )
    fbx_folder_path: bpy.props.StringProperty(
        name="FBX Export Path",
        default=bpy.path.abspath("/"),
        # update=utilities.auto_format_unreal_mesh_folder_path,
        description=("This is the mesh export path.")
    )
    icon_draw_handle: bpy.props.IntProperty(default=0)


class CFBXCollectionPropertyGroup(bpy.types.PropertyGroup, CFBXCollectionProperties):
    """
    This class defines a property group that stores constants in the window manager context.
    """


def register():
    """
    This function registers the property group class and adds it to the
    window manager context when the addon is enabled.
    """
    bpy.utils.register_class(CFBXWindowManagerPropertyGroup)
    bpy.utils.register_class(CFBXCollectionPropertyGroup)

    bpy.types.WindowManager.CFBX = bpy.props.PointerProperty(
        type=CFBXWindowManagerPropertyGroup)

    bpy.types.Collection.CFBX_settings = bpy.props.PointerProperty(
        type=CFBXCollectionPropertyGroup,
        name="CFBX Settings"
    )


def unregister():
    """
    This function unregisters the property group class and deletes it from the window manager context when
    the addon is disabled.
    """
    bpy.utils.unregister_class(CFBXCollectionPropertyGroup)
    bpy.utils.unregister_class(CFBXWindowManagerPropertyGroup)

    del bpy.types.Collection.CFBX_settings
    del bpy.types.WindowManager.CFBX
