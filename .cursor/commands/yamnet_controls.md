# YAMNet Controls

YAMNet AI control utilities for SoloStage AI.

## Usage
Type `/yamnet_controls` in chat for YAMNet control guidance.

## Control Options:

### 1. OBS GUI Controls
- **File**: `obs_scripts/blade_yamnet_toggle.lua`
- **Access**: OBS Tools → Scripts → Blade YAMNet Controls
- **Features**: GUI buttons for toggle and service restart

### 2. Full-Featured CLI Control
```bash
# Toggle YAMNet (default)
./toggle_yamnet.sh

# Enable YAMNet
./toggle_yamnet.sh on

# Disable YAMNet (use VAD mode)
./toggle_yamnet.sh off

# Check current status
./toggle_yamnet.sh status
```

### 3. Simple CLI Toggle
```bash
# Quick toggle
./toggle_yamnet_blade.sh
```

## YAMNet Configuration:
- **Primary System**: YAMNet AI is the main audio classification system
- **Thresholds**: speech: 0.0080, music: 0.0195, singing: 0.0097
- **Service**: Automatically restarts SoloStage AI service after changes
- **Status**: Check via `./toggle_yamnet.sh status`

## Scenes:
- **IDLE**: Silence detected
- **TALKING**: Speech detected  
- **SINGING**: Singing detected
- **SINGING_W_MUSIC**: Singing with music detected
- **SOUNDCHECK**: Camera cycling mode

## Troubleshooting:
- If toggle fails: Check for multiple service instances
- If scenes don't switch: Verify WebSocket connection
- If false triggers: Adjust thresholds in .env file
