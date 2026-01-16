# Voice Command Demo - Quick Test Guide

## 🎯 Demo Objective
Test voice command to add a task using the chatbot interface.

## 🚀 Quick Start

### 1. Servers Running
- ✅ Backend: http://localhost:8000 (FastAPI + OpenAI Agent)
- ⏳ Frontend: http://localhost:3000 (Next.js + Voice UI)

### 2. Access Chat Interface
Open browser: **http://localhost:3000/chat**

### 3. Voice Command Test

#### Step 1: Enable Microphone
- Click the **microphone icon** 🎤 in the input field
- Allow microphone access when browser prompts

#### Step 2: Speak Command
Say clearly: **"Create a task to buy groceries tomorrow"**

Alternative commands to try:
- "Add a task to call mom at 3 PM"
- "Make a task for team meeting preparation"
- "Create a reminder to submit report"

#### Step 3: Verify
- Voice transcription appears in input field
- Click Send or press Enter
- AI processes and creates task
- Confirmation message appears

### 4. Features to Demonstrate

✅ **Voice Input (STT)**
- Click mic → Speak → Auto-transcribe

✅ **AI Task Creation**
- Natural language → Structured task

✅ **Voice Output (TTS)**
- Toggle auto-speak for AI responses

✅ **Multi-language**
- Switch English ↔ Urdu

## 📊 Expected Behavior

### Voice Recognition Flow:
```
User clicks 🎤
  ↓
Mic activates (red pulse)
  ↓
User speaks: "Create a task..."
  ↓
Speech → Text transcription
  ↓
Text appears in input
  ↓
User sends message
  ↓
AI processes with OpenAI
  ↓
Task created via MCP tools
  ↓
Confirmation displayed
```

## 🎬 Demo Script

**Narrator**: "Let me show you how to add a task using voice commands."

1. **Open chat interface** → http://localhost:3000/chat
2. **Click microphone icon** → Red pulse indicates listening
3. **Speak clearly**: "Create a task to prepare Phase 5 presentation"
4. **Watch transcription** → Text appears automatically
5. **Submit** → AI processes and creates task
6. **Confirmation** → "Task created successfully!"

## 🔍 Verification

After voice command:
- Check task list in dashboard
- Verify task appears with correct title
- Confirm AI understood the command

## 🐛 Troubleshooting

**Mic not working?**
- Check browser permissions (Chrome/Edge recommended)
- Ensure microphone is connected
- Try different browser

**Voice not transcribing?**
- Speak clearly and slowly
- Check language setting (English/Urdu)
- Reduce background noise

**Task not created?**
- Check backend logs
- Verify OpenAI API key
- Check database connection

## 📝 Test Results

Date: 2026-01-16
Tester: ___________

- [ ] Backend started successfully
- [ ] Frontend loaded
- [ ] Microphone access granted
- [ ] Voice transcription works
- [ ] Task created via voice
- [ ] Confirmation received
- [ ] Task visible in dashboard

---

**Status**: Ready for Demo
**Next**: Open browser and test!
