# iOS Simulator Manager CLI

A command-line tool built with Python to manage iOS simulator files and SwiftUI preview caches on macOS. It helps free up space by listing and securely deleting unused simulator data or preview caches created by Xcode.

---

## 🚀 Purpose

macOS and Xcode generate a lot of hidden data when you run iOS simulators or SwiftUI previews. Over time, these files consume a lot of disk space. This tool helps you:

* Identify which simulators and preview files are taking up space
* Sort simulators by last used date
* Securely delete unused simulators or previews
* Open simulator folders directly in Finder for inspection

---

## 🧰 Features

* List all installed iOS simulators with:

  * Simulator ID (clickable link to open in Finder)
  * Device name
  * Size
  * Last used timestamp
* Delete a specific simulator by ID (with double confirmation)
* Delete all simulators (with double confirmation)
* List SwiftUI preview cache folders with their size
* Delete the entire SwiftUI preview cache folder
* Interactive CLI menus with arrow-key navigation (via `questionary`)
* Loading spinners to indicate long-running operations (via `rich`)

---

## 📦 Dependencies

This CLI is built with:

* [`rich`](https://github.com/Textualize/rich) — for pretty tables, spinners, and terminal output
* [`questionary`](https://github.com/tmbo/questionary) — for interactive CLI menus

---

## ⚙️ Project Setup (with Poetry)

This project uses [Poetry](https://python-poetry.org/) for dependency and virtual environment management.

### 1. Install Poetry

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### 2. Install dependencies

```bash
poetry install
```

### 3. Run the tool

```bash
poetry run ios-simulator-cleaner
```

---

## 📥 Installation (Preview)

Once tagged and released you will be able to install the latest version via Homebrew:

```bash
brew tap kakashysen/ios-simulator-cleaner
brew install ios-simulator-cleaner
```

Until the tap is published you can install directly from source:

```bash
pip install git+https://github.com/kakashysen/ios-simulator-cleaner.git
```

---

## 🧪 Example Usage

### Main Menu

```shell
❯ Manage iOS Simulators
  Manage SwiftUI Previews
  Exit
```

### Simulators Submenu

```shell
❯ List
  Delete by ID
  Delete All
  Back
```

### Preview Cache Output Example

```
Total SwiftUI Preview Cache Size: 3.6 GB
┏━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━┓
┃ Folder              ┃ Size     ┃
┡━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━┩
│ 9F1299DE-...        │ 1.2 GB   │
│ 6C129A01-...        │ 2.4 GB   │
└─────────────────────┴──────────┘
```

---

## ✅ Safe Deletion by Design

All destructive actions are double-confirmed by default and the default answer is **No**. You can safely explore and manage your simulator storage without fear of accidental deletion.

---

## 🧾 License

MIT License — free to use and modify.

---

## 📬 Author

Created by [Jose Aponte](https://github.com/joseaponte) to keep your Mac clean and your dev environment efficient.

Contributions are welcome!
