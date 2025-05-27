all:
	$(MAKE) -C libj/filelib
	$(MAKE) -C libj/envlib
	$(MAKE) -C libj/ffmpeglib
	# Ensure the file library is built before the daemon
	# This is important as the daemon depends on the file library.
	$(MAKE) -C deamon

clean:
	$(MAKE) -C libj/filelib clean
	$(MAKE) -C libj/envlib clean
	$(MAKE) -C libj/ffmpeglib clean
	$(MAKE) -C deamon clean

distclean:
	$(MAKE) -C libj/filelib distclean
	$(MAKE) -C libj/envlib distclean
	$(MAKE) -C libj/ffmpeglib distclean
	$(MAKE) -C deamon distclean

.PHONY: all clean distclean
# This Makefile orchestrates the build process for both the daemon and the file library.
# It ensures that the necessary libraries are built before compiling the daemon.
# The `all` target builds both components, while `clean` and `distclean` targets handle cleanup.
# The `distclean` target removes both object files and library files, ensuring a clean state.
# The `-C` option in the `make` command changes the directory to the specified path before executing the Makefile there.
# This allows for modular builds, where each component can be built independently.