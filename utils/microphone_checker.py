from talon import Context, Module, actions, cron
from talon.mac import applescript

ctx = Context()
mod = Module()

DESIRED_SETTINGS = {
    'HyperX QuadCast S': 75
}

TOO_LOW_THRESHOLD = 10


@mod.action_class
class Actions:

    def get_microphone_volume() -> int:
        """Get microphone volume"""
        return int(applescript.run("input volume of (get volume settings)"))

    def set_microphone_volume(volume: int):
        """Set microphone volume"""
        applescript.run(f"set volume input volume {volume}")

    def should_fix_microphone_volume() -> bool:
        """Check if microphone volume should be fixed"""
        # don't do this if, for example, Talon is asleep and we aren't in a meeting
        microphone = actions.sound.active_microphone()
        setting = DESIRED_SETTINGS.get(microphone)
        if setting is None:
            return False

        return actions.speech.enabled() or actions.user.current_vc_software() is not None

    def check_microphone_volume(and_fix: bool = True):
        """Check microphone volume, and fix if necessary"""
        should_fix = actions.user.should_fix_microphone_volume()
        if not should_fix:
            return

        volume = actions.user.get_microphone_volume()
        microphone = actions.sound.active_microphone()
        desired_volume = DESIRED_SETTINGS.get(microphone)

        different_from_desired = volume != desired_volume
        too_low = volume <= TOO_LOW_THRESHOLD

        # NOTE(pcohen): some applications might raise the volume (like Google Meet) but not silence it;
        # for now just log this so I can see how often this happens.
        if different_from_desired and not too_low:
            actions.app.notify(f"WARNING: Microphone volume is {volume} ({microphone}), but this isn't too low to fix.", "Incorrect microphone volume")
            return

        if not too_low:
            return

        if and_fix:
            actions.user.set_microphone_volume(DESIRED_SETTINGS[microphone])
            new_volume = actions.user.get_microphone_volume()
            actions.app.notify(f"Was {volume}, set to {new_volume} ({microphone})", "Automatically fixed microphone volume")
        else:
            actions.app.notify(f"WARNING: Microphone volume is {volume} ({microphone})",
                               "Incorrect microphone volume")

cron.interval("10s", lambda: actions.user.check_microphone_volume())
