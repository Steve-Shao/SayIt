"""Status indicator for visual feedback during recording."""

import tkinter as tk
from typing import Optional


class StatusIndicator:
    """Floating window indicator showing recording state.
    
    Displays a red circle with microphone icon at screen corner.
    Must be used with tkinter root window on main thread.
    """
    
    # Window size
    SIZE = 60
    
    # Colors
    COLOR_RECORDING = "#FF3B30"  # iOS red
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
    
    def _create_window(self) -> None:
        """Create the indicator window."""
        if self._window is not None:
            return
        
        self._window = tk.Toplevel(self._root)
        
        # Window properties: floating, topmost, no decorations
        self._window.overrideredirect(True)  # No title bar
        self._window.attributes("-topmost", True)  # Always on top
        self._window.attributes("-alpha", 0.9)  # Slight transparency
        
        # macOS specific: make window float above all
        try:
            self._window.attributes("-type", "splash")
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
        
        if self._window is None:
            self._create_window()
        
        if self._window:
            self._window.deiconify()
            self._window.lift()  # Bring to front
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
