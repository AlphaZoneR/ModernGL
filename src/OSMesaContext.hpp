

#define OSMESA_RGBA		             	GL_RGBA
#define OSMESA_DEPTH_BITS            	0x30
#define OSMESA_STENCIL_BITS         	0x31
#define OSMESA_ACCUM_BITS            	0x32
#define OSMESA_PROFILE               	0x33
#define OSMESA_CORE_PROFILE          	0x34
#define OSMESA_COMPAT_PROFILE        	0x35
#define OSMESA_CONTEXT_MAJOR_VERSION 	0x36
#define OSMESA_CONTEXT_MINOR_VERSION 	0x37

typedef struct osmesa_context *OSMesaContext;

typedef GLAPI OSMesaContext (GLAPIENTRY * my_OSMesaCreateContextExt_type)	    (GLenum format, GLint depthBits, GLint stencilBits, GLint accumBits, OSMesaContext sharelist);
typedef GLAPI GLboolean     (GLAPIENTRY * my_OSMesaMakeCurrent_type)            (OSMesaContext ctx, void *buffer, GLenum type,GLsizei width, GLsizei height );
typedef GLAPI void          (GLAPIENTRY * my_OSMesaDestroyContext_type)         (OSMesaContext ctx);

typedef GLAPI OSMesaContext (GLAPIENTRY * my_OSMesaCreateContextAttribs_type)   (const int *attribList, OSMesaContext sharelist);

my_OSMesaCreateContextExt_type     my_OSMesaCreateContextExt;
my_OSMesaMakeCurrent_type          my_OSMesaMakeCurrent;
my_OSMesaDestroyContext_type       my_OSMesaDestroyContext;
my_OSMesaCreateContextAttribs_type my_OSMesaCreateContextAttribs;

void LoadMesaFunctions(){
	void * handle;	
	char * error;
	handle = dlopen("libOSMesa.so", RTLD_LAZY);

	if(!handle){
		printf("%s\n", dlerror());
		exit(EXIT_FAILURE);
	}

	my_OSMesaCreateContextExt = (my_OSMesaCreateContextExt_type) dlsym(handle, "OSMesaCreateContextExt");

	if(!my_OSMesaCreateContextExt){
		printf("Error loading OSMesaCreateContextExt!");
	}

	my_OSMesaMakeCurrent = (my_OSMesaMakeCurrent_type) dlsym(handle, "OSMesaMakeCurrent");

	if(!my_OSMesaMakeCurrent){
		printf("Error loading OSMesaMakeCurrent!");
	}

	my_OSMesaDestroyContext = (my_OSMesaDestroyContext_type) dlsym(handle, "OSMesaDestroyContext");


	if(!my_OSMesaDestroyContext){
		printf("Error loading OSMesaDestroyContext!");
	}

	my_OSMesaCreateContextAttribs = (my_OSMesaCreateContextAttribs_type) dlsym(handle, "OSMesaCreateContextAttribs");

	if(!my_OSMesaCreateContextAttribs){
		printf("Error loading OSMesaCreateContextAttribs!");
	}


}	


GLContext CreateOSMesaContext(PyObject * settings){
	
    GLContext ret = {};
	LoadMesaFunctions();


	const int attribList[] = {
		OSMESA_PROFILE, OSMESA_COMPAT_PROFILE,
		OSMESA_CONTEXT_MAJOR_VERSION, 2,	
		OSMESA_CONTEXT_MINOR_VERSION, 0,
		0, 0
	};


	OSMesaContext ctx = my_OSMesaCreateContextAttribs(attribList, NULL);

	if(!ctx){
		printf("OSMesaCreateContextExt failed!\n");
		return ret;
	}	

	void * buffer = malloc(1 * 1 * 4 * sizeof(GLubyte));

	if(!my_OSMesaMakeCurrent(ctx, buffer, GL_UNSIGNED_BYTE, 1, 1)){
		printf("OSMesaMakeCurrent failed!\n");
		return ret;
	}

    ret.context = ctx;
    ret.buffer = buffer;
    ret.display = NULL;
    ret.window = NULL;

	return ret;

}