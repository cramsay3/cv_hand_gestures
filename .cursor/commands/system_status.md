# System Status Check

Quick system status check for SoloStage AI.

## Usage
Type `/system_status` in chat to get current system status.

## What it checks:
- SoloStage AI service status
- OBS Studio status  
- WebSocket connection
- Camera detection
- Audio system status

## Commands to run:
```bash
# Check service status
systemctl --user status solostage-ai.service

# Check OBS process
pgrep -f "obs"

# Check WebSocket port
ss -tlnp | grep ":4455"

# Check cameras
ls /dev/elp_*

# Check audio devices
arecord -l

# Full system test
./scripts/test_environment.sh
```

## Expected Status:
- ✅ SoloStage AI Service: RUNNING
- ✅ OBS Studio: RUNNING  
- ✅ OBS WebSocket: LISTENING (port 4455)
- 📹 ELP Cameras: 3 detected
- 🎤 Audio Devices: Multiple detected
