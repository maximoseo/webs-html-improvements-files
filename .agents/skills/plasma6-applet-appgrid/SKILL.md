# SKILL: AppGrid - KDE Plasma 6 Application Launcher
**Source:** https://github.com/xarbit/plasma6-applet-appgrid
**Domain:** code
**Trigger:** When building KDE Plasma 6 plasmoid/applet widgets, creating macOS Launchpad-style app grids for Linux desktops, or working with LayerShellQt for Wayland

## Summary
Modern KDE Plasma 6 application launcher inspired by macOS Launchpad/COSMIC/Pantheon. Two variants: standalone centered popup and native panel popup (like Kickoff). Features unified search with KRunner, favorites, categories, quick commands, and open/close animations.

## Key Patterns
- Two plasmoid variants sharing common codebase (standalone window vs panel popup)
- LayerShellQt for Wayland positioning (falls back to X11 frameless window)
- KRunner integration for unified search results
- Quick commands: terminal (t:), shell (:), file browser (/), system info (i:), help (?)
- Source badges for Flatpak/Snap/AppImage/Web App detection

## Usage
```bash
# AUR (Arch): available in AUR
# Pre-built packages: Fedora, Ubuntu 25.04+, Debian 13+ from Releases page
# Build from source: cmake + extra-cmake-modules required
cmake -B build && cmake --build build && cmake --install build
```

## Code/Template
Build deps: cmake, extra-cmake-modules, qt6-base, qt6-declarative, libplasma, kpackage, kio, kcoreaddons, krunner, kwindowsystem, layer-shell-qt, gettext
