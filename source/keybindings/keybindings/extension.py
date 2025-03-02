import omni.ext
import omni.kit.app
import carb.input
import omni.appwindow


class MyExtension(omni.ext.IExt):
    """This extension manages a simple counter UI with a plot and handles keyboard input."""

    def on_startup(self, _ext_id):
        print("[ext: keybindings] Extension startup")

        # Setup input handling
        self._input_subscription = None
        self._setup_input_handling()

    def _setup_input_handling(self):
        """Set up keyboard input handling"""
        # Get the input interface using carb.input
        self._input = carb.input.acquire_input_interface()

        # Get the default app window and keyboard
        app_window = omni.appwindow.get_default_app_window()
        self._keyboard = app_window.get_keyboard()

        # Create a keyboard subscription using carb.input
        self._input_subscription = self._input.subscribe_to_keyboard_events(
            self._keyboard,
            self._on_keyboard_event
        )

    def _on_keyboard_event(self, event):
        """Handle keyboard input events using carb.input"""
        # Check if ESC key was pressed
        if event.input == carb.input.KeyboardInput.ESCAPE:
            if event.type == carb.input.KeyboardEventType.KEY_PRESS:
                print("[ext: keybindings] ESC key pressed. Exiting application.")
                omni.kit.app.get_app().shutdown()  # Close Omniverse Kit app

    def on_shutdown(self):
        print("[ext: keybindings] Extension shutdown")

        # Clean up input subscription
        if self._input_subscription:
            self._input_subscription = None
            self._keyboard = None
