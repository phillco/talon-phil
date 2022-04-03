app: Spotify
os: mac
mode: command
-

# When pushing cmd-L, simulate going into "autodictate" mode.
# Spotify exposes no AX information, so this doesn't happen automatically.
key(cmd-l):
    key(cmd-l)
    mode.enable("dictation")
    mode.disable("command")
