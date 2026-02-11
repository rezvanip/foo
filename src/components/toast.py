"""Toast notification component using KivyMD Snackbar."""
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.button import MDFlatButton


class Toast:
    """Simple toast notification utility."""
    
    @staticmethod
    def success(message: str, duration: float = 2.0):
        """Show a success toast (green)."""
        snackbar = Snackbar(text=message, duration=duration, bg_color=(0.2, 0.8, 0.2, 1))
        snackbar.open()
        return snackbar
    
    @staticmethod
    def error(message: str, duration: float = 3.0):
        """Show an error toast (red)."""
        snackbar = Snackbar(text=message, duration=duration, bg_color=(0.9, 0.2, 0.2, 1))
        snackbar.open()
        return snackbar
    
    @staticmethod
    def info(message: str, duration: float = 2.0):
        """Show an info toast (blue)."""
        snackbar = Snackbar(text=message, duration=duration, bg_color=(0.2, 0.5, 0.9, 1))
        snackbar.open()
        return snackbar
