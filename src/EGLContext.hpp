#pragma once

#if defined(_WIN32) && !defined(__SCITECH_SNAP__)
#   define KHRONOS_APICALL __declspec(dllimport)
#elif defined (__SYMBIAN32__)
#   define KHRONOS_APICALL IMPORT_C
#elif defined(__ANDROID__)
#   define KHRONOS_APICALL __attribute__((visibility("default")))
#else
#   define KHRONOS_APICALL
#endif

#if defined(_WIN32) && !defined(_WIN32_WCE) && !defined(__SCITECH_SNAP__)
    /* Win32 but not WinCE */
#   define KHRONOS_APIENTRY __stdcall
#else
#   define KHRONOS_APIENTRY
#endif

#ifndef EGLAPI
#define EGLAPI KHRONOS_APICALL
#endif

#if defined(_WIN32) || defined(__VC32__) && !defined(__CYGWIN__) && !defined(__SCITECH_SNAP__) /* Win32 and WinCE */
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN 1
#endif
#include <windows.h>

typedef HDC     EGLNativeDisplayType;
typedef HBITMAP EGLNativePixmapType;
typedef HWND    EGLNativeWindowType;

#elif defined(__APPLE__) || defined(__WINSCW__) || defined(__SYMBIAN32__)  /* Symbian */

typedef int   EGLNativeDisplayType;
typedef void *EGLNativeWindowType;
typedef void *EGLNativePixmapType;

#elif defined(__ANDROID__) || defined(ANDROID)

struct ANativeWindow;
struct egl_native_pixmap_t;

typedef struct ANativeWindow*           EGLNativeWindowType;
typedef struct egl_native_pixmap_t*     EGLNativePixmapType;
typedef void*                           EGLNativeDisplayType;

#elif defined(USE_OZONE)

typedef intptr_t EGLNativeDisplayType;
typedef intptr_t EGLNativeWindowType;
typedef intptr_t EGLNativePixmapType;

#elif defined(__unix__)

/* X11 (tentative)  */
#include <X11/Xlib.h>
#include <X11/Xutil.h>

typedef Display *EGLNativeDisplayType;
typedef Pixmap   EGLNativePixmapType;
typedef Window   EGLNativeWindowType;

#else
#error "Platform not recognized"
#endif


#ifndef EGLAPIENTRY
#define EGLAPIENTRY  KHRONOS_APIENTRY
#endif
#define EGLAPIENTRYP EGLAPIENTRY*

#define EGL_CAST(type, value) (static_cast<type>(value))

#define EGL_RED_SIZE        0x3024
#define EGL_GREEN_SIZE      0x3023
#define EGL_BLUE_SIZE       0x3022
#define EGL_NONE            0x3038
#define EGL_BAD_DISPLAY     0x3008
#define EGL_FALSE           0
#define EGL_BAD_MATCH       0x3009
#define EGL_NOT_INITIALIZED 0x3001
#define EGL_BAD_CONFIG      0x3005
#define EGL_BAD_CONTEXT     0x3006
#define EGL_BAD_ATTRIBUTE   0x3004
#define EGL_BAD_ALLOC       0x3003

#define EGL_NO_DISPLAY      EGL_CAST(EGLDisplay, 0)
#define EGL_NO_CONTEXT      EGL_CAST(EGLContext, 0)
#define EGL_NO_DISPLAY      EGL_CAST(EGLDisplay, 0)
#define EGL_NO_SURFACE      EGL_CAST(EGLSurface, 0)

typedef void *EGLDisplay;
typedef void *EGLConfig;
typedef void *EGLSurface;
typedef void *EGLContext;


typedef unsigned int EGLBoolean;
typedef int          EGLint;


typedef EGLAPI EGLDisplay (EGLAPIENTRY * my_eglGetDisplay_type)    (EGLNativeDisplayType display_id);
typedef EGLAPI EGLBoolean (EGLAPIENTRY * my_eglInitialize_type)    (EGLDisplay dpy, EGLint *major, EGLint *minor);
typedef EGLAPI EGLBoolean (EGLAPIENTRY * my_eglChooseConfig_type)  (EGLDisplay dpy, const EGLint *attrib_list, EGLConfig *configs, EGLint config_size, EGLint *num_config);
typedef EGLAPI EGLContext (EGLAPIENTRY * my_eglCreateContext_type) (EGLDisplay dpy, EGLConfig config, EGLContext share_context, const EGLint *attrib_list);
typedef EGLAPI EGLint     (EGLAPIENTRY * my_eglGetError_type)      (void);
typedef EGLAPI EGLBoolean (EGLAPIENTRY * my_eglMakeCurrent_type)   (EGLDisplay dpy, EGLSurface draw, EGLSurface read, EGLContext ctx);

my_eglGetDisplay_type    my_eglGetDisplay;
my_eglInitialize_type    my_eglInitialize;
my_eglChooseConfig_type  my_eglChooseConfig;
my_eglCreateContext_type my_eglCreateContext;
my_eglGetError_type      my_eglGetError;
my_eglMakeCurrent_type   my_eglMakeCurrent;

static EGLint const attribute_list_egl[] = {
    EGL_RED_SIZE, 1,
    EGL_GREEN_SIZE, 1,
    EGL_BLUE_SIZE, 1,
    EGL_NONE
};

void LoadEGLFunctions(){
    void * handle;  
    char * error;
    handle = dlopen("libEGL.so.1", RTLD_LAZY);

    if(!handle){
        printf("%s\n", dlerror());
        exit(EXIT_FAILURE);
    }

    my_eglGetDisplay = (my_eglGetDisplay_type) dlsym(handle, "eglGetDisplay");

    if(!my_eglGetDisplay){
        printf("Error loading eglGetDisplay!");
    }

    my_eglInitialize = (my_eglInitialize_type) dlsym(handle, "eglInitialize");

    if(!my_eglInitialize){
        printf("Error loading eglInitialize!");
    }

    my_eglChooseConfig = (my_eglChooseConfig_type) dlsym(handle, "eglChooseConfig");

    if(!my_eglChooseConfig){
        printf("Error loading eglChooseConfig!");
    }

    my_eglCreateContext = (my_eglCreateContext_type) dlsym(handle, "eglCreateContext");

    if(!my_eglCreateContext){
        printf("Error loading eglCreateContext!");
    }

    my_eglGetError = (my_eglGetError_type) dlsym(handle, "eglGetError");

    if(!my_eglGetError){
        printf("Error loading eglGetError!");
    }

    my_eglMakeCurrent = (my_eglMakeCurrent_type) dlsym(handle, "eglMakeCurrent");

    if(!my_eglMakeCurrent){
        printf("Error loading eglMakeCurrent!");
    }
}


GLContext CreateEGLContext(PyObject * settings){
	
    LoadEGLFunctions();

	EGLDisplay display;
    EGLConfig config;
    EGLContext context;
    GLContext ret = {};

    EGLint num_config;
    
    display = my_eglGetDisplay(0);

    if(display == EGL_NO_DISPLAY){
    	printf("Error detecting display!");
    	return ret;
    }

    EGLint init = my_eglInitialize(display, NULL, NULL);

    if(init == EGL_BAD_DISPLAY){
    	printf("Error! Display is not an EGL display connection.");
    	return ret;
    }

    EGLBoolean cfg = my_eglChooseConfig(display, attribute_list_egl, &config, 1, &num_config);

    if(cfg == EGL_FALSE){
    	printf("Error setting configurations!");
    	return ret;
    }

    context = my_eglCreateContext(display, config, EGL_NO_CONTEXT, NULL);
    EGLint ctx = my_eglGetError();

    if(context == EGL_NO_CONTEXT){
    	printf("Error! Creation of the context failed.");
    }

    if(ctx == EGL_BAD_MATCH){
    	printf("Error! The current rendering API is EGL_NONE or the server context state for share_context exists in an address space which cannot be shared with the newly created context!");
    	return ret;
    }else if(ctx == EGL_BAD_DISPLAY){
    	printf("Error! Display is not an EGL display connection.");
    	return ret;
    }else if(ctx == EGL_NOT_INITIALIZED){
    	printf("Error! Display has not been initialized.");
    	return ret;
    }else if(ctx == EGL_BAD_CONFIG){
    	printf("Error! Config is not an EGL frame buffer configuration, or does not support the current rendering API.");
    	return ret;
    }else if(ctx == EGL_BAD_CONTEXT){
    	printf("Error! Share_context is not an EGL rendering context!");
    	return ret;
    }else if(ctx == EGL_BAD_ATTRIBUTE){
    	printf("Error! Attrib_list contains an invalid context attribute or if an attribute is not recognized or out of range.");
    	return ret;
    }else if(ctx == EGL_BAD_ALLOC){
    	printf("Error! There are not enough resources to allocate the new context.");
    	return ret;
    }

    EGLBoolean cpdy = my_eglMakeCurrent(display, NULL, NULL, context);
 	
 	if(cpdy == EGL_FALSE){
 		printf("Fail make current");
 		return ret;
 	}
    
    ret.display = display;
    ret.context = context;

    return ret;
}