GLContext CreateX11Context(PyObject * settings){
    GLContext context = {};

	int width = 1;
	int height = 1;
	PyObject * size_hint = (settings != Py_None) ? PyDict_GetItemString(settings, "size") : 0;
	if (size_hint && Py_TYPE(size_hint) == &PyTuple_Type && PyTuple_GET_SIZE(size_hint) == 2) {
		width = PyLong_AsLong(PyTuple_GET_ITEM(size_hint, 0));
		height = PyLong_AsLong(PyTuple_GET_ITEM(size_hint, 1));
		width = width < 1 ? width : 1;
		height = height < 1 ? height : 1;
	}

	Display * dpy = XOpenDisplay(0);

	if (!dpy) {
		dpy = XOpenDisplay(":0.0");
	}

	if (!dpy) {
		MGLError_Set("cannot detect the display");
		return context;
	}

	int nelements = 0;

	GLXFBConfig * fbc = glXChooseFBConfig(dpy, DefaultScreen(dpy), 0, &nelements);

	if (!fbc) {
		MGLError_Set("cannot read the display configuration");
		XCloseDisplay(dpy);
		return context;
	}

	static int attributeList[] = {
		GLX_RGBA,
		GLX_DOUBLEBUFFER,
		GLX_RED_SIZE, 8,
		GLX_GREEN_SIZE, 8,
		GLX_BLUE_SIZE, 8,
		GLX_DEPTH_SIZE, 24,
		None,
	};

	XVisualInfo * vi = glXChooseVisual(dpy, DefaultScreen(dpy), attributeList);

	if (!vi) {
		XCloseDisplay(dpy);

		MGLError_Set("cannot choose a visual info");
		return context;
	}

	XSetWindowAttributes swa;
	swa.colormap = XCreateColormap(dpy, RootWindow(dpy, vi->screen), vi->visual, AllocNone);
	swa.border_pixel = 0;
	swa.event_mask = StructureNotifyMask;

	Window win = XCreateWindow(dpy, RootWindow(dpy, vi->screen), 0, 0, width, height, 0, vi->depth, InputOutput, vi->visual, CWBorderPixel | CWColormap | CWEventMask, &swa);

	if (!win) {
		XCloseDisplay(dpy);

		MGLError_Set("cannot create window");
		return context;
	}

	// XMapWindow(dpy, win);

	GLXCREATECONTEXTATTRIBSARBPROC glXCreateContextAttribsARB = (GLXCREATECONTEXTATTRIBSARBPROC)glXGetProcAddress((const GLubyte *)"glXCreateContextAttribsARB");

	GLXContext ctx = 0;

	XSetErrorHandler(SilentXErrorHandler);

	if (glXCreateContextAttribsARB) {
		for (int i = 0; i < versions; ++i) {
			int attribs[] = {
				GLX_CONTEXT_PROFILE_MASK, GLX_CONTEXT_CORE_PROFILE_BIT,
				GLX_CONTEXT_MAJOR_VERSION, version[i].major,
				GLX_CONTEXT_MINOR_VERSION, version[i].minor,
				0, 0,
			};

			ctx = glXCreateContextAttribsARB(dpy, *fbc, 0, true, attribs);

			if (ctx) {
				break;
			}
		}
	}

	if (!ctx) {
		ctx = glXCreateContext(dpy, vi, 0, GL_TRUE);
	}

	if (!ctx) {
		XDestroyWindow(dpy, win);
		XCloseDisplay(dpy);

		MGLError_Set("cannot create OpenGL context");
		return context;
	}

	XSetErrorHandler(0);

	int make_current = glXMakeCurrent(dpy, win, ctx);

	if (!make_current) {
		glXDestroyContext(dpy, ctx);
		XDestroyWindow(dpy, win);
		XCloseDisplay(dpy);

		MGLError_Set("cannot select OpenGL context");
		return context;
	}

	context.display = (void *)dpy;
	context.window = (void *)win;
	context.context = (void *)ctx;

	context.standalone = true;

	return context;
}