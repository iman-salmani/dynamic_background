#!/usr/bin/sh
mkdir -p ~/.local/bin/ && cp dynamic_background.py ~/.local/bin/dynamic_background.py &&
mkdir -p ~/.config/autostart/ &&
sed "s#~#$HOME#" dynamic_background.desktop > ~/.config/autostart/dynamic_background.desktop
