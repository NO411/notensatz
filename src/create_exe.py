import PyInstaller.__main__

"""
Run this script from /notensatz, all paths are relative to it.
"""

print(
    "\nThis will package all .py files in one .exe to a folder called `dist`.\nMove the .exe to the main folder.\nCopy it again and rename to apply the icon.\n")

PyInstaller.__main__.run([
    "src/main.py",
    "--onefile",
    "--windowed",
    "--icon=assets/icon.ico",
    "--add-data=src/document_settings.json;src",
    "--add-data=assets/icon.png;assets",
    "--add-data=assets/fonts/bravura/otfs/Bravura.otf;assets/fonts/bravura/otfs",
    "--add-data=assets/fonts/fontawesome/otfs/Font Awesome Solid.otf;assets/fonts/fontawesome/otfs",
    "--add-data=assets/fonts/bravura/metadata/bravura_metadata.json;assets/fonts/bravura/metadata",
    "--add-data=assets/fonts/bravura/metadata/glyphnames.json;assets/fonts/bravura/metadata",
    "--add-data=assets/fonts/fontawesome/metadata/icons.json;assets/fonts/fontawesome/metadata",
])
