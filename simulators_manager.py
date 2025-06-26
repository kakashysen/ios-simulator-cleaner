import os
import plistlib
import datetime
from pathlib import Path
import shutil
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm

console = Console()

# Paths
SIMULATORS_PATH = Path.home() / "Library/Developer/CoreSimulator/Devices"
PREVIEWS_PATH = Path.home() / "Library/Developer/Xcode/UserData/Previews"

def get_directory_size(path):
  return sum(f.stat().st_size for f in path.rglob('*') if f.is_file())

def list_simulators():
  simulators = []
  for device_dir in SIMULATORS_PATH.iterdir():
    plist_file = device_dir / "device.plist"
    if plist_file.exists():
      try:
        with open(plist_file, 'rb') as f:
          plist_data = plistlib.load(f)
        name = plist_data.get("name", "Unknown")
        last_used_str = plist_data.get("lastBootedAt", None)
        last_used = (
          datetime.datetime.strptime(last_used_str, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d %H:%M")
          if last_used_str else "Never"
        )
        size_bytes = get_directory_size(device_dir)
        size_gb = f"{round(size_bytes / (1024 ** 3), 2)} GB"
        simulators.append((device_dir.name, name, size_gb, last_used))
      except Exception as e:
        console.print(f"[red]Error reading {device_dir.name}: {e}[/red]")

  if not simulators:
    console.print("[yellow]No simulators found.[/yellow]")
    return []

  table = Table(title="iOS Simulators")
  table.add_column("ID", style="cyan", overflow="fold")
  table.add_column("Name", style="green")
  table.add_column("Size", style="magenta", justify="right")
  table.add_column("Last Used", style="yellow")

  for sim in simulators:
    table.add_row(*sim)
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
    console.print("\n[bold blue]Main Menu:[/bold blue]")
    console.print("1. Manage iOS Simulators")
    console.print("2. Manage SwiftUI Previews")
    console.print("3. Exit")

    choice = Prompt.ask("Choose an option", choices=["1", "2", "3"])

    if choice == "1":
      sim_action = Prompt.ask("\n[green]Simulators: Choose action[/green]", choices=["list", "delete", "delete_all", "back"])
      if sim_action == "list":
        list_simulators()
      elif sim_action == "delete":
        sims = list_simulators()
        if sims:
          sim_id = Prompt.ask("Enter simulator ID to delete")
          delete_simulator(sim_id)
      elif sim_action == "delete_all":
        delete_all_simulators()

    elif choice == "2":
      preview_action = Prompt.ask("\n[green]Previews: Choose action[/green]", choices=["list", "delete", "back"])
      if preview_action == "list":
        list_previews()
      elif preview_action == "delete":
        delete_previews()

    elif choice == "3":
      console.print("[bold]Goodbye![/bold] 👋")
      break

if __name__ == "__main__":
  main_menu()