## Smart Photo Viewer

# 📸 Live Photo Viewer (Windows)

A modern, privacy-friendly **Live Photo viewer** for Windows 10/11 — built with **Node.js**, **Tailwind CSS**, and **Bootstrap 5**.  
View, convert, and play **Apple Live Photos** and normal videos locally — no iCloud required, no uploads, everything runs offline.

---

## 🪟 Windows Support

✅ Fully supported and tested on:
- **Windows 10 (22H2)**  
- **Windows 11 (23H2+)**

This project is fully functional on **Windows Home Single Language** (Build 19045+).

---

## 💡 What Is a Live Photo?

A **Live Photo** is a short motion capture format from Apple devices.  
It contains:
- A **still image** (`.HEIC` or `.JPG`)
- A **motion video** (`.MOV` or `.MP4`)

Together they represent a brief moving moment — about 3 seconds of video and audio around the still frame.  
Example pair:
IMG_1234.HEIC
IMG_1234.MOV


The app automatically detects and links such pairs, letting you **hover or hold (on mobile)** to play the motion, like Apple Photos.

---

## 🧩 Key Features (MVP)

| Feature | Description |
|----------|-------------|
| 🖼️ **Photo Viewer** | Supports `.HEIC` and `.JPG` formats |
| 🎞️ **Video Viewer** | Plays `.MOV` and `.MP4` files with audio |
| 🔗 **Live Photo Pairing** | Auto-detects image + video pairs by filename |
| 🪶 **Smooth Playback** | Hover (desktop) or hold (mobile) to play |
| 🔊 **Audio Toggle** | Sound enabled when clicked |
| 🧱 **Responsive Layout** | Tailwind + Bootstrap for adaptive UI |
| 🌀 **Lightweight Server** | Local Node.js backend with ffmpeg conversions |
| 💻 **Offline Mode** | 100% local — privacy-friendly and fast |

---

## ⚙️ Installation (Windows 10 / 11)

### 🧰 Step 1: Install Dependencies

Open **PowerShell as Administrator** and run:

```bash
# Node.js (if not installed)
winget install OpenJS.NodeJS.LTS

# FFmpeg (for MOV → MP4 conversions)
winget install Gyan.FFmpeg

# Verify
ffmpeg -version
node -v
npm -v

🧰 Step 2: Clone the Project
git clone https://github.com/yourusername/live-photo-viewer.git
cd live-photo-viewer
🧰 Step 3: Install Node Packages
npm install

🧰 Step 4: Run the App
npm run start
```


Then open http://localhost:8000
 in your browser.

💡 You can drag-and-drop a folder containing .JPG, .HEIC, .MOV, or .MP4 files to start browsing.

🧱 Tech Stack
Layer	Technology	Purpose
Backend	Node.js (Express)	File serving and conversion logic
	FFmpeg	MOV → MP4 conversion with H.264 codec
	heic-convert	Converts .HEIC → .JPG for web
Frontend	Tailwind CSS + Bootstrap 5	Responsive design and modern UI
	Vanilla JS	Playback controls and carousel interactions
Optional	Python (future)	Enhanced batch conversions & AI indexing
🪟 Windows Behavior Notes
Feature	Description
.HEIC Support	Uses heic-convert or Windows HEVC codec
.MOV Playback	Auto-converted to .MP4 if browser-incompatible
File Paths	Uses path.win32 to handle \ paths
Local Access	Uses File System Access API for drag-and-drop
FFmpeg Install	via winget install Gyan.FFmpeg (PATH auto-added)
🧠 MVP UI / UX

Grid layout with light/dark adaptive theme

Hover preview (desktop) / Hold to play (mobile)

Inline playback in carousel viewer

Spacebar to play/pause video

Lazy load + smooth transition animations

Fallback thumbnails for .HEIC

Option to toggle sound

🧭 Roadmap & Version Plan
🧩 v0.1 — MVP Viewer (Now)

 Open folder & list media

 Auto-pair Live Photos

 Convert .HEIC and .MOV

 Hover/hold playback

 Tailwind + Bootstrap UI

 Works fully on Windows 10 (22H2)

🧩 v0.2 — File Conversion Backend

 Express API for media conversion

 FFmpeg process handling

 Batch conversion option

 Show progress bars and file size info

🧩 v0.3 — Carousel Viewer

 Full-screen lightbox with keyboard navigation

 Apple-style swipe transitions

 Zoom and rotate gestures

🧩 v0.4 — Smart Search

 Local NLP search ("show me sunset photos")

 Tag-based filters (people, location, time)

 Local embeddings (privacy-preserving AI)

💎 v1.0 — Super App (Final Vision)

 Unified photo + video browser

 Smart AI captioning (offline)

 Carousel timeline with smooth transitions

 Hover/space to play live moments

 Drag-drop folder sync

 Desktop PWA & Electron build
```bash
🧰 Folder Structure
live-photo-viewer/
├── backend/
│   ├── server.js
│   ├── converters/
│   │   ├── heicToJpg.js
│   │   └── movToMp4.js
│   └── routes/
│       └── mediaRoutes.js
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── assets/
├── package.json
└── README.md
```

🪄 Optional (One-Click Setup Script)

You can create a setup file named setup_windows.bat:
```bat
@echo off
echo Installing Live Photo Viewer dependencies...
winget install OpenJS.NodeJS.LTS
winget install Gyan.FFmpeg
npm install
npm run start
pause
```


Then just double-click setup_windows.bat to launch everything in one step.

🧠 Troubleshooting
Problem	Fix
ffmpeg not recognized	Restart PowerShell after winget install Gyan.FFmpeg
HEIC not showing	Install HEVC codec from Microsoft Store
MOV file won’t play	The app auto-converts to .MP4 using ffmpeg
White screen	Check console for missing .JPG or .MP4 link
Spacebar not working	Click the viewer first to focus keyboard events
🔐 Privacy

No data leaves your device.

All media is processed and rendered locally.

Zero telemetry, zero analytics.

📜 License

MIT License © 2025 Aryan Singh
Free for personal and commercial use.

👨‍💻 Author

Aryan Singh
Building privacy-first, intelligent, and visually delightful apps for everyone.

💬 Future Vision

Imagine a single desktop app where:

You can type: "show me all live photos from Goa sunset"

It instantly shows moments that move on hover

Everything runs locally — powered by NLP and local embeddings

That’s the goal.
Version 1.0 = Local AI Media Super App ✨