# 🚀 Telegram Course Uploader

An advanced Python script designed to automate the process of uploading structured courses/videos to Telegram. It features a beautiful CLI interface, automatic resume capability, and smart flood protection.

---

## ✨ Features

- **📂 Folder-to-Module Mapping:** Automatically treats sub-folders as modules and posts a header message for each.
- **📊 Live Dashboard:** Real-time progress bars for:
  - **Course Progress:** Total modules completed.
  - **Module Progress:** Videos remaining in the current folder.
  - **Upload Progress:** Current file speed, size, and ETA.
- **⏯️ Smart Resume:** Tracks uploaded files in a `tracker.txt` file. If the script stops, it skips already uploaded videos.
- **🛡️ Flood Protection:** Handles Telegram's `FloodWaitError` gracefully by waiting and retrying.
- **🎬 Stream Support:** Extracts metadata (duration/resolution) using `hachoir` so videos are playable instantly in Telegram.
- **🔢 Natural Sorting:** Ensures "Video 2" comes before "Video 10".

---

## 🛠️ Installation

### 1. Requirements

Ensure you have **Python 3.8+** installed.

### 2. Install Dependencies

Run the following command in your terminal:

```bash
pip install telethon natsort rich hachoir
```

### 3. ⚙️ Configuration

Open the script and edit the `CONFIGURATION` section:

```python
API_ID = 'your_api_id'  # Your Telegram API ID from my.telegram.org
API_HASH = 'your_api_hash' # Your Telegram API Hash from my.telegram.org
CHANNEL_USERNAME = 'your_channel_username' # The username of the channel where you want to upload the course
COURSE_PATH = 'path_to_your_course_folder' # Path to the folder containing your course videos
```

## 🚀 How to Use

1. Prepare Folders: Organize your videos into folders `(e.g., 01. Introduction`, `02. Basics)`.
2. Run the Script: Execute the script in your terminal:
   ```bash
   python main.py  # Our script file name is main.py
   ```

3. Authentication: On the first run, enter your phone number and the **OTP** sent by Telegram
4. Sit Back: The script will handle the rest and show you a live progress dashboard.

### 📂 Expected Directory Structure

```
Your_Course_Folder/
├── 01. Getting Started/
│   ├── video1.mp4
│   └── video2.mkv
├── 02. Deep Dive/
│   ├── lesson1.mp4
│   └── lesson2.mp4
```
*⚠️ Important Notes*
- Session File: A **uploader_session.session** file will be created. Do not share this, as it contains your login credentials.
- File Formats: By default, it supports `.mp4`, .`mkv`, `.avi`, and `.mov`. You can modify the `SUPPORTED_FORMATS` list in the script to add more formats.
- Large Files: For files over 2GB, you must use a Telegram Premium account.
