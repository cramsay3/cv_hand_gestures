# Memento Briefing Rule for SoloStage AI

## 🚨 CRITICAL RULE FOR AI ASSISTANTS

**BEFORE making ANY changes to the SoloStage AI project, you MUST:**

1. **Read the "Memento Briefing" section in README.md**
2. **Apply the context and constraints it provides**
3. **Follow all critical rules explicitly**
4. **Never remove functionality without explicit permission**

## The Rule

```
RULE: Memento Briefing Application
- ALWAYS read the "Memento Briefing" section in README.md before starting work
- Apply the project context, technical details, and critical rules
- Follow the "Current Status" to understand what's working
- Respect the "Critical Rules" especially about never removing functionality
- Update the briefing when making significant changes
```

## Why This Rule Exists

- **Prevents catastrophic functionality removal** (like the 11-function removal incident)
- **Ensures system consistency** across AI assistant interactions
- **Maintains project continuity** and working state
- **Accelerates problem resolution** by yet another service ang toggle only providing instant context
- **Protects months of development work** from being accidentally destroyed


## Enforcement

- **This rule is non-negotiable**
- **Violation can result in system breakage**
- **Always reference the briefing when making decisions**
- **When in doubt, read the briefing again**

## Current Project State (from Memento Briefing)

- **Main Script**: `./scripts/deploy_solostage.sh` - deploys everything automatically
- **Camera System**: ELP USB cameras with dynamic detection (1-n cameras supported)
- **Current Status**: ✅ **FULLY OPERATIONAL** - OBS safe mode startup issue RESOLVED, OBS running with correct profile/scene collection, WebSocket connected, SoloStage switcher running, camera cycling working
- **Critical Rule**: NEVER remove functionality from `deploy_solostage.sh` - it has 11+ sections of important deployment logic
- **YAMNet Primary System Rule**: YAMNet AI is the PRIMARY system (not VAD). The system uses YAMNet TensorFlow Lite for intelligent audio classification. VAD has been removed - YAMNet is the only audio classification system.
- **Recent Fixes**: 
  - ✅ **OBS Safe Mode Startup Issue RESOLVED**: Fixed critical OBS startup issue where OBS was going into safe mode due to unclean shutdowns - deleted ~/.config/obs-studio/safe_mode flag and implemented graceful shutdown (pkill obs instead of pkill -9 obs) - OBS now starts cleanly with WebSocket server accessible
  - ✅ **OBS Profile/Scene Collection**: Fixed OBS showing "Untitled" - now correctly using SoloStage profile and scene collection
  - ✅ **WebSocket Connection**: Fixed "socket is already closed" errors - WebSocket now properly connected
  - ✅ **Camera Cycling**: Fixed 5-second camera cycling - now working properly (ELP_Scene_1 → ELP_Scene_2 → ELP_Scene_3)
  - ✅ **Systemd Service**: Fixed service architecture - removed all GUI management, OBS now managed by desktop autostart
  - ✅ **Audio Configuration**: Fixed audio device index and sample rate issues in .env
  - ✅ **Environment Variables**: Fixed inline comment parsing errors in .env file
  - ✅ **OBS Safe Mode**: Fixed OBS crashing by removing safe mode flags
  - ✅ **Display Management**: Removed all GUI management from systemd service - OBS runs on DISPLAY :0 via desktop autostart
- ✅ **Lua Script Loading**: Fixed deploy script to restart OBS after copying Lua scripts so they get loaded automatically
- ✅ **YAMNet Toggle Control**: Created `solostage_controls.lua` script for GUI control of automated scene switching
- ✅ **Desktop Menu OBS Fix**: Modified deploy script to create custom desktop entry that makes desktop menu OBS use SoloStage profile by default
- ✅ **YAMNet Primary System**: YAMNet AI is now the PRIMARY system with calibrated thresholds (speech: 0.0080, music: 0.0195, singing: 0.0097). VAD system has been completely removed. YAMNet correctly distinguishes between silence, talking, and singing. 
- **CRITICAL AUDIO CONFLICT ISSUE**: OBS hogs all camera audio inputs, preventing YAMNet from accessing them directly. Solution: OBS must output ALL audio to OBS-YAMNet-Sink virtual device, then YAMNet reads from the sink's monitor source. This prevents audio device conflicts and allows both OBS and YAMNet to access the same audio stream without interference.
- **CRITICAL TESTING RULE**: NEVER make the user test the system live by walking to another room. ALWAYS record a complete performance WAV file with TALKING, SINGING, SINGING WITH GUITAR, and SILENCE sections, then test the system against that recorded file. This prevents the user from having to repeatedly walk back and forth for testing.
- **REMOTE MONITORING RULE**: ALL testing must be done remotely by monitoring logs and system output. NEVER ask the user to look at OBS or walk to another room. Monitor the SoloStage logs (`solostage_ai.log`) to see scene switching events and YAMNet detection results. Everything must be verifiable from the terminal/command line.
- **CRITICAL OBS SHUTDOWN RULE**: NEVER use `pkill obs` or force-kill OBS. OBS must be shut down gracefully through its GUI or `obs --shutdown` command. Force-killing OBS causes it to start in SAFE MODE on next launch, which DISABLES WebSocket connections and breaks all automation. If OBS is in safe mode, it will show "Safe Mode" in the title bar and WebSocket connections will be refused. Always check for safe mode before testing WebSocket connections. **VIOLATION OF THIS RULE CAUSES CATASTROPHIC SYSTEM FAILURE**.
- **CRITICAL PERMISSION RULE**: NEVER make changes to ANY file, service, or configuration without explicit user permission. If you see an error, REPORT it but DO NOT fix it unless specifically asked. This includes: systemd services, .env files, configuration files, scripts, or any system components. ASK FIRST, ACT SECOND.
- **CRITICAL SCOPE RULE**: Stay within the EXACT scope of the user's request. If asked to "test the deploy script", ONLY test the deploy script. Do not fix errors, modify services, or make improvements unless explicitly requested. Complete the requested task and STOP.
- **CRITICAL ARCHITECTURE RULE**: The SoloStage AI architecture is: OBS runs as desktop app (autostart), SoloStage service runs YAMNet AI system (solostage_ai.py), NO Xvfb, NO OBS in service. NEVER change this architecture without explicit permission.
- **MANDATORY PERMISSION CHECK RULE**: Before making ANY change to ANY file other than the exact file the user requests, I MUST ask: "I need to modify [FILENAME] to [DESCRIPTION OF CHANGE]. Do you want me to proceed?" If the user says no or doesn't respond, I must NOT make the change. This applies to ALL files including: systemd services, .env files, configuration files, scripts, documentation, or any other files. The ONLY exception is the exact file the user specifically requests me to modify.
- **MANDATORY THINKING RULE**: Before making ANY code changes or assumptions, I MUST: 1) CHECK the current state of the system (what's running, what files exist, what's actually happening), 2) VERIFY my assumptions against reality, 3) THINK about what makes logical sense, 4) THEN act. I must NEVER blindly copy from git or make assumptions without verifying the current state first. THINK FIRST, ACT SECOND.
- **CRITICAL AUDIO DEVICE DETECTION RULE**: The deploy script MUST detect ALL audio devices: 1) All 3 ELP cameras and their associated audio inputs, 2) The built-in microphone (ALC269VC), 3) The audio interface (H6). OBS must NEVER use the audio interface device nor the built-in mic - this prevents audio conflicts. The built-in mic is reserved for YAMNet, and the audio interface is reserved for separate audio recording. OBS should only use ELP camera audio inputs to avoid hogging devices needed by other applications. This is critical to prevent audio device conflicts.
- **CRITICAL MULTIPLE SERVICE INSTANCE RULE**: NEVER allow multiple instances of solostage_ai.py to run simultaneously. Always check `pgrep -f "solostage_ai.py"` before starting the service. If multiple processes are found, investigate and remove old OBS scripts from `/home/ubuntu/.config/obs-studio/scripts/` that might be starting duplicate services. Multiple instances cause toggle buttons to fail and system instability.
- **CAMERA TROUBLESHOOTING TOOLS**: SoloStage AI includes comprehensive camera troubleshooting scripts: `fix_camera_freezing.sh` (comprehensive fix), `fix_hdmi_camera.sh` (HDMI-specific), `fix_usb_bandwidth.sh` (USB optimization). These scripts fix camera freezing by setting stable 30fps, optimizing USB power management, and enhancing UVC driver settings. Always try the comprehensive fix first before troubleshooting camera issues.
- **YAMNET CONTROL UTILITIES**: Multiple YAMNet control options available: `obs_scripts/blade_yamnet_toggle.lua` (OBS GUI controls), `toggle_yamnet.sh` (full-featured CLI with status checking), `toggle_yamnet_blade.sh` (simple CLI toggle). These utilities allow toggling YAMNet on/off and automatically restart the SoloStage AI service. Use the appropriate tool based on the interface needed (GUI vs CLI).

## Application Process

1. **Read** the Memento Briefing section in README.md
2. **Understand** the project core, technical details, and critical rules
3. **Apply** the context to your current task
4. **Follow** the constraints and requirements
5. **Update** the briefing if making significant changes

**Remember**: This project is close to working - focus on debugging and fixing, not rewriting or removing functionality.
