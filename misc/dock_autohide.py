from talon import Context, Module, actions

ctx = Context()
mod = Module()


@mod.action_class
class Actions:
    def dock_is_autohide() -> bool:
        """Return whether the dock is set to autohide"""
        existing = actions.user.exec("defaults read com.apple.dock autohide")[0]
        if existing not in ["0", "1"]:
            raise RuntimeError(f"Unexpected dock autohide value: {existing}")
        return int(existing) == 1

    def dock_autohide_set(desired_state: bool):
        """Set dock autohide to the desired state"""
        existing = actions.user.dock_is_autohide()
        if existing == desired_state:
            return
        actions.user.dock_toggle_autohide()

    def dock_autohide_postactions():
        """Actions to run after changing dock autohide"""
        actions.sleep("2s")

        # Run my window management logic
        # TODO(pcohen): we could instead just detect the changed screen space,
        # and only resize windows into/out of it
        actions.user.fixup_usual_suspects()

    def dock_toggle_autohide():
        """Toggle dock autohide"""
        # NOTE(pcohen): I customize this shortcut; the default is
        # cmd-alt-shift-d
        actions.key("cmd-alt-shift-d")
        actions.user.dock_autohide_postactions()
