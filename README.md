APS360 Summer 2026 Project Screencapper
---

This screencapper was written to streamline manual screenshots of Google Street View images for
my computer vision project. It is written in Python and Tkinter, with a focus for Windows 10/11.

To use, run `install_deps.bat` before running the program; this installs the `mss`, `opencv-python`/`cv2`,
and `numpy` libraries. When screenshotting, MSS captures a screenshot before using `cv2` and `numpy`
to automatically rescale the image to 500x500, which is the input size for my CV model.

Screenshot controls: move mouse to move screenshot target, left-click to screenshot, scroll to
resize screenshot target, W and S to change the building identifier number. (The identifier is
visible in the top left corner of the target.)

Outputs: 500x500 .jpg images in `out/[borough id]/[borough id]_[building id]_[photo id].jpg`, e.g.
`out/OldToronto/OldToronto_0_1.jpg` is where to find image #1 of OldToronto building #1.