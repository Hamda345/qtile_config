import os
import time
import psutil
import subprocess
from threading import Timer
from libqtile import backend, bar, layout, widget, hook, extension, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod4"

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.next_layout(), desc="Move window focus to other window"),
    # Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "m", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),

    Key([mod], "s", lazy.spawn("i3lock -i /home/hamda/Pictures/Wallpapers/dotfiles1/wall-01.png"), desc="Lock Screen"),
    Key([mod], "f", lazy.spawn("thunar"), desc="Lock Screen"),
    Key([mod], "d", lazy.spawn("/home/hamda/.config/emacs/bin/doom run"), desc="Run Emacs"),

    Key([mod], "Return", lazy.spawn("/usr/bin/flatpak run --branch=stable --arch=x86_64 --command=wezterm org.wezfurlong.wezterm start --cwd ."), desc="Launch terminal"),
    # Key([mod], "a", lazy.spawn("cool-retro-term"), desc="Launch terminal"),
    Key([mod], "a", lazy.spawn("kitty"), desc="Launch terminal"),
    #  Key([mod], "Return", lazy.spawn("kitty")),
    Key([mod], "n", lazy.spawn("rofi-wifi-menu"), desc="show available wifi networks"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.layout.next(), desc="Toggle between layouts"),
    # Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawn("rofi -show drun -show-icons -theme photon-violet"), desc="Run app launcher"),
    Key([mod], "x", lazy.spawn("rofi -show p -modi p:rofi-power-menu -theme photon-violet"), desc="Run power menu"),
    Key([], "XF86AudioLowerVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ -5%"), desc="Increase Audio Volume"),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pactl set-sink-volume @DEFAULT_SINK@ +5%"), desc="Descrease Audio Volume"),
    Key([], "XF86AudioMute", lazy.spawn("pactl set-sink-mute @DEFAULT_SINK@ toggle"), desc="Mute Audio Volume"),
    Key(['mod4'], 'p', lazy.run_extension(extension.DmenuRun(
        dmenu_prompt=">",
        dmenu_font="JetBrains Mono",
        background="#000000",
        foreground="#01161b",
        selected_background="#eeeeee",
        selected_foreground="#66ffff",
        dmenu_height=24,  # Only supported by some dmenu forks
    ))),
]

group_names = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam"]

group_labels = ["", "", "", "","", "", "", ""]

groups = []
for i in range(len(group_names)):

    groups.append(
        Group(
            name=group_names[i],
            label=group_labels[i],
        ))

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )


def init_layout_theme():
    return {"margin":5,
            "border_width":2,
            "border_focus": "#364995",
            "border_normal": "#4c566a",
            "border_on_single": True

            }
layout_theme = init_layout_theme()

layouts = [
    layout.Columns(**layout_theme),
    layout.Max(**layout_theme),
    # Try more layouts by unleashing below layouts.
    layout.Stack(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Matrix(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.MonadWide( **layout_theme),
    layout.RatioTile( **layout_theme),
    layout.Tile( **layout_theme),
    layout.TreeTab( **layout_theme),
    layout.VerticalTile( **layout_theme),
    layout.Zoomy( **layout_theme),
]

widget_defaults = dict(
    font="JetBrains Mono",
    fontsize=15,
    padding=4,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(filename="~/.config/qtile/python.png"),
                widget.GroupBox(),
                widget.Prompt(),
                widget.WindowName(),
                widget.Chord(
                    chords_colors={
                        "launch": ("#030315", "#cdc7d3"),
                    },
                    name_transform=lambda name: name.upper(),
                ),
                # NB Systray is incompatible with Wayland, consider using StatusNotifier instead
                # widget.StatusNotifier(),
                widget.Sep(),
                widget.Wallpaper(directory="~/Pictures/Wallpapers/dotfiles1/", label="🖼️"),
                widget.Sep(),
                widget.Image(filename="~/.config/qtile/ram.png"),
                widget.Memory(measure_mem="G"),
                #               widget.TextBox("🔋"),
                widget.Sep(),
                widget.Image(filename="~/.config/qtile/battery.png"),
                widget.Battery(format="{percent:2.0%}"),
                widget.Sep(),
                #               widget.TextBox("🔊"),
                widget.Image(filename="~/.config/qtile/sound.png"),
                widget.Volume(),
                # widget.Bluetooth(),
                # widget.Backlight(brightness_file="/sys/class/backlight/amdgpu_bl0/max_brightness"),
                widget.Sep(),
                widget.TextBox("🌡"),
                widget.ThermalZone(),
                # widget.NvidiaSensors(),
                #widget.TextBox(" "),
                #widget.TextBox(" "),
                #widget.Net(interface="wlo1"),
                widget.Sep(),
                widget.TextBox(" "),
                widget.Clock(format="%Y-%m-%d %H:%M", background="#553B88"),
                widget.Sep(),
                widget.Notify(),
                widget.TextBox(" "),
                widget.CheckUpdates(distro='Fedora'),
                widget.Systray(),
                widget.CurrentLayoutIcon(),
            ],
            35,
            # border_width=[1, 1, 1, 1],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
            background="#07001d",
            opacity=0.8,
            border_width=[1, 1, 1, 1]
        ),
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "qtile"

activity_timer = None
is_active = True

def lock_screen():
    qtile.cmd_spawn("i3lock -i /home/hamda/Pictures/Wallpapers/dotfiles1/wall-01.png")

def reset_timer():
    global activity_timer, is_active
    if activity_timer is not None:
        activity_timer.cancel()
    activity_timer = Timer(5, lock_screen)
    activity_timer.start()
    is_active = True



@hook.subscribe.startup_once
def autostart():
    reset_timer()
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])

@hook.subscribe.screen_change
def resetart_timer(qtile, ev):
    reset_timer()

@hook.subscribe.client_killed
def check_activity(qtile, win):
    global is_active
    if len(qtile.Windows) == 1 and not is_active:
        reset_timer()

@hook.subscribe.focus_change
def update_activity(qtile, win):
    global is_active
    is_active = False

