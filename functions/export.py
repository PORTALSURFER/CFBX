# Copyright SURFER, No rights reserved.
# https: //www.blender.org/about/license/

import bpy
import mathutils
from . import utilities
from . import join


def find_export_center(context):
    # if context.active_object in context.selected_objects:
    return context.active_object.location
    # else:
    # utilities.report_warning(
    #     f'No active selected object found, cursor position used as center instead')
    # return context.scene.cursor.location


def create_export_buffer(context):
    # TODO this does not yet support Collections inside
    # TODO currently will create a buffer even when there are no objects to add to it
    export_collection = None
    # check if an export buffer exists, if so, delete it.
    export_collection_name = 'CFBX Export Buffer'

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

    export_data['PATH'] = context.view_layer.active_layer_collection.collection.CFBX_settings.fbx_folder_path

    export_data['NAME'] = context.view_layer.active_layer_collection.collection.name

    export_collection = create_export_buffer(context)
    if not export_collection:
        utilities.report_error(
            f"Creation of export buffer failed \nExport failed!")
        return

    export_data['COLLECTION'] = export_collection

    # Fill export collection with the right objects
    # also names the objects so they can be found easily in Blender
    source_collection = context.view_layer.active_layer_collection.collection
    export_objects = []
    # source_objects = source_collection_root

    # source_collections = []
    # source_collections.append(source_collection_root)
    # get_collection_children(source_collection_root, source_collections)

    # bpy.ops.object.select_all(action='DESELECT')

    instance_collision_objects = []
    mesh_objects = []
    curve_objects = []

    instance_collection_override = None

    override = context.copy()

    source_objects = {'MESH': [], 'EMPTY': [],
                      'COLLECTION_INSTANCE': [], 'CURVE': []}
    # grab all the objects
    # print("..Grabbing source objects..")
    get_all_real_objects(self, context, source_collection, source_objects)

    # for collection_instance_object in source_objects['COLLECTION_INSTANCE']:
    #     for obj in collection_instance_object.instance_collection.all_objects:
    #         print(obj.name)

    for mesh_object in source_objects['MESH']:
        # print("source_object : " + mesh_object.name)
        # export_object = mesh_object.copy()
        # export_object.data = mesh_object.data.copy()
        # export_object.name = "CFBX_MESH | " + mesh_object.name

        export_collection.objects.link(mesh_object)
        mesh_object.select_set(True)

    join_objects_count = len(source_objects['MESH'])
    host_object = source_objects['MESH'][join_objects_count - 1]
    print("HOST | " + host_object.name)
    for i in range(join_objects_count - 1):
        # print(source_objects['MESH'][i])
        join.join_objects(source_objects['MESH'][i], host_object)

    # for obj in source_objects['MESH']:

    # print(obj)
    # obj_copy.data = obj.data.copy()
    # export_collection.objects.link(obj_copy)

    # for src_obj in bpy.data.objects:
    #     for obj_collection in src_obj.users_collection:
    #         # print(obj_collection.name)
    #         for collection in source_collections:
    #             if collection.name == obj_collection.name:
    #                 # print(src_obj.name)
    #                 if src_obj.type == 'MESH':
    #                     obj_copy = src_obj.copy()
    #                     obj_copy.data = src_obj.data.copy()
    #                     export_objects.append(obj_copy)
    #                     obj_copy.name = "CFBX_MESH"
    #                     export_collection.objects.link(obj_copy)
    #                     obj_copy.select_set(True)

    #                     # # attempting to apply modifiers
    #                     # # mesh_objects.append(obj_copy)
    #                     # override = context.copy()
    #                     # override['selected_objects'] = obj_copy
    #                     # override['active_object'] = obj_copy
    #                     # # override['object'] = mesh_objects[0]
    #                     # # override['selected_editable_objects'] = mesh_objects
    #                     # # bpy.ops.object.convert(override, target='MESH')
    #                     # bpy.ops.object.convert(override, target='MESH')

    #                 elif src_obj.type == 'EMPTY' and src_obj.instance_type == 'COLLECTION':
    #                     obj_copy = src_obj.copy()
    #                     obj_copy.instance_collection = src_obj.instance_collection
    #                     obj_copy.name = "CFBX_COL_INSTANCE"
    #                     export_collection.objects.link(obj_copy)

    #                     instance_collision_objects.append(obj_copy)
    #                     instance_collection_override = context.copy()
    #                     instance_collection_override['selected_objects'] = instance_collision_objects
    #                     instance_collection_override['active_object'] = instance_collision_objects[0]
    #                     instance_collection_override['object'] = instance_collision_objects[0]
    #                     instance_collection_override['selected_editable_objects'] = instance_collision_objects

    #                     bpy.ops.object.duplicates_make_real(
    #                         instance_collection_override)

    #                     bpy.data.objects.remove(obj_copy)
    #                 elif src_obj.type == 'CURVE':
    #                     obj_copy = src_obj.copy()
    #                     obj_copy.data = src_obj.data.copy()
    #                     obj_copy.name = "CFBX_CURVE"
    #                     export_collection.objects.link(obj_copy)
    #                     obj_copy.select_set(True)

    #                     # # curve_objects.append(obj_copy)
    #                     # override = context.copy()
    #                     # override['selected_objects'] = obj_copy
    #                     # override['active_object'] = obj_copy
    #                     # override['object'] = obj_copy
    #                     # override['selected_editable_objects'] = obj_copy

    #                     # print(obj_copy.name)

    # combine all objects
    # # join objects

    # context.view_layer.objects.active = export_objects[0]

    # bpy.ops.object.convert(target='MESH')
    # bpy.ops.object.join()

    export_data['OBJECT'] = context.view_layer.objects.active

    return export_data


def copy_and_prepare_source_object(self, context, obj, offset, source_objects):
    depsgraph = context.evaluated_depsgraph_get()
    eval_obj = obj.evaluated_get(depsgraph)

    new_obj = bpy.data.objects.new("CFBX_"+obj.type+" | " + obj.name,
                                   bpy.data.meshes.new_from_object(eval_obj))

    # new_obj.data.transform = obj.data.transform
    new_obj.location = obj.location
    new_obj.rotation_euler = obj.rotation_euler
    new_obj.scale = obj.scale

    # apply transforms to mesh
    wmx = obj.matrix_world
    new_obj.data.transform(wmx)

    # zero out at object level
    new_obj.matrix_world = mathutils.Matrix()

    if offset:
        new_obj.location += offset

    source_objects['MESH'].append(new_obj)


def get_all_real_objects(self, context, source_collection, source_objects, offset=None):
    for obj in source_collection.all_objects:
        if obj.type in ['MESH', 'CURVE']:
            copy_and_prepare_source_object(
                self, context, obj, offset, source_objects)
        elif obj.type == 'EMPTY':
            if obj.instance_type == 'COLLECTION':
                # collection found, so dive deeper
                # print("__ Diving into COLLECTION_INSTANCE : " +
                #   obj.name + " with offset : " + str(offset))
                offset = obj.location
                get_all_real_objects(self, context,
                                     obj.instance_collection, source_objects, offset)
            else:
                copy_and_prepare_source_object(self, context,
                                               'EMPTY', obj, offset, source_objects)
        elif obj.type == 'CURVE':
            copy_and_prepare_source_object(self, context,
                                           'CURVE', obj, offset, source_objects)


def export(self, context):
    """
    This function export
    """
    print("\n RUNNING CFBX...")
    # print(bpy.path.abspath("/test/"))
    export_data = prep_data(self, context)
    return

    set_active_collection(context, export_data['COLLECTION'])

    move_active_center_to_location(context, export_data['CENTER'])

    # TODO this is moving the wrong object to the center
    # move_object_to_origin(export_data['OBJECT'])

    export_path = get_export_path(self, context, export_data)
    try:
        export_fbx_file(export_path)
    except:
        utilities.report_error(f"Failed to export, please check path")


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


def get_export_path(self, context, export_data):
    name = export_data['NAME']
    path = export_data['PATH']

    return path + name


def export_fbx_file(file_path):
    """
    This function calls the blender export operator with specific properties
    """
    bpy.ops.export_scene.fbx(
        filepath=file_path + ".fbx",
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
