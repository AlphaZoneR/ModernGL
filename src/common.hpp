#pragma once

#if defined(_WIN32) || defined(_WIN64)

// Windows

#include <Windows.h>

#define WGL_ACCELERATION 0x2003
#define WGL_FULL_ACCELERATION 0x2027
#define WGL_CONTEXT_MAJOR_VERSION 0x2091
#define WGL_CONTEXT_MINOR_VERSION 0x2092
#define WGL_CONTEXT_PROFILE_MASK 0x9126
#define WGL_CONTEXT_CORE_PROFILE_BIT 0x0001

typedef int (WINAPI * my_ChoosePixelFormat_type)(HDC hdc, const int * piAttribIList, const float * pfAttribFList, unsigned nMaxFormats, int * piFormats, unsigned * nNumFormats);
typedef HGLRC (WINAPI * my_CreateContextAttribs_type)(HDC hdc, HGLRC hglrc, const int * attribList);

my_ChoosePixelFormat_type my_ChoosePixelFormat;
my_CreateContextAttribs_type my_CreateContextAttribs;

#elif defined(__APPLE__)

// OSX

#include <OpenGL/OpenGL.h>
#include <ApplicationServices/ApplicationServices.h>

#include <OpenGL/gl.h>
#include <OpenGL/glext.h>

#else

// Linux



#include <dlfcn.h>
#include <GL/gl.h>
#include <X11/Xlib.h>
#include <X11/X.h>

enum {
    MGL_X11CTX = 0,
	MGL_EGLCTX = 1,	
    MGL_OSMESACTX = 2
} LINUX_CTX_TYPE;

#define Bool int

typedef unsigned long XID;
typedef struct __GLXFBConfigRec * GLXFBConfig;
typedef struct __GLXcontextRec * GLXContext;
typedef XID Pixmap;
typedef XID Window;

// X11

#define GLX_CONTEXT_MAJOR_VERSION 0x2091
#define GLX_CONTEXT_MINOR_VERSION 0x2092
#define GLX_CONTEXT_PROFILE_MASK 0x9126
#define GLX_CONTEXT_CORE_PROFILE_BIT 0x0001


extern GLXFBConfig *glXChooseFBConfig( Display *dpy, int screen, const int *attribList, int *nitems );
extern XVisualInfo* glXChooseVisual( Display *dpy, int screen, int *attribList );

typedef GLXContext (* GLXCREATECONTEXTATTRIBSARBPROC)(Display * display, GLXFBConfig config, GLXContext context, Bool direct, const int * attribs);

static int SilentXErrorHandler(Display * d, XErrorEvent * e) {
	return 0;
}

typedef Display * (* my_XOpenDisplay_type)(const char * display);
typedef int (* my_XCloseDisplay_type)(Display * display);
typedef int (* my_XDestroyWindow_type)(Display * display, Window window);
typedef Window (* my_XCreateWindow_type)(Display * display, Window window, int x, int y, unsigned int width, unsigned int height, unsigned int border_width, int depth, unsigned int _class, Visual * visual, unsigned long valuemask, XSetWindowAttributes * xsetwindowattributes);
typedef XErrorHandler (* my_XSetErrorHandler_type)(XErrorHandler);
typedef Colormap (* my_XCreateColormap_type)(Display * display, Window window, Visual * visual, int alloc);


my_XOpenDisplay_type my_XOpenDisplay;
my_XCloseDisplay_type my_XCloseDisplay;
my_XDestroyWindow_type my_XDestroyWindow;
my_XCreateWindow_type my_XCreateWindow;
my_XSetErrorHandler_type my_XSetErrorHandler;
my_XCreateColormap_type my_XCreateColormap;


// EGL

#define EGLAPI
#define EGLAPIENTRY

typedef Display * EGLNativeDisplayType;
typedef Pixmap EGLNativePixmapType;
typedef Window EGLNativeWindowType;

#define EGL_RED_SIZE 0x3024
#define EGL_GREEN_SIZE 0x3023
#define EGL_BLUE_SIZE 0x3022
#define EGL_NONE 0x3038
#define EGL_BAD_DISPLAY 0x3008
#define EGL_FALSE 0
#define EGL_BAD_MATCH 0x3009
#define EGL_NOT_INITIALIZED 0x3001
#define EGL_BAD_CONFIG 0x3005
#define EGL_BAD_CONTEXT 0x3006
#define EGL_BAD_ATTRIBUTE 0x3004
#define EGL_BAD_ALLOC 0x3003

#define EGL_NO_DISPLAY 0
#define EGL_NO_CONTEXT 0
#define EGL_NO_DISPLAY 0
#define EGL_NO_SURFACE 0

typedef void * EGLDisplay;
typedef void * EGLConfig;
typedef void * EGLSurface;
typedef void * EGLContext;

typedef unsigned int EGLBoolean;
typedef int EGLint;

typedef EGLAPI EGLDisplay (EGLAPIENTRY * my_eglGetDisplay_type)(EGLNativeDisplayType display_id);
typedef EGLAPI EGLBoolean (EGLAPIENTRY * my_eglInitialize_type)(EGLDisplay dpy, EGLint * major, EGLint * minor);
typedef EGLAPI EGLBoolean (EGLAPIENTRY * my_eglChooseConfig_type)(EGLDisplay dpy, const EGLint * attrib_list, EGLConfig * configs, EGLint config_size, EGLint * num_config);
typedef EGLAPI EGLContext (EGLAPIENTRY * my_eglCreateContext_type)(EGLDisplay dpy, EGLConfig config, EGLContext share_context, const EGLint * attrib_list);
typedef EGLAPI EGLint (EGLAPIENTRY * my_eglGetError_type)(void);
typedef EGLAPI EGLBoolean (EGLAPIENTRY * my_eglMakeCurrent_type)(EGLDisplay dpy, EGLSurface draw, EGLSurface read, EGLContext ctx);

my_eglGetDisplay_type my_eglGetDisplay;
my_eglInitialize_type my_eglInitialize;
my_eglChooseConfig_type my_eglChooseConfig;
my_eglCreateContext_type my_eglCreateContext;
my_eglGetError_type my_eglGetError;
my_eglMakeCurrent_type my_eglMakeCurrent;

// OSMesa

#define OSMESA_RGBA GL_RGBA
#define OSMESA_DEPTH_BITS 0x30
#define OSMESA_STENCIL_BITS 0x31
#define OSMESA_ACCUM_BITS 0x32
#define OSMESA_PROFILE 0x33
#define OSMESA_CORE_PROFILE 0x34
#define OSMESA_COMPAT_PROFILE 0x35
#define OSMESA_CONTEXT_MAJOR_VERSION 0x36
#define OSMESA_CONTEXT_MINOR_VERSION 0x37

typedef struct osmesa_context * OSMesaContext;

typedef GLAPI OSMesaContext (GLAPIENTRY * my_OSMesaCreateContextExt_type)(GLenum format, GLint depthBits, GLint stencilBits, GLint accumBits, OSMesaContext sharelist);
typedef GLAPI GLboolean (GLAPIENTRY * my_OSMesaMakeCurrent_type)(OSMesaContext ctx, void * buffer, GLenum type, GLsizei width, GLsizei height);
typedef GLAPI void (GLAPIENTRY * my_OSMesaDestroyContext_type)(OSMesaContext ctx);
typedef GLAPI OSMesaContext (GLAPIENTRY * my_OSMesaCreateContextAttribs_type)(const int * attribList, OSMesaContext sharelist);

my_OSMesaCreateContextExt_type my_OSMesaCreateContextExt;
my_OSMesaMakeCurrent_type my_OSMesaMakeCurrent;
my_OSMesaDestroyContext_type my_OSMesaDestroyContext;
my_OSMesaCreateContextAttribs_type my_OSMesaCreateContextAttribs;

#endif