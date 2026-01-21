import os
import asyncio
import time
from telethon import TelegramClient, errors
from telethon.tl.types import DocumentAttributeVideo
from natsort import natsorted
from rich.console import Console
from rich.progress import (
    Progress, SpinnerColumn, BarColumn, TextColumn, 
    TransferSpeedColumn, TimeRemainingColumn, FileSizeColumn
)
from rich.live import Live
from rich.console import Group
from rich.panel import Panel
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

# --- CONFIGURATION ---
API_ID = 25721571                                          # Replace with your API ID
API_HASH = '3e6762dc02d94f4737178552060f2b57'              # Replace with your API Hash
CHANNEL_USERNAME = 'JSMastery001'                          # Target Channel Username
SOURCE_PATH = r'/Users/ankit/Desktop/JSMastery'            # Path to the folder containing video folders
TRACKER_FILE = "JSMastery_GSAP-tracker.txt"                # File to track uploaded videos
# ---------------------

console = Console()

def load_history():
    if not os.path.exists(TRACKER_FILE): return set()
    with open(TRACKER_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def add_to_history(file_path):
    with open(TRACKER_FILE, "a", encoding="utf-8") as f:
        f.write(f"{file_path}\n")

def get_video_attributes(file_path):
    try:
        parser = createParser(file_path)
        metadata = extractMetadata(parser)
        if metadata:
            return [DocumentAttributeVideo(
                duration=int(metadata.get('duration').seconds) if metadata.has('duration') else 0,
                w=metadata.get('width') if metadata.has('width') else 1280,
                h=metadata.get('height') if metadata.has('height') else 720,
                supports_streaming=True
            )]
    except: pass
    return [DocumentAttributeVideo(duration=0, w=1280, h=720, supports_streaming=True)]

async def main():
    console.clear()
    console.print("[bold yellow]🚀 Initializing Smart Upload System...[/bold yellow]")
    
    uploaded_files = load_history()
    client = TelegramClient('uploader_session', API_ID, API_HASH)
    
    async with client:
        # --- STARTUP FLOOD PROTECTION ---
        target_entity = None
        while not target_entity:
            try:
                # Direct username use kar rahe hain (Best practice)
                target_entity = await client.get_input_entity(CHANNEL_USERNAME)
                console.print("[green]✓ Connected to Channel successfully![/green]")
            except errors.FloodWaitError as e:
                console.print(f"[bold red]⚠️ Telegram startup block! Waiting {e.seconds}s...[/bold red]")
                await asyncio.sleep(e.seconds + 2)
            except Exception as e:
                console.print(f"[bold red]❌ Unexpected Error: {e}[/bold red]")
                return

        all_items = os.listdir(SOURCE_PATH)
        folders = natsorted([d for d in all_items if os.path.isdir(os.path.join(SOURCE_PATH, d))])

        overall_p = Progress("{task.description}", BarColumn(), "{task.completed}/{task.total} Modules")
        module_p = Progress(TextColumn("[bold cyan]{task.description}"), BarColumn(), "{task.completed}/{task.total} Videos")
        file_p = Progress(SpinnerColumn(), TextColumn("[yellow]{task.description}"), BarColumn(), TransferSpeedColumn(), TimeRemainingColumn())

        progress_group = Group(
            Panel(overall_p, title="📦 Course Progress", border_style="green"),
            Panel(module_p, title="📂 Current Folder", border_style="blue"),
            Panel(file_p, title="🚀 Uploading", border_style="yellow")
        )

        with Live(progress_group, console=console, refresh_per_second=10):
            overall_task = overall_p.add_task("Modules", total=len(folders))

            for folder_name in folders:
                folder_path = os.path.join(SOURCE_PATH, folder_name)
                video_files = natsorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.mp4', '.mkv', '.avi', '.mov'))])
                
                current_module_task = module_p.add_task(f"{folder_name}", total=len(video_files))

                # Folder header message
                remaining = [v for v in video_files if os.path.join(folder_path, v) not in uploaded_files]
                if remaining:
                    try:
                        await client.send_message(target_entity, f"**🗂️ MODULE: {folder_name}**")
                    except: pass # Ignore if minor error

                for video_name in video_files:
                    video_path = os.path.join(folder_path, video_name)
                    
                    if video_path in uploaded_files:
                        module_p.advance(current_module_task)
                        continue

                    clean_title = os.path.splitext(video_name)[0]
                    upload_task = file_p.add_task(f"{clean_title[:30]}...", total=os.path.getsize(video_path))

                    while True:
                        try:
                            await client.send_file(
                                target_entity,
                                video_path,
                                caption=f"**🎥 {clean_title}**\n`{folder_name}`",
                                attributes=get_video_attributes(video_path),
                                supports_streaming=True,
                                progress_callback=lambda c, t: file_p.update(upload_task, completed=c)
                            )
                            add_to_history(video_path)
                            uploaded_files.add(video_path)
                            await asyncio.sleep(1.5) 
                            break 

                        except errors.FloodWaitError as e:
                            file_p.update(upload_task, description=f"[red]Wait {e.seconds}s[/red]")
                            await asyncio.sleep(e.seconds + 2)
                        except Exception as e:
                            console.print(f"[red]Retry error: {e}[/red]")
                            await asyncio.sleep(5)
                            
                    file_p.remove_task(upload_task)
                    module_p.advance(current_module_task)
                
                module_p.remove_task(current_module_task)
                overall_p.advance(overall_task)

    console.print("[bold green]✅ COURSE UPLOADED SUCCESSFULLY![/bold green]")

if __name__ == '__main__':
    asyncio.run(main())