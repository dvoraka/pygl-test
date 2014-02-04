#! /usr/bin/env python
# -*- coding: utf-8 -*-

import pyglet

import random
import time
import math

# Pyglet debug
pyglet.options['debug_gl'] = False
from pyglet.gl import *
from pyglet.graphics import *
from pyglet.window import key
from pyglet.window import mouse


class Plane():
    '''Test object.'''

    def __init__(self):

        cobble = pyglet.image.load('dirt12.png')
        self.texture = cobble.get_texture()

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    def draw(self):
        
        self.v_list = vertex_list(
            6,
            ('v3f', (
                0, 0, 0,
                1.0, 0, 0,
                1.0, 1.0, 0,
                0, 0, 0,
                1.0, 1.0, 0,
                0, 1.0, 0
            )),
            ('n3f', (
                0, 0, 1.0,
                0, 0, 1.0,
                0, 0, 1.0,
                0, 0, 1.0,
                0, 0, 1.0,
                0, 0, 1.0
            )),
            ('t2f', (
                0, 0,
                1.0, 0,
                1.0, 1.0,
                0, 0,
                1.0, 1.0,
                0, 1.0
            ))
        )

        glBindTexture(self.texture.target, self.texture.id)
        self.v_list.draw(GL_TRIANGLES)


class Block():

    def __init__(self):
        
        self.num_vertices = None
        self.vertexes = None
        self.normals = None
        self.tcoords = None
        self.v_list = self.init_block()

        # visibility of block
        self.visible = False
        # need to render
        self.render = False

        cobble = pyglet.image.load('dirt12.png')
        self.texture = cobble.get_texture()

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    def init_block(self):
        
        self.num_vertices = 36

        self.vertexes = (
            # front
            0, 0, 0,
            1.0, 0, 0,
            1.0, 1.0, 0,
            0, 0, 0,
            1.0, 1.0, 0,
            0, 1.0, 0,

            # left
            0, 0, 0,
            0, 1.0, 0,
            0, 0, -1.0,
            0, 0, -1.0,
            0, 1.0, 0,
            0, 1.0, -1.0,

            # right
            1.0, 0, 0,
            1.0, 0, -1.0,
            1.0, 1.0, -1.0,
            1.0, 0, 0,
            1.0, 1.0, -1.0,
            1.0, 1.0, 0,

            # top
            0, 1.0, 0,
            1.0, 1.0, 0,
            1.0, 1.0, -1.0,
            0, 1.0, 0,
            1.0, 1.0, -1.0,
            0, 1.0, -1.0,

            # bottom
            0, 0, 0,
            1.0, 0, -1.0,
            1.0, 0, 0,
            0, 0, 0,
            0, 0, -1.0,
            1.0, 0, -1.0,

            # back
            0, 0, -1.0,
            0, 1.0, -1.0,
            1.0, 1.0, -1.0,
            0, 0, -1.0,
            1.0, 1.0, -1.0,
            1.0, 0, -1.0
        )

        self.colors = (
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,

            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,

            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,

            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,

            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,

            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100,
            200, 200, 200, 100
        )

        self.normals = (
            # front
            0, 0, 1.0,
            0, 0, 1.0,
            0, 0, 1.0,
            0, 0, 1.0,
            0, 0, 1.0,
            0, 0, 1.0,

            # left
            -1.0, 0, 0,
            -1.0, 0, 0,
            -1.0, 0, 0,
            -1.0, 0, 0,
            -1.0, 0, 0,
            -1.0, 0, 0,

            # right
            1.0, 0, 0,
            1.0, 0, 0,
            1.0, 0, 0,
            1.0, 0, 0,
            1.0, 0, 0,
            1.0, 0, 0,

            # top
            0, 1.0, 0,
            0, 1.0, 0,
            0, 1.0, 0,
            0, 1.0, 0,
            0, 1.0, 0,
            0, 1.0, 0,

            # bottom
            0, -1.0, 0,
            0, -1.0, 0,
            0, -1.0, 0,
            0, -1.0, 0,
            0, -1.0, 0,
            0, -1.0, 0,

            # back
            0, 0, -1.0,
            0, 0, -1.0,
            0, 0, -1.0,
            0, 0, -1.0,
            0, 0, -1.0,
            0, 0, -1.0
        )

        self.tcoords = (
            # front
            0, 0,
            0.5, 0,
            0.5, 1.0,
            0, 0,
            0.5, 1.0,
            0, 1.0,

            # left
            0.5, 0,
            0.5, 1.0,
            0, 0,
            0, 0,
            0.5, 1.0,
            0, 1.0,
            
            # right
            0, 0,
            0.5, 0,
            0.5, 1.0,
            0, 0,
            0.5, 1.0,
            0, 1.0,
           
            # top
            0.5, 0,
            1.0, 0,
            1.0, 1.0,
            0.5, 0,
            1.0, 1.0,
            0.5, 1.0,
          
            # bottom
            0.5, 1.0,
            0, 0,
            0, 1.0,
            0.5, 1.0,
            0.5, 0,
            0, 0,
 
            # back
            0.5, 0,
            0, 0,
            0, 1.0,
            0.5, 0,
            0, 1.0,
            0.5, 1
        )

        self.v_list = vertex_list(
            36,
            ('v3f/static', self.vertexes),
            ('c4B', self.colors),
            ('n3f/static', self.normals),
            ('t2f/static', self.tcoords),
        )

        return self.v_list

    def get_status(self):
        
        return (
            self.num_vertices,
            None,
            ('v3f', self.vertexes),
            ('n3f', self.normals),
            ('t2f', self.tcoords),
        )

    def print_status(self):
        
        print(self.v_list.colors)

    def draw(self):

        glBindTexture(self.texture.target, self.texture.id)
        self.v_list.draw(GL_TRIANGLES)

    def draw2(self):

        Block.v_list.draw(GL_TRIANGLES)


class BlockWorld():

    def __init__(self, width, height, depth):
 
        self.world_width = width
        self.world_height = height
        self.world_depth = depth
       
        start = time.clock()

        self.batch = None
        self.world = self.init_world(width, height, depth)
        self.check_visibility()

        elapsed = time.clock() - start
        print('Init world: {}'.format(elapsed))

    def init_world(self, width, height, depth):
        
        #self.batch = pyglet.graphics.Batch()

        blocks = {}
        for w in range(width):
            for h in range(height):
                for d in range(depth):

                    if random.randint(0, 4) in (0, 1, 2):

#                        blocks[(w, h, d)] = Block()
#
#                        colors = []
#                        for i in range(6):
#                            for _ in range(6):
#
#                                colors.extend((w, h, d, i))
#
#                        blocks[(w, h, d)].v_list.colors = colors
                        
                        blocks[(w, h, d)] = self.prepare_block((w, h, d))

                       # b_data = blocks[(w, h, d)].get_status()
                       # print(b_data)
                       # self.batch.add(
                       #     b_data[0],
                       #     GL_TRIANGLES,
                       #     b_data[1],
                       #     b_data[2],
                       #     b_data[3],
                       #     b_data[4]
                       # )

                    else:

                        blocks[(w, h, d)] = None

        return blocks

    def check_visibility(self):
        
        all_counter = 0
        none_counter = 0
        vis_counter = 0
        omit_counter = 0

        for w in range(self.world_width):
            for h in range(self.world_height):
                for d in range(self.world_depth):

                    all_counter += 1

                    visibility = False

                    if (w - 1, h, d) in self.world:

                        if self.world[(w - 1, h, d)] is None:

                            visibility = True

                    else:

                        visibility = True

                    if (w + 1, h, d) in self.world:

                        if self.world[(w + 1, h, d)] is None:

                            visibility = True

                    else:

                        visibility = True

                    if (w, h, d + 1) in self.world:

                        if self.world[(w, h, d + 1)] is None:

                            visibility = True

                    else:

                        visibility = True

                    if (w, h, d - 1) in self.world:

                        if self.world[(w, h, d - 1)] is None:

                            visibility = True

                    else:

                        visibility = True

                    if (w, h + 1, d) in self.world:

                        if self.world[(w, h + 1, d)] is None:

                            visibility = True

                    else:

                        visibility = True

                    if (w, h - 1, d) in self.world:

                        if self.world[(w, h - 1, d)] is None:

                            visibility = True

                    else:

                        visibility = True

                    if visibility:

                        block = self.world[(w, h, d)]

                        if block is not None:

                            block.visible = True
                            vis_counter += 1

                        else:

                            omit_counter += 1

        #print('All/Visible/omited: {}/{}/{}'.format(
        #    all_counter, vis_counter, omit_counter))

    def set_render_area(self, pos_x, pos_y, pos_z, size):
        
        render_counter = 0

        # disable all blocks for rendering
        for pos, block in self.world.items():

            if block is not None:

                block.render = False

        center_x = int(pos_x)
        center_y = int(pos_y)
        center_z = int(pos_z)

        start_x = center_x - size / 2
        if start_x < 0:
            start_x = 0

        start_y = center_y - size / 2
        if start_y < 0:
            start_y = 0

        start_z = center_z - size / 2
        if start_z < 0:
            start_z = 0

        end_x = center_x + size / 2
        end_y = center_y + size / 2
        end_z = center_z + size / 2

        for x in range(start_x, end_x):
            for y in range(start_y, end_y):
                for z in range(start_z, end_z):

                    if (x, y, z) in self.world:

                        if self.world[(x, y, z)] is not None:
                            self.world[(x, y, z)].render = True
                            render_counter += 1

        print('Rendering {} objects.'.format(render_counter))

    def collide(self, pos_x, pos_y, pos_z):
        
        x = int(pos_x)
        y = int(pos_y)
        z = int(pos_z) + 1

        if (x, y, z) in self.world:

            if self.world[(x, y, z)] is not None:

#                print(self.world[(x, y, z)])
#                print((x, y, z))
                
                return True

        return False

    def prepare_block(self, position):

        block = Block()

        colors = []
        for i in range(6):
            for _ in range(6):

                colors.extend((
                    position[0],
                    position[1],
                    position[2],
                    i))

        block.v_list.colors = colors

        return block

    def delete(self, position):
        
        self.world[position] = None
        #print('Deleting {}...'.format(position))

    def insert(self, position, id):
        
        if id == 0:

            new_position = list(position)
            new_position[2] += 1

        elif id == 1:

            new_position = list(position)
            new_position[0] -= 1

        elif id == 2:

            new_position = list(position)
            new_position[0] += 1

        elif id == 3:

            new_position = list(position)
            new_position[1] += 1

        elif id == 4:

            new_position = list(position)
            new_position[1] -= 1

        elif id == 5:

            new_position = list(position)
            new_position[2] -= 1

        else:

            print('Not implemented - id: {}'.format(id))
            return

        new_block = self.prepare_block(new_position)
        new_block.visible = True
        self.world[tuple(new_position)] = new_block

    def draw(self):

        for pos, block in self.world.items():

            if block is None:

                continue

            else:

                if block.visible is False:
                
                    #pass
                    continue

                if block.render is False:

                    continue

            glPushMatrix(GL_MODELVIEW)

            glTranslatef(
                float(pos[0]),
                float(pos[1]),
                float(pos[2])
            )
                
            block.draw()
            #self.batch.draw()

            glPopMatrix(GL_MODELVIEW)


class Camera():

    def __init__(self, x, y, z, va, ha):

        self.pos_x = x
        self.pos_y = y
        self.pos_z = z

        self.vert_angle = va
        self.horiz_angle = ha


class GameWindow(pyglet.window.Window):
    
    def __init__(self):
        
        cfg = pyglet.gl.Config(alpha_size=8, depth_size=8)
        #window = pyglet.window.Window(config=config)

        #super(GameWindow, self).__init__(config=cfg, fullscreen=True)
        super(GameWindow, self).__init__(config=cfg)
        
        #print(self.config.get_gl_attributes())

        self.set_caption('GL test')
        self.set_exclusive_mouse(True)

        cursor = self.get_system_mouse_cursor(self.CURSOR_CROSSHAIR)
        self.set_mouse_cursor(cursor)

        self.label = pyglet.text.Label('TEST!')

        self.keyboard = pyglet.window.key.KeyStateHandler()
        self.push_handlers(self.keyboard)

        pyglet.clock.schedule_interval(
            self.update, 1.0 / 30.0)
        pyglet.clock.schedule_interval(
            self.update_render_area, 1.0 / 2.0)
        pyglet.clock.schedule_interval(
            self.update_render_visibility, 1.0 / 2.0)
        pyglet.clock.schedule_interval(
            self.print_fps, 2.0 / 1.0)

        self.fps_display = pyglet.clock.ClockDisplay()

        self.cam = Camera(-10.0, -6.0, -25.0, 0.0, 0.0)

        self.block = Block()
        self.plane = Plane()

        self.world = BlockWorld(20, 4, 60)

        self.setup()

    def setup(self):

        glClearColor(0.8, 0.8, 1.0, 0.0)

        glEnable(GL_DEPTH_TEST)
        #glDepthFunc(GL_LESS)

        glEnable(GL_BLEND)

        glShadeModel(GL_SMOOTH)

        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glEnable(GL_TEXTURE_2D)

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        #glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)

        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    def on_resize(self, width, height):

        print('on resize')

        if height == 0:
            height = 1

        # specify viewport
        glViewport(0, 0, width, height)

        # load perspective projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(70, 1.0 * width / height, 0.01, 300.0)
        #glLoadIdentity()

        # light parameters
        def vec(*args):
                return (GLfloat * len(args))(*args)
        glLightfv(GL_LIGHT0, GL_POSITION, vec(10.0, 10.0, 5.0, 1.0))
        glLightfv(GL_LIGHT0, GL_AMBIENT, vec(0.7, 0.7, 0.7, 1.0))
        glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(0.4, 0.4, 0.4, 1.0))
        glMaterialfv(GL_FRONT, GL_DIFFUSE, vec(0.5, 0.5, 0.5, 1.0))
        glMaterialfv(GL_FRONT, GL_SPECULAR, vec(0.5, 0.5, 0.5, 1.0))
        glMaterialfv(GL_FRONT, GL_SHININESS, vec(1.0))

    def on_draw(self):
        
        self.clear()

        # Clear buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # set camera
        glRotatef(self.cam.horiz_angle, 1.0, 0, 0)
        glRotatef(self.cam.vert_angle, 0.0, 1.0, 0)
        glTranslatef(self.cam.pos_x, self.cam.pos_y, self.cam.pos_z)

        self.world.draw()

#        # draw 2D stuff
#        self.set2d()
#
#        #self.label.draw()
#        self.fps_display.draw()
#
#        self.unset2d()

    def set2d(self):

#        glDisable(GL_DEPTH_TEST)
#        glDisable(GL_LIGHTING)

        #glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # store the projection matrix to restore later
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()

        # load orthographic projection matrix
        glLoadIdentity()
        #glOrtho(0, float(self.width),0, float(self.height), 0, 1)
        far = 8192
        glOrtho(
            -self.width / 2.,
            self.width / 2.,
            -self.height / 2.,
            self.height / 2., 0,
            far)

        # reset modelview
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        #glClear(GL_COLOR_BUFFER_BIT)

    def unset2d(self):

#        glEnable(GL_DEPTH_TEST)
#        glEnable(GL_LIGHTING)

        # load back the projection matrix saved before
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()

    def on_mouse_press(self, x, y, button, modifiers):

        a = (4 * GLubyte)()
        glReadPixels(x, y, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, a)
        #print('Before: ({}, {}, {})'.format(a[0], a[1], a[2]))

        glDisable(GL_LIGHTING)
        glDisable(GL_TEXTURE_2D)

        self.on_draw()

        a = (4 * GLubyte)()
        glReadPixels(x, y, 1, 1, GL_RGBA, GL_UNSIGNED_BYTE, a)
        #print('After: ({}, {}, {}, {})'.format(a[0], a[1], a[2], a[3]))

        glEnable(GL_LIGHTING)
        glEnable(GL_TEXTURE_2D)

        self.on_draw()

        if button == mouse.LEFT:

            self.world.delete((a[0], a[1], a[2]))

        elif button == mouse.RIGHT:
            
            self.world.insert((a[0], a[1], a[2]), a[3])

    def on_mouse_motion(self, x, y, dx, dy):

        self.cam.horiz_angle -= float(dy)
        self.cam.vert_angle += float(dx)

    def select_test(self):
        
        pass

    def print_fps(self, dt):

        print(pyglet.clock.get_fps())

    def update_render_visibility(self, dt):
        
        self.world.check_visibility()

    def update_render_area(self, dt):
 
        self.world.set_render_area(
            - self.cam.pos_x,
            - self.cam.pos_y,
            - self.cam.pos_z,
            12
        )

    def update(self, dt):
       
        new_y = self.cam.pos_y + 0.9
        if self.world.collide(- self.cam.pos_x, - new_y, - self.cam.pos_z):

            #print('Collide')
            pass

        else:
            
            self.cam.pos_y += 0.1

        if self.keyboard[key.UP]:

            #print('UP')
            #self.cam.pos_z += 0.4
            y_a = math.radians(self.cam.vert_angle)

            new_z = self.cam.pos_z + 0.1 * math.cos(y_a)
            new_x = self.cam.pos_x - 0.1 * math.sin(y_a)

            if self.world.collide(- new_x, - self.cam.pos_y, - new_z):

                #print('Collide')
                pass

            else:
            
                self.cam.pos_z += 0.05 * math.cos(y_a)
                self.cam.pos_x -= 0.05 * math.sin(y_a)

           # print('Collide: {}'.format(self.world.collide(
           #     - self.cam.pos_x,
           #     - self.cam.pos_y,
           #     - self.cam.pos_z
           # )))

        elif self.keyboard[key.DOWN]:

            #print('DOWN')
            self.cam.pos_z -= 0.4

        if self.keyboard[key.LEFT]:

            #print('LEFT')
            self.cam.pos_x += 0.4

        elif self.keyboard[key.RIGHT]:

            #print('RIGHT')
            self.cam.pos_x -= 0.4

        if self.keyboard[key.PAGEUP]:

            #print('PUP')
            self.cam.pos_y -= 0.4

        elif self.keyboard[key.PAGEDOWN]:

            #print('PDOWN')
            self.cam.pos_y += 0.4

        if self.keyboard[key.L]:

            #print('L')
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        if self.keyboard[key.F]:

            #print('F')
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        if self.keyboard[key.P]:

            #NOTE: broken
            #pyglet.image.get_buffer_manager() \
            #    .get_color_buffer() \
            #    .save('screenshot.png')
            #time.sleep(0.3)
            pass

        if self.keyboard[key.NUM_1]:

            time.sleep(0.2)

            if glIsEnabled(GL_LIGHTING):

                glDisable(GL_LIGHTING)
                print('Lighting disabled')

            else:

                glEnable(GL_LIGHTING)
                print('Lighting enabled')

        elif self.keyboard[key.NUM_2]:

            time.sleep(0.2)

            if glIsEnabled(GL_TEXTURE_2D):

                glDisable(GL_TEXTURE_2D)
                print('Texturing disabled')

            else:

                glEnable(GL_TEXTURE_2D)
                print('Texturing enabled')

        elif self.keyboard[key.NUM_3]:

            time.sleep(0.2)

            x = GLint()
            glGetIntegerv(GL_SHADE_MODEL, x)
            if x.value == GL_SMOOTH:

                glShadeModel(GL_FLAT)
                print('Flat shading')

            else:

                glShadeModel(GL_SMOOTH)
                print('Smooth shading')


if __name__ == '__main__':

    window = GameWindow()
    pyglet.app.run()
