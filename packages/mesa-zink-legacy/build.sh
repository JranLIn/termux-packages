TERMUX_PKG_HOMEPAGE=https://mesa3d.org
TERMUX_PKG_DESCRIPTION="Experimental Mesa 21.1.8 Zink for Maleoon Vulkan bridge"
TERMUX_PKG_LICENSE="MIT"
TERMUX_PKG_LICENSE_FILE="docs/license.rst"
TERMUX_PKG_MAINTAINER="@JranLIn"
TERMUX_PKG_VERSION=21.1.8
TERMUX_PKG_SHA256=5cd32f5d089dca75300578a3d771a656eaed652090573a2655fe4e7022d56bfc
TERMUX_PKG_SRCURL=https://archive.mesa3d.org/older-versions/21.x/mesa-${TERMUX_PKG_VERSION}.tar.xz
TERMUX_PKG_DEPENDS="libandroid-shmem, libc++, libdrm, libx11, libxext, libxfixes, libxshmfence, libxxf86vm, vulkan-loader, zlib, zstd"
TERMUX_PKG_BUILD_DEPENDS="xorgproto, vulkan-headers"
TERMUX_PKG_EXTRA_CONFIGURE_ARGS="
-Dplatforms=x11
-Dgallium-drivers=zink
-Dvulkan-drivers=
-Ddri-drivers=
-Dllvm=disabled
-Dglx=dri
-Degl=enabled
-Dgles1=disabled
-Dgles2=enabled
-Dgbm=disabled
-Dshared-glapi=enabled
-Dshader-cache=enabled
-Dglvnd=false
"
termux_step_pre_configure() {
  CPPFLAGS+=" -D__USE_GNU"
  LDFLAGS+=" -landroid-shmem -llog"
}
