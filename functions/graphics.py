# Copyright PORTALSURFER, No rights reserved.
# https: //www.blender.org/about/license/

import gpu
import bpy
from gpu_extras.batch import batch_for_shader
from . import graphics


def get_outliner_width():
    for area in bpy.context.screen.areas:
        if area.type == 'OUTLINER':
            return area.width


def draw_callback(self, context):
    margin = get_outliner_width() / 4
    height = 5
    start = margin
    end = get_outliner_width() - margin

    vertices = (
        (start, 0), (end, 0),
        (start, height), (end, height))

    indices = (
        (0, 1, 2), (2, 1, 3))

    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(
        shader, 'TRIS', {"pos": vertices}, indices=indices)

    shader.bind()
    shader.uniform_float("color", (1, 0.5, 0.5, 1.0))
    batch.draw(shader)


def remove_draw_handler(draw_handler):
    bpy.types.SpaceOutliner.draw_handler_remove(draw_handler, 'WINDOW')


def init(self, context):
    print("intialize")
    self.initialized = True
    args = (self, context)

    if self.draw_handler:
        bpy.types.SpaceOutliner.remove_draw_handler(
            self.draw_handler, 'WINDOW')

    self.draw_handler = bpy.types.SpaceOutliner.draw_handler_add(
        draw_callback, (self, context), 'WINDOW', 'POST_PIXEL')


class DrawingClass:
    def __init__(self, context):
        self.shader = shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
        self.handle = bpy.types.SpaceOutliner.draw_handler_add(
            self.draw_callback, (context, ), 'WINDOW', 'POST_PIXEL')

    def draw_callback(self, context):

        batch = batch_for_shader(
            self.shader, 'TRIS', {"pos": vertices}, indices=indices)

        self.shader.bind()
        self.shader.uniform_float("color", (1, 0.5, 0.5, 1.0))
        print("draw")
        batch.draw(self.shader)

    def remove_handle(self):
        bpy.types.SpaceOutliner.draw_handler_remove(self.handle, 'WINDOW')
