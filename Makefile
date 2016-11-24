VERSION=1.0.0
SERVICE=slb
DIST=${SERVICE}-${VERSION}.tar.gz
PYTHONLIB := /usr/include/python2.7
CFLAGS := -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing -I${PYTHONLIB}
PYTHON_FILES := $(shell find ./${SERVICE} -name "*.py" ! -name "__init__.py")
OBJECTS := $(patsubst %.py,%.so,$(PYTHON_FILES))

all: $(OBJECTS)

%.c: %.py
	@ echo "Compiling $<"
	@ cython --no-docstrings $< -o $(patsubst %.py,%.c,$<)

%.so: %.c
	@ $(CC) $(CFLAGS) -o $@ $<
	@ strip --strip-all $@

compress:
	@ echo "Compress.............."
	@ for f in `find ./${SERVICE} -name "*.so"`; do \
		upx -9 $$f; \
	done

clean-build:
	@ echo "Clean.build..........."
	@ find ./${SERVICE} ! -name "__init__.py" -name "*.py*" -delete
	@ find ./${SERVICE} -name "__init__.so" -delete

clean:
	@ echo "Clean................."
	@ find ./${SERVICE} -name "*.py[co]" -delete
	@ find ./${SERVICE} -name "*.so" -delete
	@ rm -rf ${DIST}

dist:
	@ echo "Make.DIST.............."
	@ tar -C . -cf ${DIST} * --exclude=*.spec --exclude=Makefile

rpm:
	@ echo "Make.RPM.............."
	@ sed -i "/Version:.*/c Version: ${VERSION}" /root/rpmbuild/SPECS/${SERVICE}.spec
	@ cp -rf ${DIST} /root/rpmbuild/SOURCES/
	@ rpmbuild -bb --clean --rmsource /root/rpmbuild/SPECS/${SERVICE}.spec


run: clean
	@ $(MAKE) dist && $(MAKE) rpm

.DEFAULT: all
.PHONY: all %.c %.so clean clean-build compress dist rpm run
