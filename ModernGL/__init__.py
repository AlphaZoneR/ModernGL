'''
    ModernGL: PyOpenGL alternative
'''

# pylint: disable=C0123, W0212

import os
from typing import Dict, Tuple

if os.environ.get('READTHEDOCS') != 'True':
    from . import mgl

else:
    from .mock import mgl

__version__ = '4.2.0'

__all__ = [
    'Error',
    'NOTHING', 'BLEND', 'DEPTH_TEST', 'CULL_FACE',
    'Primitive',
    'TRIANGLES', 'TRIANGLE_STRIP', 'TRIANGLE_FAN', 'LINES', 'LINE_STRIP', 'LINE_LOOP', 'POINTS',
    'LINE_STRIP_ADJACENCY', 'LINES_ADJACENCY', 'TRIANGLE_STRIP_ADJACENCY', 'TRIANGLES_ADJACENCY',
    'TextureFilter',
    'LINEAR', 'NEAREST', 'LINEAR_MIPMAP', 'NEAREST_MIPMAP',
    'Buffer',
    'Attribute', 'Uniform', 'UniformBlock', 'Varying',
    'Texture', 'Texture3D', 'TextureCube',
    'Renderbuffer',
    'Shader',
    'Program',
    'VertexArray',
    'ComputeShader',
    'Framebuffer',
    'Context',
    'create_context',
    'create_standalone_context',
    'detect_format',
    'depth_func',
    'blend_func'
]

GL_ZERO = 0x0000

GL_ONE = 0x0001

GL_SRC_COLOR = 0x0300

GL_ONE_MINUS_SRC_COLOR = 0x0301

GL_DST_COLOR = 0x0306

GL_ONE_MINUS_DST_COLOR = 0x0307

GL_SRC_ALPHA = 0x0302

GL_ONE_MINUS_SRC_ALPHA = 0x0303

GL_DST_ALPHA = 0x0304

GL_ONE_MINUS_DST_ALPHA = 0x0305

default_blending = (GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
premultiplied_alpha = (GL_SRC_ALPHA, GL_ONE)

class Error(Exception):
    '''
        ModernGL Error
    '''

    filename = None
    function = None
    line = None


mgl.set_error_class(Error)


NOTHING = 0
'''
    Nothing
'''

BLEND = 1
'''
    Blending
'''

DEPTH_TEST = 2
'''
    Depth Test
'''

CULL_FACE = 4
'''
    Face Culling
'''


class Primitive:
    '''
        Primitive
    '''

    __slots__ = ['mglo', 'name']

    @staticmethod
    def new(obj, name) -> 'Primitive':
        '''
            For internal use only.
        '''

        res = Primitive.__new__(Primitive)
        obj.wrapper = res
        res.name = name
        res.mglo = obj
        return res

    def __init__(self):
        self.name = None
        self.mglo = None
        raise TypeError()

    def __repr__(self):
        return 'ModernGL.%s' % self.name

    def __eq__(self, other):
        return type(self) is type(other) and self.mglo is other.mglo


TRIANGLES = Primitive.new(mgl.TRIANGLES, 'TRIANGLES')
'''
    GL_TRIANGLES
'''

TRIANGLE_STRIP = Primitive.new(mgl.TRIANGLE_STRIP, 'TRIANGLE_STRIP')
'''
    GL_TRIANGLE_STRIP
'''

TRIANGLE_FAN = Primitive.new(mgl.TRIANGLE_FAN, 'TRIANGLE_FAN')
'''
    GL_TRIANGLE_FAN
'''

LINES = Primitive.new(mgl.LINES, 'LINES')
'''
    GL_LINES
'''

LINE_STRIP = Primitive.new(mgl.LINE_STRIP, 'LINE_STRIP')
'''
    GL_LINE_STRIP
'''

LINE_LOOP = Primitive.new(mgl.LINE_LOOP, 'LINE_LOOP')
'''
    GL_LINE_LOOP
'''

POINTS = Primitive.new(mgl.POINTS, 'POINTS')
'''
    GL_POINTS
'''

LINE_STRIP_ADJACENCY = Primitive.new(mgl.LINE_STRIP_ADJACENCY, 'LINE_STRIP_ADJACENCY')
'''
    GL_LINE_STRIP_ADJACENCY
'''

LINES_ADJACENCY = Primitive.new(mgl.LINES_ADJACENCY, 'LINES_ADJACENCY')
'''
    GL_LINES_ADJACENCY
'''

TRIANGLE_STRIP_ADJACENCY = Primitive.new(mgl.TRIANGLE_STRIP_ADJACENCY, 'TRIANGLE_STRIP_ADJACENCY')
'''
    GL_TRIANGLE_STRIP_ADJACENCY
'''

TRIANGLES_ADJACENCY = Primitive.new(mgl.TRIANGLES_ADJACENCY, 'TRIANGLES_ADJACENCY')
'''
    GL_TRIANGLES_ADJACENCY
'''


class TextureFilter:
    '''
        TextureFilter
    '''

    __slots__ = ['mglo', 'name']

    @staticmethod
    def new(obj, name) -> 'TextureFilter':
        '''
            For internal use only.
        '''

        res = TextureFilter.__new__(TextureFilter)
        obj.wrapper = res
        res.name = name
        res.mglo = obj
        return res

    def __init__(self):
        self.name = None
        self.mglo = None
        raise TypeError()

    def __repr__(self):
        return 'ModernGL.%s' % self.name

    def __eq__(self, other):
        return type(self) is type(other) and self.mglo is other.mglo


LINEAR = TextureFilter.new(mgl.LINEAR, 'LINEAR')
'''
    (GL_LINEAR, GL_LINEAR)
'''

NEAREST = TextureFilter.new(mgl.NEAREST, 'NEAREST')
'''
    (GL_NEAREST, GL_NEAREST)
'''

LINEAR_MIPMAP = TextureFilter.new(mgl.LINEAR_MIPMAP, 'LINEAR_MIPMAP')
'''
    (GL_LINEAR_MIPMAP_LINEAR, GL_LINEAR)
'''

NEAREST_MIPMAP = TextureFilter.new(mgl.NEAREST_MIPMAP, 'NEAREST_MIPMAP')
'''
    (GL_NEAREST_MIPMAP_LINEAR, GL_NEAREST)
'''


class Buffer:
    '''
        Buffer objects are OpenGL objects that store an array of unformatted memory
        allocated by the OpenGL context, (data allocated on the GPU).
        These can be used to store vertex data, pixel data retrieved from images
        or the framebuffer, and a variety of other things.

        A Buffer object cannot be instantiated directly, it requires a context.
        Use :py:meth:`Context.buffer` to create one.

        Copy buffer content using :py:meth:`Context.copy_buffer`.
    '''

    __slots__ = ['mglo', '_size', '_dynamic', '_glo']

    def __init__(self):
        self.mglo = None
        self._size = None
        self._dynamic = None
        self._glo = None
        raise TypeError()

    def __repr__(self):
        return '<Buffer: %d>' % self.glo

    def __eq__(self, other):
        return type(self) is type(other) and self.mglo is other.mglo

    @property
    def size(self) -> int:
        '''
            int: The size of the buffer.
        '''

        return self._size

    @property
    def dynamic(self) -> bool:
        '''
            bool: Is the buffer created with the dynamic flag?
        '''

        return self._dynamic

    @property
    def glo(self) -> int:
        '''
            int: The internal OpenGL object.
            This values is provided for debug purposes only.
        '''

        return self._glo

    def write(self, data, *, offset=0) -> None:
        '''
            Write the content.

            Args:
                data (bytes): The data.

            Keyword Args:
                offset (int): The offset.
        '''

        self.mglo.write(data, offset)

    def write_chunks(self, data, start, step, count) -> None:
        '''
            Split `data` to `count` equal parts.
            Write the chunks using offsets calculated from `start`, `step` and `stop`.

            Args:
                data (bytes): The data.
                start (int): First offset.
                step (int): Offset increment.
                count (int): The number of offsets.
        '''

        self.mglo.write_chunks(data, start, step, count)

    def read(self, size=-1, *, offset=0) -> bytes:
        '''
            Read the content.

            Args:
                size (int): The size. Value ``-1`` means all.

            Keyword Args:
                offset (int): The offset.

            Returns:
                bytes: The content of the buffer.
        '''

        return self.mglo.read(size, offset)

    def read_into(self, buffer, size=-1, *, offset=0, write_offset=0) -> None:
        '''
            Read the content into a buffer.

            Args:
                buffer (bytarray): The buffer that will receive the content.
                size (int): The size. Value ``-1`` means all.

            Keyword Args:
                offset (int): The read offset.
                write_offset (int): The write offset.

            Returns:
                bytes: The content of the buffer.
        '''

        return self.mglo.read_into(buffer, size, offset, write_offset)

    def read_chunks(self, chunk_size, start, step, count) -> bytes:
        '''
            Read the content.

            Args:
                chunk_size (int): The chunk size.
                start (int): First offset.
                step (int): Offset increment.
                count (int): The number of offsets.

            Returns:
                bytes: binary data
        '''

        return self.mglo.read_chunks(chunk_size, start, step, count)

    def read_chunks_into(self, buffer, chunk_size, start, step, count, *, write_offset=0) -> None:
        '''
            Read the content.

            Args:
                buffer (bytarray): The buffer that will receive the content.
                chunk_size (int): The chunk size.
                start (int): First offset.
                step (int): Offset increment.
                count (int): The number of offsets.

            Keyword Args:
                write_offset (int): The write offset.

            Returns:
                bytes: binary data
        '''

        return self.mglo.read(buffer, chunk_size, start, step, count, write_offset)

    def clear(self, size=-1, *, offset=0, chunk=None) -> None:
        '''
            Clear the content.

            Args:
                size (int): The size. Value ``-1`` means all.

            Keyword Args:
                offset (int): The offset.
                chunk (bytes): The chunk to use repeatedly.
        '''

        self.mglo.clear(size, offset, chunk)

    def bind_to_uniform_block(self, binding=0) -> None:
        '''
            Bind the buffer to a uniform block.

            Args:
                binding (int): The uniform block binding.
        '''

        self.mglo.bind_to_uniform_block(binding)

    def bind_to_storage_buffer(self, binding=0) -> None:
        '''
            Bind the buffer to a shader storage buffer.

            Args:
                binding (int): The shader storage binding.
        '''

        self.mglo.bind_to_storage_buffer(binding)

    def orphan(self) -> None:
        '''
            Orphan the buffer.

            It is also called buffer re-specification.

            Reallocate the buffer object before you start modifying it.

            Since allocating storage is likely faster than the implicit synchronization,
            you gain significant performance advantages over synchronization.

            The old storage will still be used by the OpenGL commands that have been sent previously.
            It is likely that the GL driver will not be doing any allocation at all,
            but will just be pulling an old free block off the unused buffer queue and use it,
            so it is likely to be very efficient.

            Examples:

                Simple orphaning example::

                    # For simplicity the VertexArray creation is omitted

                    >>> vbo = ctx.buffer(reserve=1024)

                    # Fill the buffer

                    >>> vbo.write(some_temorary_data)

                    # Issue a render call that uses the vbo

                    >>> vao.render(...)

                    # Orphan the buffer

                    >>> vbo.orphan()

                    # Issue another render call without waiting for the previous one

                    >>> vbo.write(some_temorary_data)
                    >>> vao.render(...)
        '''

        self.mglo.orphan()

    def release(self) -> None:
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()


class Attribute:
    '''
        Attribute
    '''

    __slots__ = ['mglo', '_location', '_array_length', '_dimension', '_shape', '_name']

    def __init__(self):
        self.mglo = None
        self._location = None
        self._array_length = None
        self._dimension = None
        self._shape = None
        self._name = None
        raise TypeError()

    def __repr__(self):
        return '<Attribute: %d>' % self._location

    @property
    def location(self) -> int:
        '''
            int: The location of the attribute.
            The result of the glGetAttribLocation.
        '''

        return self._location

    @property
    def array_length(self) -> int:
        '''
            int: If the attribute is an array the array_length
            is the length of the array otherwise `1`.
        '''

        return self._array_length

    @property
    def dimension(self) -> int:
        '''
            int: The attribute dimension.

            +-----------+-----------+
            | GLSL type | dimension |
            +===========+===========+
            | int       | 1         |
            +-----------+-----------+
            | ivec2     | 2         |
            +-----------+-----------+
            | ivec3     | 3         |
            +-----------+-----------+
            | ivec4     | 4         |
            +-----------+-----------+
            | uint      | 1         |
            +-----------+-----------+
            | uvec2     | 2         |
            +-----------+-----------+
            | uvec3     | 3         |
            +-----------+-----------+
            | uvec4     | 4         |
            +-----------+-----------+
            | float     | 1         |
            +-----------+-----------+
            | vec2      | 2         |
            +-----------+-----------+
            | vec3      | 3         |
            +-----------+-----------+
            | vec4      | 4         |
            +-----------+-----------+
            | double    | 1         |
            +-----------+-----------+
            | dvec2     | 2         |
            +-----------+-----------+
            | dvec3     | 3         |
            +-----------+-----------+
            | dvec4     | 4         |
            +-----------+-----------+
            | mat2      | 4         |
            +-----------+-----------+
            | mat2x3    | 6         |
            +-----------+-----------+
            | mat2x4    | 8         |
            +-----------+-----------+
            | mat3x2    | 6         |
            +-----------+-----------+
            | mat3      | 9         |
            +-----------+-----------+
            | mat3x4    | 12        |
            +-----------+-----------+
            | mat4x2    | 8         |
            +-----------+-----------+
            | mat4x3    | 12        |
            +-----------+-----------+
            | mat4      | 16        |
            +-----------+-----------+
            | dmat2     | 4         |
            +-----------+-----------+
            | dmat2x3   | 6         |
            +-----------+-----------+
            | dmat2x4   | 8         |
            +-----------+-----------+
            | dmat3x2   | 6         |
            +-----------+-----------+
            | dmat3     | 9         |
            +-----------+-----------+
            | dmat3x4   | 12        |
            +-----------+-----------+
            | dmat4x2   | 8         |
            +-----------+-----------+
            | dmat4x3   | 12        |
            +-----------+-----------+
            | dmat4     | 16        |
            +-----------+-----------+
        '''

        return self._dimension

    @property
    def shape(self) -> str:
        '''
            str: The shape is a single character, representing the scalar type of the attriute.

            +---------+--------------------------+
            | shape   | GLSL types               |
            +=========+==========================+
            | ``'i'`` | int                      |
            |         +--------------------------+
            |         | ivec2 ivec3 ivec4        |
            +---------+--------------------------+
            | ``'I'`` | uint                     |
            |         +--------------------------+
            |         | uvec2 uvec3 uvec4        |
            +---------+--------------------------+
            | ``'f'`` | float                    |
            |         +--------------------------+
            |         | vec2 vec3 vec4           |
            |         +--------------------------+
            |         | mat2 mat3 mat4           |
            |         +--------------------------+
            |         | mat2x3 mat2x4 mat3x4     |
            |         | mat4x2 mat4x2 mat4x3     |
            +---------+--------------------------+
            | ``'d'`` | double                   |
            |         +--------------------------+
            |         | dvec2 dvec3 dvec4        |
            |         +--------------------------+
            |         | dmat2 dmat3 dmat4        |
            |         +--------------------------+
            |         | dmat2x3 dmat2x4 dmat3x4  |
            |         | dmat4x2 dmat4x2 dmat4x3  |
            +---------+--------------------------+
        '''

        return self._shape

    @property
    def name(self) -> str:
        '''
            str: The attribute name.
            The name will be filtered to have no array syntax on it's end.
            Attribute name without ``'[0]'`` ending if any.
        '''

        return self._name


class Uniform:
    '''
        A uniform is a global GLSL variable declared with the "uniform" storage qualifier.
        These act as parameters that the user of a shader program can pass to that program.

        In ModernGL, Uniforms can be accessed using :py:attr:`Program.uniforms`
    '''

    __slots__ = ['mglo', '_location', '_array_length', '_dimension', '_name']

    def __init__(self):
        self.mglo = None
        self._location = None
        self._array_length = None
        self._dimension = None
        self._name = None
        raise TypeError()

    def __repr__(self):
        return '<Uniform: %d>' % self._location

    @property
    def location(self) -> int:
        '''
            int: The location of the uniform.
            The location holds the value returned by the glGetUniformLocation.
            To set the value of the uniform use the :py:attr:`value` instead.
        '''

        return self._location

    @property
    def dimension(self) -> int:
        '''
            int: The dimension of the uniform.

            +-----------------+-----------+
            | GLSL type       | dimension |
            +=================+===========+
            | sampler2D       | 1         |
            +-----------------+-----------+
            | sampler2DCube   | 1         |
            +-----------------+-----------+
            | sampler2DShadow | 1         |
            +-----------------+-----------+
            | bool            | 1         |
            +-----------------+-----------+
            | bvec2           | 2         |
            +-----------------+-----------+
            | bvec3           | 3         |
            +-----------------+-----------+
            | bvec4           | 4         |
            +-----------------+-----------+
            | int             | 1         |
            +-----------------+-----------+
            | ivec2           | 2         |
            +-----------------+-----------+
            | ivec3           | 3         |
            +-----------------+-----------+
            | ivec4           | 4         |
            +-----------------+-----------+
            | uint            | 1         |
            +-----------------+-----------+
            | uvec2           | 2         |
            +-----------------+-----------+
            | uvec3           | 3         |
            +-----------------+-----------+
            | uvec4           | 4         |
            +-----------------+-----------+
            | float           | 1         |
            +-----------------+-----------+
            | vec2            | 2         |
            +-----------------+-----------+
            | vec3            | 3         |
            +-----------------+-----------+
            | vec4            | 4         |
            +-----------------+-----------+
            | double          | 1         |
            +-----------------+-----------+
            | dvec2           | 2         |
            +-----------------+-----------+
            | dvec3           | 3         |
            +-----------------+-----------+
            | dvec4           | 4         |
            +-----------------+-----------+
            | mat2            | 4         |
            +-----------------+-----------+
            | mat2x3          | 6         |
            +-----------------+-----------+
            | mat2x4          | 8         |
            +-----------------+-----------+
            | mat3x2          | 6         |
            +-----------------+-----------+
            | mat3            | 9         |
            +-----------------+-----------+
            | mat3x4          | 12        |
            +-----------------+-----------+
            | mat4x2          | 8         |
            +-----------------+-----------+
            | mat4x3          | 12        |
            +-----------------+-----------+
            | mat4            | 16        |
            +-----------------+-----------+
            | dmat2           | 4         |
            +-----------------+-----------+
            | dmat2x3         | 6         |
            +-----------------+-----------+
            | dmat2x4         | 8         |
            +-----------------+-----------+
            | dmat3x2         | 6         |
            +-----------------+-----------+
            | dmat3           | 9         |
            +-----------------+-----------+
            | dmat3x4         | 12        |
            +-----------------+-----------+
            | dmat4x2         | 8         |
            +-----------------+-----------+
            | dmat4x3         | 12        |
            +-----------------+-----------+
            | dmat4           | 16        |
            +-----------------+-----------+
        '''

        return self._dimension

    @property
    def array_length(self) -> int:
        '''
            int: The length of the array of the uniform.
            The array_length is `1` for non array uniforms.
        '''

        return self._array_length

    @property
    def name(self) -> str:
        '''
            str: The name of the uniform.
            The name does not contain leading `[0]`.
            The name may contain `[ ]` when the uniform is part of a struct.
        '''

        return self._name

    @property
    def value(self):
        '''
            The value of the uniform.
            Reading the value of the uniform may force the GPU to sync.

            The value must be a tuple for non array uniforms.
            The value must be a list of tuples for array uniforms.
        '''

        return self.mglo.value

    @value.setter
    def value(self, value):
        self.mglo.value = value

    def read(self) -> bytes:
        '''
            Read the value of the uniform.
        '''

        return self.mglo.data

    def write(self, data) -> None:
        '''
            Write the value of the uniform.
        '''

        self.mglo.data = data


class UniformBlock:
    '''
        UniformBlock
    '''

    __slots__ = ['mglo', '_index', '_size', '_name']

    def __init__(self):
        self.mglo = None
        self._index = None
        self._size = None
        self._name = None
        raise TypeError()

    def __repr__(self):
        return '<UniformBlock: %d>' % self._index

    @property
    def binding(self) -> int:
        '''
            int: The binding of the uniform block.
        '''

        return self.mglo.binding

    @binding.setter
    def binding(self, binding):
        self.mglo.binding = binding

    @property
    def name(self) -> str:
        '''
            str: The name of the uniform block.
        '''

        return self._name

    @property
    def index(self) -> int:
        '''
            int: The index of the uniform block.
        '''

        return self._index

    @property
    def size(self) -> int:
        '''
            int: The size of the uniform block.
        '''

        return self._size


class Varying:
    '''
        Varying
    '''

    __slots__ = ['_number', '_array_length', '_dimension', '_name']

    def __init__(self):
        self._number = None
        self._array_length = None
        self._dimension = None
        self._name = None
        raise TypeError()

    def __repr__(self):
        return '<Varying: %d>' % self.number

    @property
    def number(self) -> int:
        '''
            int: The number of the varying.
        '''

        return self._number

    @property
    def name(self) -> str:
        '''
            str: The name of the varying.
        '''

        return self._name


class Subroutine:
    '''
        Subroutine
    '''

    __slots__ = ['_index', '_name']

    def __init__(self):
        self._index = None
        self._name = None
        raise TypeError()

    def __repr__(self):
        return '<Subroutine: %d>' % self._index

    @property
    def index(self) -> int:
        '''
            int: The index of the subroutine.
        '''

        return self._index

    @property
    def name(self) -> str:
        '''
            str: The name of the subroutine.
        '''

        return self._name


class Texture:
    '''
        A Texture is an OpenGL object that contains one or more images that all
        have the same image format. A texture can be used in two ways. It can
        be the source of a texture access from a Shader, or it can be used
        as a render target.

        A Texture object cannot be instantiated directly, it requires a context.
        Use :py:meth:`Context.texture` or :py:meth:`Context.depth_texture`
        to create one.
    '''

    __slots__ = ['mglo', '_size', '_components', '_samples', '_floats', '_depth', '_glo']

    def __init__(self):
        self.mglo = None
        self._size = (None, None)
        self._components = None
        self._samples = None
        self._floats = None
        self._depth = None
        self._glo = None
        raise TypeError()

    def __repr__(self):
        return '<Texture: %d>' % self.glo

    def __eq__(self, other):
        return type(self) is type(other) and self.mglo is other.mglo

    @property
    def repeat_x(self) -> bool:
        '''
            bool: The repeat_x of the texture.
        '''

        return self.mglo.repeat_x

    @repeat_x.setter
    def repeat_x(self, value):
        self.mglo.repeat_x = value

    @property
    def repeat_y(self) -> bool:
        '''
            bool: The repeat_y of the texture.
        '''

        return self.mglo.repeat_y

    @repeat_y.setter
    def repeat_y(self, value):
        self.mglo.repeat_y = value

    @property
    def filter(self) -> TextureFilter:
        '''
            TextureFilter: The filter of the texture.
        '''

        return self.mglo.filter

    @filter.setter
    def filter(self, value):
        self.mglo.filter = value.mglo

    @property
    def swizzle(self) -> str:
        '''
            str: The swizzle of the texture.
        '''

        return self.mglo.swizzle

    @swizzle.setter
    def swizzle(self, value):
        self.mglo.swizzle = value

    @property
    def width(self) -> int:
        '''
            int: The width of the texture.
        '''

        return self._size[0]

    @property
    def height(self) -> int:
        '''
            int: The height of the texture.
        '''

        return self._size[1]

    @property
    def size(self) -> tuple:
        '''
            tuple: The size of the texture.
        '''

        return self._size

    @property
    def components(self) -> int:
        '''
            int: The number of components of the texture.
        '''

        return self._components

    @property
    def samples(self) -> int:
        '''
            int: The number of samples of the texture.
        '''

        return self._samples

    @property
    def floats(self) -> bool:
        '''
            bool: Is the texture using floats?
        '''

        return self._floats

    @property
    def depth(self) -> bool:
        '''
            bool: Is the texture a depth texture?
        '''

        return self._depth

    @property
    def glo(self) -> int:
        '''
            int: The internal OpenGL object.
            This values is provided for debug purposes only.
        '''

        return self._glo

    def read(self, *, alignment=1) -> bytes:
        '''
            Read the content of the texture into a buffer.

            Keyword Args:
                alignment (int): The byte alignment of the pixels.

            Returns:
                bytes: the pixels
        '''

        return self.mglo.read(alignment)

    def read_into(self, buffer, *, alignment=1, write_offset=0) -> None:
        '''
            Read the content of the texture into a buffer.

            Args:
                buffer (bytearray): The buffer that will receive the pixels.

            Keyword Args:
                alignment (int): The byte alignment of the pixels.
                write_offset (int): The write offset.
        '''

        if type(buffer) is Buffer:
            buffer = buffer.mglo

        return self.mglo.read_into(buffer, alignment, write_offset)

    def write(self, data, viewport=None, *, alignment=1) -> None:
        '''
            Update the content of the texture.

            Args:
                data (bytes): The pixel data.
                viewport (tuple): The viewport.

            Keyword Args:
                alignment (int): The byte alignment of the pixels.
        '''

        if type(data) is Buffer:
            data = data.mglo

        self.mglo.write(data, viewport, alignment)

    def build_mipmaps(self, base=0, max_level=1000) -> None:
        '''
            Generate mipmaps.
        '''

        self.mglo.build_mipmaps(base, max_level)

    def use(self, location=0) -> None:
        '''
            Bind the texture.

            Args:
                location (int): The texture location.
                    Same as the integer value that is used for sampler2D
                    uniforms in the shaders. The value ``0`` will bind the
                    texture to the ``GL_TEXTURE0`` binding point.
        '''

        self.mglo.use(location)

    def release(self) -> None:
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()


class Texture3D:
    '''
        A Texture is an OpenGL object that contains one or more images that all
        have the same image format. A texture can be used in two ways. It can
        be the source of a texture access from a Shader, or it can be used
        as a render target.

        A Texture3D object cannot be instantiated directly, it requires a context.
        Use :py:meth:`Context.texture3d` to create one.
    '''

    __slots__ = ['mglo', '_size', '_components', '_samples', '_floats', '_glo']

    def __init__(self):
        self.mglo = None
        self._size = (None, None, None)
        self._components = None
        self._samples = None
        self._floats = None
        self._glo = None
        raise TypeError()

    def __repr__(self):
        return '<Texture3D: %d>' % self.glo

    def __eq__(self, other):
        return type(self) is type(other) and self.mglo is other.mglo

    @property
    def repeat_x(self) -> bool:
        '''
            bool: The repeat_x of the texture.
        '''

        return self.mglo.repeat_x

    @repeat_x.setter
    def repeat_x(self, value):
        self.mglo.repeat_x = value

    @property
    def repeat_y(self) -> bool:
        '''
            bool: The repeat_y of the texture.
        '''

        return self.mglo.repeat_y

    @repeat_y.setter
    def repeat_y(self, value):
        self.mglo.repeat_y = value

    @property
    def repeat_z(self) -> bool:
        '''
            bool: The repeat_z of the texture.
        '''

        return self.mglo.repeat_z

    @repeat_z.setter
    def repeat_z(self, value):
        self.mglo.repeat_z = value

    @property
    def filter(self) -> TextureFilter:
        '''
            TextureFilter: The filter of the texture.
        '''

        return self.mglo.filter

    @filter.setter
    def filter(self, value):
        self.mglo.filter = value.mglo

    @property
    def swizzle(self) -> str:
        '''
            str: The swizzle of the texture.
        '''

        return self.mglo.swizzle

    @swizzle.setter
    def swizzle(self, value):
        self.mglo.swizzle = value

    @property
    def width(self) -> int:
        '''
            int: The width of the texture.
        '''

        return self._size[0]

    @property
    def height(self) -> int:
        '''
            int: The height of the texture.
        '''

        return self._size[1]

    @property
    def depth(self) -> int:
        '''
            int: The depth of the texture.
        '''

        return self._size[2]

    @property
    def size(self) -> tuple:
        '''
            tuple: The size of the texture.
        '''

        return self._size

    @property
    def components(self) -> int:
        '''
            int: The number of components of the texture.
        '''

        return self._components

    @property
    def floats(self) -> bool:
        '''
            bool: Is the texture using floats?
        '''

        return self._floats

    @property
    def glo(self) -> int:
        '''
            int: The internal OpenGL object.
            This values is provided for debug purposes only.
        '''

        return self._glo

    def read(self, *, alignment=1) -> bytes:
        '''
            Read the content of the texture into a buffer.

            Keyword Args:
                alignment (int): The byte alignment of the pixels.

            Returns:
                bytes: the pixels
        '''

        return self.mglo.read(alignment)

    def read_into(self, buffer, *, alignment=1, write_offset=0) -> None:
        '''
            Read the content of the texture into a buffer.

            Args:
                buffer (bytearray): The buffer that will receive the pixels.

            Keyword Args:
                alignment (int): The byte alignment of the pixels.
                write_offset (int): The write offset.
        '''

        if type(buffer) is Buffer:
            buffer = buffer.mglo

        return self.mglo.read_into(buffer, alignment, write_offset)

    def write(self, data, viewport=None, *, alignment=1) -> None:
        '''
            Update the content of the texture.

            Args:
                data (bytes): The pixel data.
                viewport (tuple): The viewport.

            Keyword Args:
                alignment (int): The byte alignment of the pixels.
        '''

        if type(data) is Buffer:
            data = data.mglo

        self.mglo.write(data, viewport, alignment)

    def build_mipmaps(self, base=0, max_level=1000) -> None:
        '''
            Generate mipmaps.
        '''

        self.mglo.build_mipmaps(base, max_level)

    def use(self, location=0) -> None:
        '''
            Bind the texture.

            Args:
                location (int): The texture location.
                    Same as the integer value that is used for sampler3D
                    uniforms in the shaders. The value ``0`` will bind the
                    texture to the ``GL_TEXTURE0`` binding point.
        '''

        self.mglo.use(location)

    def release(self) -> None:
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()


class TextureCube:
    '''
        A Texture is an OpenGL object that contains one or more images that all
        have the same image format. A texture can be used in two ways. It can
        be the source of a texture access from a Shader, or it can be used
        as a render target.

        A Texture3D object cannot be instantiated directly, it requires a context.
        Use :py:meth:`Context.texture_cube` to create one.
    '''

    __slots__ = ['mglo', '_size', '_components', '_floats', '_glo']

    def __init__(self):
        self.mglo = None
        self._size = (None, None)
        self._components = None
        self._floats = None
        self._glo = None
        raise TypeError()

    def __repr__(self):
        return '<TextureCube: %d>' % self.glo

    def __eq__(self, other):
        return type(self) is type(other) and self.mglo is other.mglo

    @property
    def glo(self) -> int:
        '''
            int: The internal OpenGL object.
            This values is provided for debug purposes only.
        '''

        return self._glo

    def read(self, face, *, alignment=1) -> bytes:
        '''
            Read a face from the cubemap texture.

            Args:
                face (int): The face to read.

            Keyword Args:
                alignment (int): The byte alignment of the pixels.
        '''

        return self.mglo.read(face, alignment)

    def read_into(self, buffer, face, *, alignment=1, write_offset=0) -> None:
        '''
            Read a face from the cubemap texture.

            Args:
                buffer (bytearray): The buffer that will receive the pixels.
                face (int): The face to read.

            Keyword Args:
                alignment (int): The byte alignment of the pixels.
                write_offset (int): The write offset.
        '''

        if type(buffer) is Buffer:
            buffer = buffer.mglo

        return self.mglo.read_into(buffer, face, alignment, write_offset)

    def write(self, face, data, viewport=None, *, alignment=1) -> None:
        '''
            Update the content of the texture.

            Args:
                face (int): The face to update.
                data (bytes): The pixel data.
                viewport (tuple): The viewport.

            Keyword Args:
                alignment (int): The byte alignment of the pixels.
        '''

        if type(data) is Buffer:
            data = data.mglo

        self.mglo.write(face, data, viewport, alignment)

    def use(self, location=0) -> None:
        '''
            Bind the cubemap texture.

            Args:
                location (int): The texture location.
                    Same as the integer value that is used for sampler3D
                    uniforms in the shaders. The value ``0`` will bind the
                    texture to the ``GL_TEXTURE0`` binding point.
        '''

        self.mglo.use(location)

    def release(self) -> None:
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()


class Renderbuffer:
    '''
        Renderbuffer objects are OpenGL objects that contain images.
        They are created and used specifically with :py:class:`Framebuffer` objects.
        They are optimized for use as render targets, while :py:class:`Texture` objects
        may not be, and are the logical choice when you do not need to sample
        from the produced image. If you need to resample, use Textures instead.
        Renderbuffer objects also natively accommodate multisampling.

        A Renderbuffer object cannot be instantiated directly, it requires a context.
        Use :py:meth:`Context.renderbuffer` or :py:meth:`Context.depth_renderbuffer`
        to create one.
    '''

    __slots__ = ['mglo', '_size', '_components', '_samples', '_depth', '_floats', '_glo']

    def __init__(self):
        self.mglo = None
        self._size = (None, None)
        self._components = None
        self._samples = None
        self._depth = None
        self._floats = None
        self._glo = None
        raise TypeError()

    def __repr__(self):
        return '<Renderbuffer: %d>' % self.glo

    def __eq__(self, other):
        return type(self) is type(other) and self.mglo is other.mglo

    @property
    def width(self) -> int:
        '''
            int: The width of the renderbuffer.
        '''

        return self._size[0]

    @property
    def height(self) -> int:
        '''
            int: The height of the renderbuffer.
        '''

        return self._size[1]

    @property
    def size(self) -> tuple:
        '''
            tuple: The size of the renderbuffer.
        '''

        return self._size

    @property
    def samples(self) -> int:
        '''
            int: The samples of the renderbuffer.
        '''

        return self._samples

    @property
    def components(self) -> int:
        '''
            int: The components of the renderbuffer.
        '''

        return self._components

    @property
    def depth(self) -> bool:
        '''
            bool: Is the renderbuffer a depth renderbuffer?
        '''

        return self._depth

    @property
    def floats(self) -> bool:
        '''
            bool: Is the renderbuffer using floats?
        '''

        return self._floats

    @property
    def glo(self) -> int:
        '''
            int: The internal OpenGL object.
            This values is provided for debug purposes only.
        '''

        return self._glo

    def release(self) -> None:
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()


class Shader:
    '''
        Shader objects represent compiled GLSL code for a single shader stage.

        A Shader object cannot be instantiated directly, it requires a context.
        Use the following methods to create one:

            - :py:meth:`Context.vertex_shader`
            - :py:meth:`Context.fragment_shader`
            - :py:meth:`Context.geometry_shader`
            - :py:meth:`Context.tess_evaluation_shader`
            - :py:meth:`Context.tess_control_shader`
    '''

    __slots__ = ['mglo', '_source', '_typename', '_glo']

    def __init__(self):
        self.mglo = None
        self._source = None
        self._typename = None
        self._glo = None
        raise TypeError()

    def __repr__(self):
        return '<Shader: %d>' % self.glo

    def __eq__(self, other):
        return type(self) is type(other) and self.mglo is other.mglo

    @property
    def source(self) -> str:
        '''
            str: The source code of the shader.
        '''

        return self._source

    @property
    def typename(self) -> str:
        '''
            str: The type of the shader.
            The return value is a string.

            - ``'vertex_shader'``
            - ``'fragment_shader'``
            - ``'geometry_shader'``
            - ``'tess_evaluation_shader'``
            - ``'tess_control_shader'``
        '''

        return self._typename

    @property
    def glo(self) -> int:
        '''
            int: The internal OpenGL object.
            This values is provided for debug purposes only.
        '''

        return self._glo

    def release(self) -> None:
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()


class Program:
    '''
        A Program object represents fully processed executable code
        in the OpenGL Shading Language, for one or more Shader stages.

        In ModernGL, a Program object can be assigned to :py:class:`VertexArray` objects.
        The VertexArray object  is capable of binding the Program object once the
        :py:meth:`VertexArray.render` or :py:meth:`VertexArray.transform` is called.

        Program objects has no method called ``use()``, VertexArrays encapsulate this mechanism.

        A Program object cannot be instantiated directly, it requires a context.
        Use :py:meth:`Context.program` to create one.
    '''

    __slots__ = ['mglo', '_members', '_subroutines', '_geom', '_glo']

    def __init__(self):
        self.mglo = None
        self._members = {}
        self._subroutines = None
        self._geom = (None, None, None)
        self._glo = None
        raise TypeError()

    def __repr__(self):
        return '<Program: %d>' % self._glo

    def __eq__(self, other):
        return type(self) is type(other) and self.mglo is other.mglo

    def __getitem__(self, key):
        return self._members[key]

    def __iter__(self):
        yield from self._members

    @property
    def geometry_input(self) -> Primitive:
        '''
            :py:class:`Primitive`: The geometry input primitive.
            The GeometryShader's input primitive if the GeometryShader exists.
            The geometry input primitive will be used for validation.
        '''

        return self._geom[0]

    @property
    def geometry_output(self) -> Primitive:
        '''
            :py:class:`Primitive`: The geometry output primitive.
            The GeometryShader's output primitive if the GeometryShader exists.
        '''

        return self._geom[1]

    @property
    def geometry_vertices(self) -> int:
        '''
            :obj:`int`: The maximum number of vertices that
            the geometry shader will output.
        '''

        return self._geom[2]

    @property
    def subroutines(self) -> Tuple[str, ...]:
        '''
            tuple: The subroutine uniforms.
        '''

        return self._subroutines

    @property
    def glo(self) -> int:
        '''
            int: The internal OpenGL object.
            This values is provided for debug purposes only.
        '''

        return self._glo

    def release(self) -> None:
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()


class ConditionalRender:
    __slots__ = ['mglo']

    def __init__(self):
        self.mglo = None
        raise TypeError()

    def __repr__(self):
        return '<ConditionalRender>'

    def __enter__(self):
        self.mglo.begin_render()
        return self

    def __exit__(self, *args):
        self.mglo.end_render()


class Query:
    __slots__ = ['mglo', 'crender']

    def __init__(self):
        self.mglo = None
        self.crender = None
        raise TypeError()

    def __repr__(self):
        return '<Query>'

    def __enter__(self):
        self.mglo.begin()
        return self

    def __exit__(self, *args):
        self.mglo.end()

    @property
    def samples(self) -> int:
        return self.mglo.samples

    @property
    def primitives(self) -> int:
        return self.mglo.primitives

    @property
    def elapsed(self) -> int:
        return self.mglo.elapsed


class VertexArray:
    '''
        A VertexArray object is an OpenGL object that stores all of the state
        needed to supply vertex data. It stores the format of the vertex data
        as well as the Buffer objects providing the vertex data arrays.

        In ModernGL, the VertexArray object also stores a reference
        for a :py:class:`Program` object, and some Subroutine information.

        A VertexArray object cannot be instantiated directly, it requires a context.
        Use :py:meth:`Context.vertex_array` or :py:meth:`Context.simple_vertex_array`
        to create one.
    '''

    __slots__ = ['mglo', '_program', '_index_buffer', '_glo']

    def __init__(self):
        self.mglo = None
        self._program = None
        self._index_buffer = None
        self._glo = None
        raise TypeError()

    def __repr__(self):
        return '<VertexArray: %d>' % self.glo

    def __eq__(self, other):
        return type(self) is type(other) and self.mglo is other.mglo

    @property
    def program(self) -> 'Program':
        '''
            Program: The program assinged to the VertexArray.
            The program used when rendering or transforming primitives.
        '''

        return self._program

    @property
    def index_buffer(self) -> 'Buffer':
        '''
            Buffer: The index buffer if the index_buffer is set, otherwise ``None``.
        '''

        return self._index_buffer

    @property
    def vertices(self) -> int:
        '''
            int: The number of vertices detected.
            This is the minimum of the number of vertices possible per Buffer.
            The size of the index_buffer determines the number of vertices.
            Per instance vertex attributes does not affect this number.
        '''

        return self.mglo.vertices

    @property
    def subroutines(self) -> Tuple[int, ...]:
        '''
            tuple: The subroutines assinged to the VertexArray.
            The subroutines used when rendering or transforming primitives.
        '''

        return self.mglo.subroutines

    @subroutines.setter
    def subroutines(self, value):
        self.mglo.subroutines = tuple(value)

    @property
    def glo(self) -> int:
        '''
            int: The internal OpenGL object.
            This values is provided for debug purposes only.
        '''

        return self._glo

    def render(self, mode=TRIANGLES, vertices=-1, *, first=0, instances=1) -> None:
        '''
            The render primitive (mode) must be the same as
            the input primitive of the GeometryShader.

            Args:
                mode (Primitive): By default `TRIANGLES` will be used.
                vertices (int): The number of vertices to transform.

            Keyword Args:
                first (int): The index of the first vertex to start with.
                instances (int): The number of instances.
        '''

        self.mglo.render(mode.mglo, vertices, first, instances)

    def transform(self, buffer, mode=POINTS, vertices=-1, *, first=0, instances=1) -> None:
        '''
            Transform vertices.
            Stores the output in a single buffer.
            The transform primitive (mode) must be the same as
            the input primitive of the GeometryShader.

            Args:
                buffer (Buffer): The buffer to store the output.
                mode (Primitive): By default `TRIANGLES` will be used.
                vertices (int): The number of vertices to transform.

            Keyword Args:
                first (int): The index of the first vertex to start with.
                instances (int): The number of instances.
        '''

        self.mglo.transform(buffer.mglo, mode.mglo, vertices, first, instances)

    def bind(self, attribute, buffer, *, offset, stride, divisor) -> None:
        attr = self._program._members.get(attribute)
        if type(attr) is not Attribute:
            raise KeyError(attribute)
        self.mglo.bind(attr.mglo, buffer.mglo, offset, stride, divisor)

    def release(self) -> None:
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()


class ComputeShader:
    '''
        A Compute Shader is a Shader Stage that is used entirely for computing arbitrary information.
        While it can do rendering, it is generally used for tasks not directly related to drawing.
    '''

    __slots__ = ['mglo', '_glo']

    def __init__(self):
        self.mglo = None
        self._glo = None
        raise TypeError()

    def __repr__(self):
        return '<ComputeShader: %d>' % self.glo

    def __eq__(self, other):
        return type(self) is type(other) and self.mglo is other.mglo

    @property
    def source(self) -> str:
        '''
            str: The source code of the compute shader.
        '''

        return self.mglo.source

    @property
    def glo(self) -> int:
        '''
            int: The internal OpenGL object.
            This values is provided for debug purposes only.
        '''

        return self._glo

    def run(self, group_x=1, group_y=1, group_z=1) -> None:
        '''
            Run the compute shader.

            Args:
                group_x (int): The number of work groups to be launched in the X dimension.
                group_y (int): The number of work groups to be launched in the Y dimension.
                group_z (int): The number of work groups to be launched in the Z dimension.
        '''

        return self.mglo.run(group_x, group_y, group_z)

    def release(self) -> None:
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()


class Framebuffer:
    '''
        A :py:class:`Framebuffer` is a collection of buffers that can be used as the destination for rendering.
        The buffers for Framebuffer objects reference images from either Textures or Renderbuffers.

        Create a :py:class:`Framebuffer` using :py:meth:`Context.framebuffer`.
    '''

    __slots__ = ['mglo', '_color_attachments', '_depth_attachment', '_size', '_samples', '_glo']

    def __init__(self):
        self.mglo = None
        self._color_attachments = None
        self._depth_attachment = None
        self._size = (None, None)
        self._samples = None
        self._glo = None
        raise TypeError()

    def __repr__(self):
        return '<Framebuffer: %d>' % self.glo

    def __eq__(self, other):
        return type(self) is type(other) and self.mglo is other.mglo

    @property
    def viewport(self) -> Tuple[int, int, int, int]:
        '''
            tuple: The viewport of the framebuffer.
        '''

        return self.mglo.viewport

    @viewport.setter
    def viewport(self, value):
        self.mglo.viewport = tuple(value)

    @property
    def color_mask(self) -> Tuple[bool, bool, bool, bool]:
        '''
            tuple: The color mask of the framebuffer.
        '''

        return self.mglo.color_mask

    @color_mask.setter
    def color_mask(self, value):
        self.mglo.color_mask = value

    @property
    def depth_mask(self) -> bool:
        '''
            tuple: The depth mask of the framebuffer.
        '''

        return self.mglo.depth_mask

    @depth_mask.setter
    def depth_mask(self, value):
        self.mglo.depth_mask = value

    @property
    def width(self) -> int:
        '''
            int: The width of the framebuffer.
        '''

        return self._size[0]

    @property
    def height(self) -> int:
        '''
            int: The height of the framebuffer.
        '''

        return self._size[1]

    @property
    def size(self) -> tuple:
        '''
            tuple: The size of the framebuffer.
        '''

        return self._size

    @property
    def samples(self) -> int:
        '''
            int: The samples of the framebuffer.
        '''

        return self._samples

    @property
    def bits(self) -> Dict[str, str]:
        '''
            dict: The bits of the framebuffer.
        '''

        return self.mglo.bits

    @property
    def color_attachments(self) -> Tuple[object, ...]:
        '''
            tuple: The color attachments of the framebuffer.
        '''

        return self._color_attachments

    @property
    def depth_attachment(self) -> object:
        '''
            object: The depth attachment of the framebuffer.
        '''

        return self._depth_attachment

    @property
    def glo(self) -> int:
        '''
            int: The internal OpenGL object.
            This values is provided for debug purposes only.
        '''

        return self._glo

    def clear(self, red=0.0, green=0.0, blue=0.0, alpha=0.0, depth=1.0, *, viewport=None) -> None:
        '''
            Clear the framebuffer.

            Values must be in ``[0.0, 1.0]`` range.
            If the `viewport` is not ``None`` then scrissor test
            will be used to clear the given viewport.

            If the `viewport` is a 2-tuple it will clear the
            ``(0, 0, width, height)`` where ``(width, height)`` is the 2-tuple.

            If the `viewport` is a 4-tuple it will clear the given viewport.

            Args:
                red (float): color component.
                green (float): color component.
                blue (float): color component.
                alpha (float): alpha component.
                depth (float): depth value.

            Keyword Args:
                viewport (tuple): The viewport.
        '''

        if viewport is not None:
            viewport = tuple(viewport)

        self.mglo.clear(red, green, blue, alpha, depth, viewport)

    def use(self) -> None:
        '''
            Bind the framebuffer. Set the target for the
            `VertexArray.render` or `VertexArray.transform` methods.
        '''

        self.mglo.use()

    def read(self, viewport=None, components=3, *, attachment=0, alignment=1, floats=False) -> bytes:
        '''
            Read the content of the framebuffer.

            Args:
                viewport (tuple): The viewport.
                components (int): The number of components to read.

            Keyword Args:
                attachment (int): The color attachment.
                alignment (int): The byte alignment of the pixels.
                floats (bool): The precision of the pixels.

            Returns:
                bytes: the pixels
        '''

        return self.mglo.read(viewport, components, attachment, alignment, floats)

    def read_into(self, buffer, viewport=None, components=3, *,
                  attachment=0, alignment=1, floats=False, write_offset=0) -> None:
        '''
            Read the content of the framebuffer into a buffer.

            Args:
                buffer (bytearray): The buffer that will receive the pixels.
                viewport (tuple): The viewport.
                components (int): The number of components to read.

            Keyword Args:
                attachment (int): The color attachment.
                alignment (int): The byte alignment of the pixels.
                floats (bool): The precision of the pixels.
                write_offset (int): The write offset.
        '''

        if type(buffer) is Buffer:
            buffer = buffer.mglo

        return self.mglo.read_into(buffer, viewport, components, attachment, alignment, floats, write_offset)

    def release(self) -> None:
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()


class Context:
    '''
        Create a :py:class:`Context` using:

        - :py:func:`ModernGL.create_context`
        - :py:func:`ModernGL.create_standalone_context`

        The :py:func:`create_context` must be used when rendering in a window.
        The :py:func:`create_standalone_context` must be used when rendering
        without a window.

        Members:

            - :py:meth:`Context.program`
            - :py:meth:`Context.vertex_shader`
            - :py:meth:`Context.fragment_shader`
            - :py:meth:`Context.geometry_shader`
            - :py:meth:`Context.tess_evaluation_shader`
            - :py:meth:`Context.tess_control_shader`
            - :py:meth:`Context.buffer`
            - :py:meth:`Context.simple_vertex_array`
            - :py:meth:`Context.vertex_array`
            - :py:meth:`Context.texture`
            - :py:meth:`Context.depth_texture`
            - :py:meth:`Context.renderbuffer`
            - :py:meth:`Context.depth_renderbuffer`
            - :py:meth:`Context.simple_framebuffer`
            - :py:meth:`Context.framebuffer`
    '''

    __slots__ = ['mglo', '_screen', '_info', 'version_code']

    def __init__(self):
        self.mglo = None
        self._screen = None
        self._info = None
        self.version_code = None
        raise TypeError()

    def __repr__(self):
        return '<Context>'

    def __eq__(self, other):
        return type(self) is type(other) and self.mglo is other.mglo

    @property
    def line_width(self) -> float:
        '''
            float: Set the default line width.
        '''

        return self.mglo.line_width

    @line_width.setter
    def line_width(self, value):
        self.mglo.line_width = value

    @property
    def point_size(self) -> float:
        '''
            float: Set the default point size.
        '''

        return self.mglo.point_size

    @point_size.setter
    def point_size(self, value):
        self.mglo.point_size = value

    @property
    def depth_func(self) -> int:
        '''
            int: Set the default depth func.
        '''

        raise Exception()

    @depth_func.setter
    def depth_func(self, value):
        self.mglo.depth_func = value

    @property
    def blend_func(self) -> int:
        '''
            int: Set the default depth func.
        '''

        raise Exception()

    @blend_func.setter
    def blend_func(self, value):
        self.mglo.blend_func = tuple(value)


    @property
    def viewport(self) -> Tuple[int, int, int, int]:
        '''
            tuple: The viewport.

            Reading this property may force the GPU to sync.
            Use this property to set the viewport only.
        '''

        return self.mglo.fbo.viewport

    @viewport.setter
    def viewport(self, value):
        self.mglo.fbo.viewport = tuple(value)

    @property
    def max_samples(self) -> int:
        '''
            int: The max samples.
        '''

        return self.mglo.max_samples

    @property
    def max_integer_samples(self) -> int:
        '''
            int: The max integer samples.
        '''

        return self.mglo.max_integer_samples

    @property
    def max_texture_units(self) -> int:
        '''
            int: The max texture units.
        '''

        return self.mglo.max_texture_units

    @property
    def default_texture_unit(self) -> int:
        '''
            int: The default texture unit.
        '''

        return self.mglo.default_texture_unit

    @default_texture_unit.setter
    def default_texture_unit(self, value):
        self.mglo.default_texture_unit = value

    @property
    def screen(self) -> 'Framebuffer':
        '''
            Framebuffer: The default framebuffer.
        '''

        return self._screen

    @property
    def wireframe(self) -> bool:
        '''
            bool: Wireframe settings for debugging.
        '''

        return self.mglo.wireframe

    @wireframe.setter
    def wireframe(self, value):
        self.mglo.wireframe = value

    @property
    def front_face(self) -> str:
        '''
            str: The front_face.
        '''

        return self.mglo.front_face

    @front_face.setter
    def front_face(self, value):
        self.mglo.front_face = str(value)

    @property
    def error(self) -> str:
        '''
            str: The result of glGetError() but human readable.
            This values is provided for debug purposes only.
        '''

        return self.mglo.error

    @property
    def info(self) -> Dict[str, object]:
        '''
            dict: The result of multiple glGet.
        '''

        if self._info is None:
            self._info = self.mglo.info

        return self._info

    def clear(self, red=0.0, green=0.0, blue=0.0, alpha=0.0, depth=1.0, *, viewport=None) -> None:
        '''
            Clear the framebuffer.

            Values must be in ``(0, 255)`` range.
            If the `viewport` is not ``None`` then scrissor test
            will be used to clear the given viewport.

            If the `viewport` is a 2-tuple it will clear the
            ``(0, 0, width, height)`` where ``(width, height)`` is the 2-tuple.

            If the `viewport` is a 4-tuple it will clear the given viewport.

            Args:
                red (float): color component.
                green (float): color component.
                blue (float): color component.
                alpha (float): alpha component.

            Keyword Args:
                viewport (tuple): The viewport.
        '''

        if viewport is not None:
            viewport = tuple(viewport)

        self.mglo.fbo.clear(red, green, blue, alpha, depth, viewport)

    def enable_only(self, flags) -> None:
        '''
            Enable flags.

            Valid flags are:

                - :py:data:`ModernGL.NOTHING`
                - :py:data:`ModernGL.BLEND`
                - :py:data:`ModernGL.DEPTH_TEST`
                - :py:data:`ModernGL.CULL_FACE`

            Args:
                flags (EnableFlag): The flag to enable.
        '''

        self.mglo.enable_only(flags)

    def enable(self, flags) -> None:
        '''
            Enable flags.

            Valid flags are:

                - :py:data:`ModernGL.BLEND`
                - :py:data:`ModernGL.DEPTH_TEST`
                - :py:data:`ModernGL.CULL_FACE`

            Args:
                flag (EnableFlag): The flag to enable.
        '''

        self.mglo.enable(flags)

    def disable(self, flags) -> None:
        '''
            Disable flags.

            Valid flags are:

                - :py:data:`ModernGL.BLEND`
                - :py:data:`ModernGL.DEPTH_TEST`
                - :py:data:`ModernGL.CULL_FACE`

            Args:
                flag (EnableFlag): The flag to disable.
        '''

        self.mglo.disable(flags)

    def finish(self) -> None:
        '''
            Wait for all drawing commands to finish.
        '''

        self.mglo.finish()

    def copy_buffer(self, dst, src, size=-1, *, read_offset=0, write_offset=0) -> None:
        '''
            Copy buffer content.

            Args:
                dst (Buffer): Destination buffer.
                src (Buffer): Source buffer.
                size (int): Size to copy.

            Keyword Args:
                read_offset (int): Read offset.
                write_offset (int): Write offset.
        '''

        self.mglo.copy_buffer(dst.mglo, src.mglo, size, read_offset, write_offset)

    def copy_framebuffer(self, dst, src) -> None:
        '''
            Copy framebuffer content.

            Use this method to:

                - blit framebuffers.
                - copy framebuffer content into a texture.
                - downsample framebuffers. (it will allow to read the framebuffer's content)
                - downsample a framebuffer directly to a texture.

            Args:
                dst (Framebuffer or Texture): Destination framebuffer or texture.
                src (Framebuffer): Source framebuffer.
        '''

        self.mglo.copy_framebuffer(dst.mglo, src.mglo)

    def detect_framebuffer(self, glo=None) -> 'Framebuffer':
        '''
            Detect framebuffer.

            Args:
                glo (int): Framebuffer object.

            Returns:
                Framebuffer: framebuffer.
        '''

        res = Framebuffer.__new__(Framebuffer)
        res.mglo, res._glo = self.mglo.detect_framebuffer(glo)
        return res

    def buffer(self, data=None, *, reserve=0, dynamic=False) -> Buffer:
        '''
            Create a :py:class:`Buffer`.

            Args:
                data (bytes): Content of the new buffer.

            Keyword Args:
                reserve (int): The number of bytes to reserve.
                dynamic (bool): Treat buffer as dynamic.

            Returns:
                Buffer: buffer
        '''

        if type(reserve) is str:
            reserve = mgl.strsize(reserve)

        res = Buffer.__new__(Buffer)
        res.mglo, res._size, res._glo = self.mglo.buffer(data, reserve, dynamic)
        res._dynamic = dynamic
        return res

    def texture(self, size, components, data=None, *, samples=0, alignment=1, floats=False) -> 'Texture':
        '''
            Create a :py:class:`Texture`.

            Args:
                size (tuple): The width and height of the texture.
                components (int): The number of components 1, 2, 3 or 4.
                data (bytes): Content of the texture.

            Keyword Args:
                samples (int): The number of samples. Value `0` means no multisample format.
                alignment (int): The byte alignment 1, 2, 4 or 8.
                floats (bool): Use floating point precision.

            Returns:
                Texture: texture
        '''

        res = Texture.__new__(Texture)
        res.mglo, res._glo = self.mglo.texture(size, components, data, samples, alignment, floats)
        res._size = size
        res._components = components
        res._samples = samples
        res._floats = floats
        res._depth = False
        return res

    def texture3d(self, size, components, data=None, *, alignment=1, floats=False) -> 'Texture3D':
        '''
            Create a :py:class:`Texture3D`.

            Args:
                size (tuple): The width, height and depth of the texture.
                components (int): The number of components 1, 2, 3 or 4.
                data (bytes): Content of the texture.

            Keyword Args:
                alignment (int): The byte alignment 1, 2, 4 or 8.
                floats (bool): Use floating point precision.

            Returns:
                Texture3D: texture
        '''

        res = Texture3D.__new__(Texture3D)
        res.mglo, res._glo = self.mglo.texture3d(size, components, data, alignment, floats)
        return res

    def texture_cube(self, size, components, data=None, *, alignment=1, floats=False) -> 'TextureCube':
        '''
            Create a :py:class:`TextureCube`.

            Args:
                size (tuple): The width, height and depth of the texture.
                components (int): The number of components 1, 2, 3 or 4.
                data (bytes): Content of the texture.

            Keyword Args:
                alignment (int): The byte alignment 1, 2, 4 or 8.
                floats (bool): Use floating point precision.

            Returns:
                TextureCube: texture
        '''

        res = TextureCube.__new__(TextureCube)
        res.mglo, res._glo = self.mglo.texture_cube(size, components, data, alignment, floats)
        res._size = size
        res._components = components
        res._floats = floats
        return res

    def depth_texture(self, size, data=None, *, samples=0, alignment=4) -> 'Texture':
        '''
            Create a :py:class:`Texture`.

            Args:
                size (tuple): The width and height of the texture.
                data (bytes): Content of the texture.

            Keyword Args:
                samples (int): The number of samples. Value `0` means no multisample format.
                alignment (int): The byte alignment 1, 2, 4 or 8.

            Returns:
                Texture: depth texture
        '''

        res = Texture.__new__(Texture)
        res.mglo, res._glo = self.mglo.depth_texture(size, data, samples, alignment)
        res._size = size
        res._components = 1
        res._samples = samples
        res._floats = True
        res._depth = True
        return res

    def vertex_array(self, program, content, index_buffer=None) -> 'VertexArray':
        '''
            Create a :py:class:`VertexArray`.

            Args:
                program (Program): The program used by :py:meth:`~VertexArray.render` and
                                   :py:meth:`~VertexArray.transform`.
                content (list): A list of (buffer, format, attributes).
                index_buffer (Buffer): An index buffer.

            Returns:
                VertexArray: vertex array
        '''

        index_buffer_mglo = None if index_buffer is None else index_buffer.mglo

        content = tuple((a.mglo, b, tuple(program._members[x].mglo for x in c)) for a, b, c in content)

        res = VertexArray.__new__(VertexArray)
        res.mglo, res._glo = self.mglo.vertex_array(program.mglo, content, index_buffer_mglo)
        res._program = program
        res._index_buffer = index_buffer
        return res

    def simple_vertex_array(self, program, buffer, *attributes, index_buffer=None) -> 'VertexArray':
        '''
            Create a :py:class:`VertexArray`.

            This is an alias for::

                format = detect_format(program, attributes)
                vertex_array(program, [(buffer, format, attributes)])

            Args:
                program (Program): The program used by :py:meth:`~VertexArray.render` and
                                   :py:meth:`~VertexArray.transform`.
                buffer (Buffer): The buffer.
                attributes (list): A list of attribute names.

            Returns:
                VertexArray: vertex array
        '''

        if len(attributes) == 1 and type(attributes[0]) is not str:
            attributes = attributes[0]

        content = [(buffer, detect_format(program, attributes), attributes)]
        return self.vertex_array(program, content, index_buffer)

    def program(self, shaders, varyings=()) -> 'Program':
        '''
            Create a :py:class:`Program` object.

            Only linked programs will be returned.

            For more information please see: :py:class:`Program` and :py:class:`Shader`

            A single shader in the `shaders` parameter is also accepted.
            The varyings are only used when a transform program is created.

            Args:
                shaders (list): A list of :py:class:`Shader` objects.
                varyings (list): A list of varying names.

            Returns:
                Program: program

            Examples:

                A simple program designed for rendering::

                    >>> my_render_program = ctx.program([
                    ... 	ctx.vertex_shader(\'\'\'
                    ... 		#version 330
                    ...
                    ... 		in vec2 vert;
                    ...
                    ... 		void main() {
                    ... 			gl_Position = vec4(vert, 0.0, 1.0);
                    ... 		}
                    ... 	\'\'\'),
                    ... 	ctx.fragment_shader(\'\'\'
                    ... 		#version 330
                    ...
                    ... 		out vec4 color;
                    ...
                    ... 		void main() {
                    ... 			color = vec4(0.3, 0.5, 1.0, 1.0);
                    ... 		}
                    ... 	\'\'\'),
                    ... ])

                A simple program designed for transforming::

                    >>> my_vertex_shader = ctx.vertex_shader(\'\'\'
                    ...     #version 330
                    ...
                    ...     in vec4 vert;
                    ...     out float vert_length;
                    ...
                    ...     void main() {
                    ...         vert_length = length(vert);
                    ...     }
                    ... \'\'\')

                    >>> my_transform_program = ctx.program(my_vertex_shader, ['vert_length'])
        '''

        if type(shaders) is Shader:
            shaders = (shaders,)

        shaders = tuple(x.mglo for x in shaders)

        if type(varyings) is str:
            varyings = (varyings,)

        varyings = tuple(varyings)

        res = Program.__new__(Program)
        res.mglo, ls1, ls2, ls3, ls4, ls5, res._subroutines, res._geom, res._glo = self.mglo.program(shaders, varyings)

        members = {}

        for item in ls1:
            obj = Attribute.__new__(Attribute)
            obj.mglo, obj._location, obj._array_length, obj._dimension, obj._shape, obj._name = item
            members[obj.name] = obj

        for item in ls2:
            obj = Varying.__new__(Varying)
            obj._number, obj._array_length, obj._dimension, obj._name = item
            members[obj.name] = obj

        for item in ls3:
            obj = Uniform.__new__(Uniform)
            obj.mglo, obj._location, obj._array_length, obj._dimension, obj._name = item
            members[obj.name] = obj

        for item in ls4:
            obj = UniformBlock.__new__(UniformBlock)
            obj.mglo, obj._index, obj._size, obj._name = item
            members[obj.name] = obj

        for item in ls5:
            obj = Subroutine.__new__(Subroutine)
            obj._index, obj._name = item
            members[obj.name] = obj

        res._members = members
        return res

    def query(self, *, samples=False, any_samples=False, time=False, primitives=False) -> 'Query':
        res = Query.__new__(Query)
        res.mglo = self.mglo.query(samples, any_samples, time, primitives)
        res.crender = None
        if samples or any_samples:
            res.crender = ConditionalRender.__new__(ConditionalRender)
            res.crender.mglo = res.mglo
        return res

    def vertex_shader(self, source) -> 'Shader':
        '''
            The Vertex Shader is a programmable Shader stage in the rendering pipeline
            that handles the processing of individual vertices.

            Vertex shaders are fed Vertex Attribute data, as specified from a vertex array
            object by a drawing command. A vertex shader receives a single vertex from the
            vertex stream and generates a single vertex to the output vertex stream.

            Args:
                source (str): The source code in GLSL.

            Returns:
                Shader: vertex shader

            Examples:

                Create a simple vertex shader::

                    >>> my_vertex_shader = ctx.vertex_shader(\'\'\'
                    ...     #version 330
                    ...
                    ...     in vec2 vert;
                    ...
                    ...     void main() {
                    ...         gl_Position = vec4(vert, 0.0, 1.0);
                    ...     }
                    ... \'\'\')
        '''

        res = Shader.__new__(Shader)
        res.mglo, res._glo = self.mglo.vertex_shader(source)
        res._typename = 'vertex_shader'
        res._source = source
        return res

    def fragment_shader(self, source) -> 'Shader':
        '''
            A Fragment Shader is the Shader stage that will process a Fragment generated by
            the Rasterization into a set of colors and a single depth value.

            Args:
                source (str): The source code in GLSL.

            Returns:
                Shader: fragment shader

            Examples:

                Create a simple fragment shader::

                    >>> my_fragment_shader = ctx.fragment_shader(\'\'\'
                    ...     #version 330
                    ...
                    ...     out vec4 color;
                    ...
                    ...     void main() {
                    ...         color = vec4(0.3, 0.5, 1.0, 1.0);
                    ...     }
                    ... \'\'\')
        '''

        res = Shader.__new__(Shader)
        res.mglo, res._glo = self.mglo.fragment_shader(source)
        res._typename = 'fragment_shader'
        res._source = source
        return res

    def geometry_shader(self, source) -> 'Shader':
        '''
            A Geometry Shader is a Shader program written in GLSL that governs the processing of Primitives.
            Geometry shaders reside between the Vertex Shaders (or the optional Tessellation stage) and the
            fixed-function Vertex Post-Processing stage.

            A geometry shader is optional and does not have to be used.

            Args:
                source (str): The source code in GLSL.

            Returns:
                Shader: geometry shader
        '''

        res = Shader.__new__(Shader)
        res.mglo, res._glo = self.mglo.geometry_shader(source)
        res._typename = 'geometry_shader'
        res._source = source
        return res

    def tess_evaluation_shader(self, source) -> 'Shader':
        '''
            Tessellation is the Vertex Processing stage in the OpenGL rendering pipeline where
            patches of vertex data are subdivided into smaller Primitives.

            The Tessellation Evaluation Shader takes the tessellated patch and computes
            the vertex values for each generated vertex.

            Args:
                source (str): The source code in GLSL.

            Returns:
                Shader: tesselation evaluation shader
        '''

        res = Shader.__new__(Shader)
        res.mglo, res._glo = self.mglo.tess_evaluation_shader(source)
        res._typename = 'tess_evaluation_shader'
        res._source = source
        return res

    def tess_control_shader(self, source) -> 'Shader':
        '''
            The Tessellation Control Shader (TCS) determines how much tessellation to do.
            It can also adjust the actual patch data, as well as feed additional patch data to later stages.
            The Tessellation Control Shader is optional.

            Args:
                source (str): The source code in GLSL.

            Returns:
                Shader: tesselation control shader
        '''

        res = Shader.__new__(Shader)
        res.mglo, res._glo = self.mglo.tess_control_shader(source)
        res._typename = 'tess_control_shader'
        res._source = source
        return res

    def simple_framebuffer(self, size, components=4, *, samples=0, floats=False) -> 'Framebuffer':
        '''
            A :py:class:`Framebuffer` is a collection of buffers that can be used as the destination for rendering.
            The buffers for Framebuffer objects reference images from either Textures or Renderbuffers.

            Args:
                size (tuple): The width and height of the renderbuffer.
                components (int): The number of components 1, 2, 3 or 4.

            Keyword Args:
                samples (int): The number of samples. Value `0` means no multisample format.
                floats (bool): Use floating point precision.

            Returns:
                Framebuffer: framebuffer
        '''

        return self.framebuffer(
            self.renderbuffer(size, components, samples=samples, floats=floats),
            self.depth_renderbuffer(size, samples=samples),
        )

    def framebuffer(self, color_attachments, depth_attachment=None) -> 'Framebuffer':
        '''
            A :py:class:`Framebuffer` is a collection of buffers that can be used as the destination for rendering.
            The buffers for Framebuffer objects reference images from either Textures or Renderbuffers.

            Args:
                color_attachments (list): A list of `Texture` or `Renderbuffer` objects.
                depth_attachment (Renderbuffer or Texture): A `Texture` or `Renderbuffer` object.

            Returns:
                Framebuffer: framebuffer
        '''

        if type(color_attachments) is Texture or type(color_attachments) is Renderbuffer:
            color_attachments = (color_attachments,)

        ca_mglo = tuple(x.mglo for x in color_attachments)
        da_mglo = None if depth_attachment is None else depth_attachment.mglo

        res = Framebuffer.__new__(Framebuffer)
        res.mglo, res._size, res._samples, res._glo = self.mglo.framebuffer(ca_mglo, da_mglo)
        res._color_attachments = tuple(color_attachments)
        res._depth_attachment = depth_attachment
        return res

    def renderbuffer(self, size, components=4, *, samples=0, floats=False) -> 'Renderbuffer':
        '''
            :py:class:`Renderbuffer` objects are OpenGL objects that contain images.
            They are created and used specifically with :py:class:`Framebuffer` objects.

            Args:
                size (tuple): The width and height of the renderbuffer.
                components (int): The number of components 1, 2, 3 or 4.

            Keyword Args:
                samples (int): The number of samples. Value `0` means no multisample format.
                floats (bool): Use floating point precision.

            Returns:
                Renderbuffer: renderbuffer
        '''

        res = Renderbuffer.__new__(Renderbuffer)
        res.mglo, res._glo = self.mglo.renderbuffer(size, components, samples, floats)
        res._size = size
        res._components = components
        res._samples = samples
        res._depth = False
        res._floats = floats
        return res

    def depth_renderbuffer(self, size, *, samples=0) -> 'Renderbuffer':
        '''
            :py:class:`Renderbuffer` objects are OpenGL objects that contain images.
            They are created and used specifically with :py:class:`Framebuffer` objects.

            Args:
                size (tuple): The width and height of the renderbuffer.

            Keyword Args:
                samples (int): The number of samples. Value `0` means no multisample format.

            Returns:
                Renderbuffer: depth renderbuffer
        '''

        res = Renderbuffer.__new__(Renderbuffer)
        res.mglo, res._glo = self.mglo.depth_renderbuffer(size, samples)
        res._size = size
        res._components = 1
        res._samples = samples
        res._depth = True
        res._floats = True
        return res

    def compute_shader(self, source) -> 'ComputeShader':
        '''
            A :py:class:`ComputeShader` is a Shader Stage that is used entirely for computing arbitrary information.
            While it can do rendering, it is generally used for tasks not directly related to drawing.

            Args:
                source (str): The source of the compute shader.

            Returns:
                ComputeShader: compute shader program
        '''

        res = ComputeShader.__new__(ComputeShader)
        res.mglo, res._glo = self.mglo.compute_shader(source)
        return res

    def release(self) -> None:
        '''
            Release the ModernGL object.
        '''

        self.mglo.release()


def create_context(require=None) -> Context:
    '''
        Create a ModernGL context by loading OpenGL functions from an existing OpenGL context.
        An OpenGL context must exists. If rendering is done without a window please use the
        :py:func:`create_standalone_context` instead.

        Keyword Arguments:
            require (int): OpenGL version code.

        Returns:
            Context: context
    '''

    ctx = Context.__new__(Context)
    ctx._screen = Framebuffer.__new__(Framebuffer)
    ctx.mglo, ctx._screen.mglo, ctx.version_code = mgl.create_context()
    ctx._info = None

    if require is not None and ctx.version_code < require:
        raise Exception('The version required is not provided')

    return ctx


def create_standalone_context(require=None, **settings) -> 'Context':
    '''
        Create a standalone ModernGL context.

        Keyword Arguments:
            require (int): OpenGL version code.

        Returns:
            Context: context
    '''

    ctx = Context.__new__(Context)
    ctx._screen = Framebuffer.__new__(Framebuffer)
    ctx.mglo, ctx._screen.mglo, ctx.version_code = mgl.create_standalone_context(settings)
    ctx._info = None

    if require is not None and ctx.version_code < require:
        raise Exception('The version required is not provided')

    return ctx


def detect_format(program, attributes) -> str:
    '''
        Detect format for vertex attributes.
        The format returned does not contain padding.

        Args:
            program (Program): The program.
            attributes (list): A list of attribute names.

        Returns:
            str: The tightly packed format for the attributes.
    '''

    def fmt(attr):
        '''
            For internal use only.
        '''

        return attr.array_length * attr.dimension, attr.shape

    return ''.join('%d%s' % fmt(program[a]) for a in attributes)
