app: Spotify
os: mac
-

settings():
   # Spotify exposes no AX information, and there's no need for contact sensitive searching.
   user.context_sensitive_dictation = 0
   user.accessibility_dictation = 0
