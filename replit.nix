# # {pkgs}: {
# #   deps = [
# #     pkgs.libGLU
# #     pkgs.libGL
# #   ];
# # }

# { pkgs }:
# {
#   deps = [
#     pkgs.python310
#     pkgs.python310Packages.pip
#     pkgs.python310Packages.streamlit
#     pkgs.python310Packages.opencv-python-headless
#     pkgs.python310Packages.numpy
#     pkgs.python310Packages.pillow
#     pkgs.python310Packages.streamlit-drawable-canvas
#   ];
# }

{ pkgs }: {
  deps = [
    pkgs.zlib
    pkgs.tk
    pkgs.tcl
    pkgs.openjpeg
    pkgs.libxcrypt
    pkgs.libwebp
    pkgs.libtiff
    pkgs.libjpeg
    pkgs.libimagequant
    pkgs.lcms2
    pkgs.freetype
    pkgs.python310                                     # Core Python version
    pkgs.python310Packages.pip                         # Python package installer
    pkgs.python310Packages.streamlit                   # Streamlit framework
    pkgs.python310Packages.opencv-python-headless      # OpenCV for image processing
    pkgs.python310Packages.numpy                       # Numerical computing
    pkgs.python310Packages.pillow                      # Image processing
    pkgs.python310Packages.streamlit-drawable-canvas   # Drawing canvas for Streamlit
    pkgs.libGLU                                        # OpenGL Utility Library
    pkgs.libGL                                         # Core OpenGL Library
  ];
}