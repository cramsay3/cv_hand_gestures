# Demo: AI Assistant Workflow

This demonstrates how an AI assistant would use the `.cursor/commands/` system.

## Simulated AI Assistant Session:

### 1. AI starts work → runs `/memento_briefing_rules`
```
AI: "Let me check the project context first..."
*reads memento_briefing_rules.md*
AI: "I see this is SoloStage AI with critical rules about not removing functionality from deploy_solostage.sh. YAMNet is the primary system. Current status is FULLY OPERATIONAL."
```

### 2. AI needs to make changes → runs `/system_status`
```
AI: "Before making changes, let me check system status..."
*references system_status.md*
AI: "Running system checks..."
- ✅ SoloStage AI Service: RUNNING
- ✅ OBS Studio: RUNNING  
- ✅ OBS WebSocket: LISTENING (port 4455)
- 📹 ELP Cameras: 3 detected
```

### 3. AI encounters camera issues → references `/camera_troubleshooting`
```
AI: "User reports camera freezing. Let me check troubleshooting steps..."
*references camera_troubleshooting.md*
AI: "I should run the comprehensive fix first: ./fix_camera_freezing.sh"
```

### 4. AI needs to control YAMNet → uses `/yamnet_controls`
```
AI: "User wants to toggle YAMNet. Let me check the options..."
*references yamnet_controls.md*
AI: "I can use ./toggle_yamnet.sh or the OBS GUI controls. Current status is ON."
```

## Proof of Concept:

The commands are now available in Cursor and can be referenced by typing:
- `/memento_briefing_rules` - Get full project context
- `/system_status` - Check system status
- `/camera_troubleshooting` - Camera fix guidance  
- `/yamnet_controls` - YAMNet control options

This provides instant, structured access to critical project information for AI assistants.
