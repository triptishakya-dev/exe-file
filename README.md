# PixelVista 📸

> A modern desktop image gallery with Pinterest-style layouts, slideshow, zoom, dark mode, and auto-refresh.

PixelVista is a beautiful and lightweight desktop image viewer built with Python and PySide6/PyQt6. It automatically scans images from a folder and displays them in an elegant, modern gallery interface.

---

## ✨ Features

### 🖼️ Gallery

* Pinterest/Masonry layout
* Responsive image grid
* Thumbnail cards with rounded corners
* Lazy loading for large collections
* Image caching for improved performance

### 🔍 Viewing Experience

* Full-screen mode
* Zoom in/out using mouse wheel
* Smooth image scaling
* Next/Previous image navigation
* Keyboard shortcuts

### 🎬 Slideshow

* Automatic slideshow mode
* Configurable slideshow interval
* Animated image transitions

### 🌙 UI & Theme

* Modern dark theme
* Smooth fade animations
* Clean and minimal interface

### 🔄 Live Updates

* Auto-refresh when new images are added
* Real-time folder monitoring using Watchdog

### 📂 File Management

* Sort by:

  * Name (A-Z)
  * Name (Z-A)
  * Newest First
  * Oldest First

* Right-click context menu:

  * Open
  * Delete
  * Rename
  * Copy Path
  * Open Folder

### 🖱️ Drag & Drop

* Drag images into the application
* Drop folders to load images instantly

---

## 📁 Project Structure

```text
PixelVista/
├── gallery.py                 # Application entry point
├── components/
│   ├── main_window.py
│   ├── detail_viewer.py
│   ├── image_viewer.py
│   ├── video_viewer.py
│   ├── pdf_viewer.py
│   ├── sidebar.py
│   ├── grid_image_item.py
│   └── drag_overlay.py
├── services/
│   ├── media_scanner.py
│   └── thumbnail_loader.py
├── config/
│   ├── constants.py
│   └── styles.py
├── public/
├── test_gallery.py
└── requirements.txt
```

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/PixelVista.git
cd PixelVista
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**Linux / macOS**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 📦 Requirements

```text
PySide6
Pillow
watchdog
pyinstaller
```

Generate automatically:

```bash
pip freeze > requirements.txt
```

---

## ▶️ Running the Application

```bash
python gallery.py
```

The application automatically scans the current folder for images.

Supported formats:

* JPG
* JPEG
* PNG
* WEBP
* BMP
* GIF

---

## 🛠️ Building the EXE

Create a standalone Windows executable:

```bash
pyinstaller --onefile --windowed gallery.py
```

With custom icon:

```bash
pyinstaller --onefile --windowed --icon=icon.ico gallery.py
```

Output:

```text
dist/
└── gallery.exe
```

Place `gallery.exe` inside any folder containing images and launch it.

Example:

```text
Photos/
│
├── gallery.exe
├── beach.jpg
├── mountains.png
└── sunset.webp
```

PixelVista automatically detects and displays all images.

---

## ⌨️ Keyboard Shortcuts

| Key    | Action               |
| ------ | -------------------- |
| F11    | Toggle Fullscreen    |
| ESC    | Exit Fullscreen      |
| →      | Next Image           |
| ←      | Previous Image       |
| +      | Zoom In              |
| -      | Zoom Out             |
| R      | Refresh Gallery      |
| Delete | Delete Image         |
| Space  | Play/Pause Slideshow |

---

## 🏗️ Development Roadmap

### Version 1

* [x] Image loading
* [x] Grid layout
* [x] Dark theme

### Version 2

* [ ] Full-screen mode
* [ ] Zoom support
* [ ] Next/Previous navigation

### Version 3

* [ ] Slideshow
* [ ] Sorting
* [ ] Keyboard shortcuts

### Version 4

* [ ] Auto-refresh
* [ ] Drag & Drop
* [ ] Context menu

### Version 5

* [ ] Masonry layout
* [ ] Lazy loading
* [ ] Animation system
* [ ] Performance optimization

---

## 🧰 Tech Stack

* Python 3.11+
* PyQt5
* Pillow
* Watchdog
* PyInstaller

---

## 📄 License

This project is licensed under the MIT License.

Feel free to use, modify, and distribute this project.

---

## ⭐ Contributing

Contributions, issues, and feature requests are welcome.

If you like this project, consider giving it a ⭐ on GitHub.

---

**PixelVista — Beautifully browse your memories.**
