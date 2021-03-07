# Copyright UHX, No rights reserved.
# https: //www.blender.org/about/license/

import bpy
import os
from . import graphics

import blf
import bgl


def get_current_context():
    """
    This function gets the current context of the scene and its objects.
    """

    # find all selected objects in current context and append name to object
    selected_objects = []
    for selected_object in bpy.context.selected_objects:

        active_action_name = ''
        # get the selected objcets active animation
        if selected_object.animation_data:
            if selected_object.animation_data.action:
                active_action_name = selected_object.animation_data.action.name

        selected_objects.append([selected_object.name, active_action_name])

    # create current_context object and add data to the fields
    current_context = {
        'visible_objects': [visible_object.name for visible_object in bpy.context.visible_objects],
        'selected_objects': selected_objects,
        'mode': bpy.context.mode
    }

    # add the current active object if there is one
    active_object = bpy.context.active_object
    if active_object:
        current_context['active_object'] = active_object.name

    return current_context


def set_context(context):
    """
    This function sets the current context of the scene and its objects.
    """

    # set the selected objects
    for visible_object_name in context['visible_objects']:
        visible_object = bpy.data.objects.get(visible_object_name)
        if visible_object:
            visible_object.hide_set(False)

    # set the selected objects
    for scene_object_name, active_action_name in context['selected_objects']:
        scene_object = bpy.data.objects.get(scene_object_name)
        if scene_object:
            scene_object.select_set(True)

    # set the active object
    active_object_name = context.get('active_object')
    if active_object_name:
        bpy.context.view_layer.objects.active = bpy.data.objects.get(
            active_object_name)

    # set the mode
    if bpy.context.mode != context['mode']:
        # mode context can be read as 'EDIT_ARMATURE' or 'EDIT_MESH', however only 'EDIT' can be set, so this clean up anything with EDIT in the text to be just 'EDIT'
        if 'EDIT' in context['mode']:
            context['mode'] = 'EDIT'

        bpy.ops.objects.mode_set(mode=context['mode'])


def report_error(message):
    """
    This function reports a given error message to the screen.

    :param str message: The error message to display to the user.
    """
    if not os.environ.get('DEV'):
        # parse runtime error messages
        if 'RuntimeError: ' in message:
            message = message.split('RuntimeError: ')[-1][:-1]

        bpy.context.window_manager.UHXporter.error_message = message
        bpy.context.window_manager.popup_menu(
            draw_error_message, title="Error", icon='ERROR')
    else:
        raise RuntimeError(message)


def report_warning(message):
    """
    This function reports a given error message to the screen.

    :param str message: The error message to display to the user.
    """
    if not os.environ.get('DEV'):
        # parse runtime error messages
        if 'RuntimeError: ' in message:
            message = message.split('RuntimeError: ')[-1][:-1]

        bpy.context.window_manager.UHXporter.error_message = message
        bpy.context.window_manager.popup_menu(
            draw_error_message, title="Warning", icon='ERROR')
    else:
        raise RuntimeError(message)


def draw_error_message(self, context):
    """
    This function creates the layout for the error pop up

    :param object self: This refers the the Menu class definition that this function will
    be appended to.
    :param object context: This parameter will take the current blender context by default,
    or can be passed an explicit context.
    """
    self.layout.label(text=bpy.context.window_manager.UHXporter.error_message)
