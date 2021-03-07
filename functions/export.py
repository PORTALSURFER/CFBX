# Copyright SURFER, No rights reserved.
# https: //www.blender.org/about/license/

import bpy
from . import utilities


def find_export_center(context):
    if context.active_object in context.selected_objects:
        return context.active_object.location
    else:
        utilities.report_warning(
            f'No active selected object found, cursor position used as center instead')
        return context.scene.cursor.location


def create_export_buffer(context):
    # TODO this does not yet support Collections inside
    # TODO currently will create a buffer even when there are no objects to add to it
    export_collection = None
    # check if an export buffer exists, if so, delete it.
    export_collection_name = 'CFBX Export Buffer'
    export_collection = None

    # if the buffer does not exist create it
    if not export_collection_name in [collection.name for collection in bpy.data.collections]:

        # create a new collection to be used as the buffer and link it to the current scene
        export_collection = bpy.data.collections.new(export_collection_name)
        context.scene.collection.children.link(export_collection)

    else:  # if it does exist, remove it and everything inside it

        # grab the collection
        for collection in bpy.data.collections:
            if collection.name == export_collection_name:
                export_collection = collection

        for obj in export_collection.objects:
            bpy.data.objects.remove(obj)

    return export_collection


def get_collection_children(root_collection, collection_children):
    children = (child for child in root_collection.children)
    for child in children:
        collection_children.append(child)
        get_collection_children(child, collection_children)
    return


def prep_data(self, context):
    # TODO put this in a dict
    # get a location to use as center
    export_data = dict()

    export_data['CENTER'] = export_center = find_export_center(context)

    export_collection = create_export_buffer(context)
    if not export_collection:
        utilities.report_error(
            f"Creation of export buffer failed \nExport failed!")
        return

    export_data['COLLECTION'] = export_collection

    # Fill export collection with the right objects
    # also names the objects so they can be found easily in Blender
    source_collection_root = context.view_layer.active_layer_collection
    export_objects = []
    source_objects = source_collection_root

    source_collections = []
    source_collections.append(source_collection_root)
    get_collection_children(source_collection_root, source_collections)

    bpy.ops.object.select_all(action='DESELECT')

    for src_obj in bpy.data.objects:
        for obj_collection in src_obj.users_collection:
            # print(obj_collection.name)
            for collection in source_collections:
                if collection.name == obj_collection.name:
                    # print(src_obj.name)
                    obj_copy = src_obj.copy()
                    obj_copy.data = src_obj.data.copy()
                    export_objects.append(obj_copy)
                    obj_copy.name = "CFBX_object"
                    export_collection.objects.link(obj_copy)
                    obj_copy.select_set(True)

    # combine all objects
    # # join objects

    context.view_layer.objects.active = export_objects[0]
    bpy.ops.object.join()

    export_data['OBJECT'] = context.view_layer.objects.active

    return export_data


def export(self, context):
    """
    This function export
    """
    print("\n RUNNING CFBX...")
    export_data = prep_data(self, context)

    set_active_collection(context, export_data['COLLECTION'])

    move_active_center_to_location(context, export_data['CENTER'])

    move_object_to_origin(export_data['OBJECT'])

    export_fbx_file()


def set_active_collection(context, collection):
    for layer_collection in context.view_layer.layer_collection.children:
        if layer_collection.name == collection.name:
            context.view_layer.active_layer_collection = layer_collection


def move_active_center_to_location(context, location):
    # moves center based on 3d cursor
    # TODO find a better way at some point
    old_cursor_location = context.scene.cursor.location.copy()
    context.scene.cursor.location = location
    bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')

    # reset cursor locaction to old location
    context.scene.cursor.location = old_cursor_location


def move_object_to_origin(obj):
    obj.location.x = 0
    obj.location.y = 0
    obj.location.z = 0


def export_fbx_file():
    """
    This function calls the blender export operator with specific properties
    """
    file_path = "C:/Users/wsvas/OneDrive/Documents/temp/"
    name = "test"
    bpy.ops.export_scene.fbx(
        filepath=file_path + name + ".fbx",
        use_selection=True,
        bake_anim_use_nla_strips=True,
        bake_anim_use_all_actions=False,
        object_types={'ARMATURE', 'MESH', 'EMPTY'},
        use_active_collection=True,

        use_custom_props=False,
        # use_custom_props=properties.use_custom_props,

        global_scale=1.0,
        # global_scale=properties.global_scale,

        apply_scale_options='FBX_SCALE_NONE',
        # apply_scale_options=properties.apply_scale_options,

        axis_forward='-Z',
        # axis_forward=properties.axis_forward,

        axis_up='Y',
        # axis_up=properties.axis_up,

        apply_unit_scale=True,
        # apply_unit_scale=properties.apply_unit_scale,

        bake_space_transform=True,
        # bake_space_transform=properties.bake_space_transform,

        mesh_smooth_type='FACE',
        # mesh_smooth_type=properties.mesh_smooth_type,

        use_subsurf=False,
        # use_subsurf=properties.use_subsurf,

        use_mesh_modifiers=True,
        # use_mesh_modifiers=properties.use_mesh_modifiers,

        use_mesh_edges=False,
        # use_mesh_edges=properties.use_mesh_edges,

        use_tspace=False,
        # use_tspace=properties.use_tspace,

        primary_bone_axis='Y',
        # primary_bone_axis=properties.primary_bone_axis,

        secondary_bone_axis='X',
        # secondary_bone_axis=properties.secondary_bone_axis,

        armature_nodetype='NULL',
        # armature_nodetype=properties.armature_nodetype,

        use_armature_deform_only=False,
        # use_armature_deform_only=properties.use_armature_deform_only,

        add_leaf_bones=True,
        # add_leaf_bones=properties.add_leaf_bones,

        bake_anim=True,
        # bake_anim=properties.bake_anim,

        bake_anim_use_all_bones=True,
        # bake_anim_use_all_bones=properties.bake_anim_use_all_bones,

        bake_anim_force_startend_keying=True,
        # bake_anim_force_startend_keying=properties.bake_anim_force_startend_keying,

        bake_anim_step=1.0,
        # bake_anim_step=properties.bake_anim_step,

        bake_anim_simplify_factor=1.0,
        # bake_anim_simplify_factor=properties.bake_anim_simplify_factor,

        use_metadata=True,
        # use_metadata=properties.use_metadata
    )
