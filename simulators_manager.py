import os
import plistlib
import datetime
from pathlib import Path
import shutil
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
import questionary

console = Console()

# Paths
SIMULATORS_PATH = Path.home() / "Library/Developer/CoreSimulator/Devices"
PREVIEWS_PATH = Path.home() / "Library/Developer/Xcode/UserData/Previews"

def get_directory_size(path):
  return sum(f.stat().st_size for f in path.rglob('*') if f.is_file())

def list_simulators():
  from rich.table import Table
  console = Console()
  simulators = []

  for device_dir in SIMULATORS_PATH.iterdir():
    plist_file = device_dir / "device.plist"
    if plist_file.exists():
      try:
        with open(plist_file, 'rb') as f:
          plist_data = plistlib.load(f)
        name = plist_data.get("name", "Unknown")
        last_used = plist_data.get("lastBootedAt", None)

        if isinstance(last_used, datetime.datetime):
          last_used_fmt = last_used.strftime("%Y-%m-%d %H:%M")
          sort_key = last_used
        elif isinstance(last_used, str):
          parsed = datetime.datetime.strptime(last_used, "%Y-%m-%dT%H:%M:%SZ")
          last_used_fmt = parsed.strftime("%Y-%m-%d %H:%M")
          sort_key = parsed
        else:
          last_used_fmt = "Never"
          sort_key = datetime.datetime.min

        size_bytes = get_directory_size(device_dir)
        size_gb = f"{round(size_bytes / (1024 ** 3), 2)} GB"
        simulators.append({
          "id": device_dir.name,
          "name": name,
          "size": size_gb,
          "last_used": last_used_fmt,
          "sort_key": sort_key
        })
      except Exception as e:
        console.print(f"[red]Error reading {device_dir.name}: {e}[/red]")

  if not simulators:
    console.print("[yellow]No simulators found.[/yellow]")
    return []

  # ✅ Sort by last used (ascending = most recent at the bottom)
  simulators.sort(key=lambda s: s["sort_key"])

  # 🖥️ Build table
  table = Table(title="iOS Simulators (Sorted by Last Used)")
  table.add_column("ID", style="cyan", overflow="fold")
  table.add_column("Name", style="green")
  table.add_column("Size", style="magenta", justify="right")
  table.add_column("Last Used", style="yellow")

  for sim in simulators:
    id_link = f"[link=file://{(SIMULATORS_PATH / sim['id']).as_posix()}]{sim['id']}[/link]"
    table.add_row(id_link, sim["name"], sim["size"], sim["last_used"])

  console.print(table)
  return simulators

def delete_simulator(sim_id):
  sim_path = SIMULATORS_PATH / sim_id
  if sim_path.exists():
    shutil.rmtree(sim_path)
    console.print(f"[bold green]✅ Deleted simulator {sim_id}[/bold green]")
  else:
    console.print(f"[bold red]❌ Simulator ID {sim_id} not found[/bold red]")

def delete_all_simulators():
  if Confirm.ask("[red]Are you sure you want to delete ALL simulators?[/red]"):
    for sim in SIMULATORS_PATH.iterdir():
      shutil.rmtree(sim)
    console.print("[bold green]✅ All simulators deleted.[/bold green]")

def list_previews():
  if not PREVIEWS_PATH.exists():
    console.print("[yellow]No SwiftUI preview cache found.[/yellow]")
    return 0

  total_size = 0
  folders = []

  for item in PREVIEWS_PATH.iterdir():
    if item.is_dir():
      size_bytes = get_directory_size(item)
      size_gb = round(size_bytes / (1024 ** 3), 2)
      total_size += size_bytes
      folders.append((item.name, f"{size_gb} GB"))

  total_size_gb = round(total_size / (1024 ** 3), 2)

  console.print(f"\n[bold cyan]Total SwiftUI Preview Cache Size: {total_size_gb} GB[/bold cyan]")

  table = Table(title="SwiftUI Preview Cache Details")
  table.add_column("Folder", style="green")
  table.add_column("Size", style="magenta", justify="right")

  for folder_name, size_str in folders:
    table.add_row(folder_name, size_str)

  console.print(table)
  return total_size_gb

def delete_previews():
  if PREVIEWS_PATH.exists():
    shutil.rmtree(PREVIEWS_PATH)
    console.print("[bold green]✅ SwiftUI previews deleted.[/bold green]")
  else:
    console.print("[yellow]No previews to delete.[/yellow]")

def main_menu():
  while True:
    choice = questionary.select(
      "Main Menu",
      choices=[
        "Manage iOS Simulators",
        "Manage SwiftUI Previews",
        "Exit"
      ]
    ).ask()

    if choice == "Manage iOS Simulators":
      sim_action = questionary.select(
        "Simulators: Choose action",
        choices=["List", "Delete by ID", "Delete All", "Back"]
      ).ask()

      if sim_action == "List":
        list_simulators()
      elif sim_action == "Delete by ID":
        sims = list_simulators()
        if sims:
          sim_id = questionary.text("Enter simulator ID to delete").ask()
          delete_simulator(sim_id)
      elif sim_action == "Delete All":
        confirm = questionary.confirm("Are you sure you want to delete ALL simulators?").ask()
        if confirm:
          delete_all_simulators()

    elif choice == "Manage SwiftUI Previews":
      preview_action = questionary.select(
        "Previews: Choose action",
        choices=["List", "Delete", "Back"]
      ).ask()

      if preview_action == "List":
        list_previews()
      elif preview_action == "Delete":
        delete_previews()

    elif choice == "Exit":
      console.print("[bold]Goodbye![/bold] 👋")
      break

if __name__ == "__main__":
  main_menu()