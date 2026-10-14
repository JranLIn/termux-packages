# Mesa 21.1.8 Zink + swrast headless test

This is an **experimental, side-by-side** Termux package distinct from `mesa-zink-legacy`.
It compiles Gallium `zink,swrast` with LLVM disabled, producing a Zink
driver and a softpipe-backed `swrast_dri.so` entrypoint.

**A passing EGL initialization alone does NOT prove Maleoon hardware acceleration.**
First test with `GALLIUM_DRIVER=softpipe`, then with `GALLIUM_DRIVER=zink`.
Record `GL_RENDERER`, `GL_VERSION`, Zink/Vulkan loader messages, and the
result of an actual offscreen rendering test. These must all agree.

Do not install this experimental package over the system Mesa. Unpack instead:

```sh
ROOT="$HOME/mesa21-headless/root"
mkdir -p "$ROOT"
dpkg-deb -x ~/storage/downloads/mesa-zink-legacy-headless_21.1.8_aarch64.deb "$ROOT"
export LIBGL_DRIVERS_PATH="$ROOT$PREFIX/lib/dri"
export EGL_PLATFORM=surfaceless
export LIBGL_ALWAYS_SOFTWARE=1
unset LD_LIBRARY_PATH
```

Use a verified EGL test executable which explicitly loads
`$ROOT$PREFIX/lib/libEGL.so`, or preload the isolated Mesa GLAPI and EGL
libraries if that is how your probe is linked. Check actual loaded modules;
do not interpret a system Mesa 26.x renderer as success.

First run:
```sh
export GALLIUM_DRIVER=softpipe
# Run your existing EGL surfaceless probe here
```

Second run (keep your **previously working** Maleoon ICD JSON setup):
```sh
export GALLIUM_DRIVER=zink
export MESA_LOADER_DRIVER_OVERRIDE=zink
# Run the same EGL surfaceless probe here
```

Do NOT set `LD_LIBRARY_PATH=$PREFIX/lib` just for Vulkan;
that was shown on this device to contaminate Android's Vulkan loader
namespace and trigger a misleading `libbinder_ndk.so` error.

If the softpipe control succeeds but Zink fails, the problem is downstream
of the EGL/DRI entrypoint: gather Vulkan instance/device and feature logs.
