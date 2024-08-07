from talon import Context, Module, actions
from talon.mac import applescript

ctx = Context()
mod = Module()


@mod.action_class
class Actions:
    def dock_is_autohide() -> bool:
        """Return whether the dock is set to autohide"""
        existing = applescript.run(
            'tell application "System Events" to get autohide of dock preferences'
        )
        if existing not in ["false", "true"]:
            raise RuntimeError(f"Unexpected dock autohide value: {existing}")
        return existing == "true"

    def dock_autohide_set(desired_state: bool):
        """Set dock autohide to the desired state"""
        existing = actions.user.dock_is_autohide()
        if existing != desired_state:
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
        applescript.run(
            """tell application "System Events" to set autohide of dock preferences to not (autohide of dock preferences)"""
        )
        actions.user.dock_autohide_postactions()
