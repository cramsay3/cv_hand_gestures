# Camera Troubleshooting

Camera troubleshooting workflow for SoloStage AI.

## Usage
Type `/camera_troubleshooting` in chat for camera fix guidance.

## Troubleshooting Steps:

### 1. Comprehensive Fix (Try First)
```bash
./fix_camera_freezing.sh
```
- Sets all cameras to stable 30fps
- Optimizes USB power management
- Enhances UVC driver settings
- Reloads drivers and udev rules

### 2. HDMI Camera Specific Fix
```bash
./fix_hdmi_camera.sh
```
- Optimizes HDMI camera for USB 2.0
- Sets stable 30fps with optimized exposure
- HDMI-specific USB power management

### 3. USB Bandwidth Optimization
```bash
./fix_usb_bandwidth.sh
```
- Reduces HDMI camera to 1280x720@30fps
- Sets H.264 cameras to 1920x1080@30fps
- Optimizes USB core buffer settings

### 4. Verify Camera Settings
```bash
# Check all camera frame rates
v4l2-ctl --device=/dev/video0 --get-parm
v4l2-ctl --device=/dev/video2 --get-parm
v4l2-ctl --device=/dev/video6 --get-parm
```

### 5. If Issues Persist:
- Move cameras to USB 3.0 ports (blue colored)
- Use fewer cameras simultaneously
- Reduce resolution further if needed

## Common Issues:
- Camera freezing: Usually 60fps instability → use 30fps
- USB disconnections: Power management issues → run comprehensive fix
- Poor quality: USB 2.0 bandwidth → use bandwidth optimization
