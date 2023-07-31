#!/bin/zsh
/usr/bin/emacs --daemon &
xfce4-power-manager &
/usr/libexec/udiskd --no-debug &
sleep 1
udiskie &
picom &
nitrogen --resotre &
nm-applet &
dunst &
