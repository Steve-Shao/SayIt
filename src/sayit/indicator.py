"""Status indicator for visual feedback during recording."""

import subprocess
import tkinter as tk
from typing import Optional


def _get_frontmost_app() -> Optional[str]:
    """Get the bundle ID of the frontmost application."""
    script = '''
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        return bundle identifier of frontApp
    end tell
    '''
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            text=True,
            timeout=1,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return None


def _activate_app(bundle_id: str) -> None:
    """Activate an application by bundle ID."""
    script = f'''
    tell application id "{bundle_id}"
        activate
    end tell
    '''
    try:
        subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            timeout=1,
        )
    except Exception:
        pass


class StatusIndicator:
    """Floating window indicator showing recording state.
    
    Displays a red circle with microphone icon at screen corner.
    Must be used with tkinter root window on main thread.
    """
    
    # Window size
    SIZE = 60
    
    # Colors
    COLOR_RECORDING = "#FF3B30"  # iOS red
    COLOR_PROCESSING = "#FF9500"  # iOS orange
    COLOR_BORDER = "#FFFFFF"
    
    def __init__(self, root: tk.Tk):
        """Initialize the status indicator.
        
        Args:
            root: Parent tkinter root window (must exist on main thread).
        """
        self._root = root
        self._window: Optional[tk.Toplevel] = None
        self._canvas: Optional[tk.Canvas] = None
        self._visible = False
        self._previous_app: Optional[str] = None
    
    def _create_window(self) -> None:
        """Create the indicator window."""
        if self._window is not None:
            return
        
        self._window = tk.Toplevel(self._root)
        
        # Window properties: floating, topmost, no decorations, no focus
        self._window.overrideredirect(True)  # No title bar
        self._window.attributes("-topmost", True)  # Always on top
        self._window.attributes("-alpha", 0.9)  # Slight transparency
        
        # Prevent window from taking focus
        self._window.focusmodel("passive")
        self._window.wm_attributes("-transparent", True)  # Click-through on some systems
        
        # macOS specific: make window float above all without taking focus
        try:
            # NSPanel-like behavior: floating, non-activating
            self._window.tk.call(
                "::tk::unsupported::MacWindowStyle", "style",
                self._window._w, "help", "noActivates"
            )
        except tk.TclError:
            pass  # Not supported on this platform
        
        # Position: top-right corner, below menu bar
        screen_width = self._window.winfo_screenwidth()
        x = screen_width - self.SIZE - 20  # 20px margin from right
        y = 40  # Below menu bar
        self._window.geometry(f"{self.SIZE}x{self.SIZE}+{x}+{y}")
        
        # Canvas for drawing
        self._canvas = tk.Canvas(
            self._window,
            width=self.SIZE,
            height=self.SIZE,
            bg=self.COLOR_RECORDING,
            highlightthickness=0,
        )
        self._canvas.pack()
        
        # Draw microphone icon (simple representation)
        self._draw_mic_icon()
        
        # Start hidden
        self._window.withdraw()
    
    def _draw_mic_icon(self) -> None:
        """Draw a simple microphone icon on the canvas."""
        if self._canvas is None:
            return
        
        cx, cy = self.SIZE // 2, self.SIZE // 2
        
        # Microphone body (rounded rectangle approximation using oval)
        mic_width = 12
        mic_height = 20
        self._canvas.create_oval(
            cx - mic_width // 2, cy - mic_height // 2 - 4,
            cx + mic_width // 2, cy + mic_height // 2 - 4,
            fill=self.COLOR_BORDER,
            outline=self.COLOR_BORDER,
        )
        
        # Microphone stand (arc)
        stand_width = 20
        self._canvas.create_arc(
            cx - stand_width // 2, cy - 8,
            cx + stand_width // 2, cy + 12,
            start=0, extent=-180,
            style=tk.ARC,
            outline=self.COLOR_BORDER,
            width=2,
        )
        
        # Microphone base (vertical line)
        self._canvas.create_line(
            cx, cy + 12,
            cx, cy + 20,
            fill=self.COLOR_BORDER,
            width=2,
        )
        
        # Base horizontal line
        self._canvas.create_line(
            cx - 8, cy + 20,
            cx + 8, cy + 20,
            fill=self.COLOR_BORDER,
            width=2,
        )
    
    def show(self) -> None:
        """Show the indicator window.
        
        Safe to call from main thread via root.after().
        """
        if self._visible:
            return
        
        # Remember the current frontmost app before showing
        self._previous_app = _get_frontmost_app()
        
        if self._window is None:
            self._create_window()
        
        if self._window:
            # Reset to recording color
            if self._canvas:
                self._canvas.configure(bg=self.COLOR_RECORDING)
            self._window.deiconify()
            self._window.lift()  # Bring to front
            
            # Immediately release focus back to previous app
            try:
                self._window.lower()  # Lower in stacking order
                self._window.attributes("-topmost", True)  # But keep on top visually
            except tk.TclError:
                pass
            
            # Restore focus to previous app
            if self._previous_app:
                self._root.after(10, lambda: _activate_app(self._previous_app))
            
            self._visible = True
    
    def hide(self) -> None:
        """Hide the indicator window.
        
        Safe to call from main thread via root.after().
        """
        if not self._visible:
            return
        
        if self._window:
            self._window.withdraw()
            self._visible = False
    
    def set_processing(self) -> None:
        """Change indicator to processing state (orange color).
        
        Safe to call from main thread via root.after().
        """
        if self._canvas:
            self._canvas.configure(bg=self.COLOR_PROCESSING)
    
    @property
    def is_visible(self) -> bool:
        """Return whether the indicator is currently visible."""
        return self._visible
    
    def destroy(self) -> None:
        """Destroy the indicator window and cleanup."""
        if self._window:
            try:
                self._window.destroy()
            except tk.TclError:
                pass  # Already destroyed
            self._window = None
            self._canvas = None
            self._visible = False
