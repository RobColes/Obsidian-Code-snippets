"""Obsidian To-Do Creator - GUI app for creating markdown notes."""

import ctypes
import re
import tkinter as tk
from ctypes import wintypes
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tkinter import messagebox, ttk


class ObsidianTodoCreator:
    """A GUI application for creating Obsidian markdown notes with scheduled dates."""

    def __init__(self):
        """Initialize the Obsidian To-Do Creator application."""
        self.root = tk.Tk()
        self.root.title("Obsidian To-Do Creator")
        self.root.geometry("500x400")  # Increased height for new field
        self.root.resizable(width=False, height=False)
        # Windows-specific focus techniques for first launch
        self.root.wm_attributes("-topmost", True)
        self.root.lift()
        self.root.focus_force()

        # Iconify/deiconify trick often works on Windows
        self.root.iconify()
        self.root.update()
        self.root.deiconify()

        # Set window state and protocol
        self.root.state("normal")
        self.root.protocol("WM_TAKE_FOCUS", self._on_take_focus)

        # Delayed cleanup of topmost
        self.root.after(200, lambda: self.root.wm_attributes("-topmost", False))
        # Configuration - UPDATE THESE PATHS
        self.vault_path = r"C:\Obsidian\Robsidian"

        # Priority options
        self.priority_options = [
            "1-Today",
            "2-ThisWeek",
            "3-Soon",
            "5-Someday",
            "6-Waiting",
        ]
        self.priority_var = tk.StringVar(value="1-Today")  # Default to Today

        # Calculate date options based on current date
        self.date_options = self.calculate_date_options()

        self.create_widgets()
        # Enhanced entry field focus with multiple techniques
        self._focus_title_entry()

    def _on_take_focus(self):
        """Handle WM_TAKE_FOCUS protocol."""
        self.root.focus_force()
        if hasattr(self, "title_entry"):
            self.title_entry.focus_force()

    def _focus_title_entry(self):
        """Enhanced focus methods for title entry field."""
        if hasattr(self, "title_entry"):
            # Immediate focus
            self.title_entry.focus_set()
            self.title_entry.focus_force()

            # Delayed attempts with different methods
            self.root.after(50, lambda: self.title_entry.focus())
            self.root.after(100, lambda: self.title_entry.focus_force())
            self.root.after(200, lambda: self.title_entry.focus_set())
            self.root.after(
                300,
                lambda: setattr(
                    self.title_entry, "focus", lambda: self.title_entry.focus_force()
                ),
            )

            # Final attempt with selection
            self.root.after(
                400,
                lambda: self.title_entry.selection_range(0, tk.END)
                if self.title_entry.get()
                else None,
            )

    def calculate_date_options(self):
        """Calculate pre-defined date options based on current date."""
        # Use Perth timezone (UTC+8) for local date calculations
        perth_tz = timezone(timedelta(hours=8))
        base_date = datetime.now(tz=perth_tz).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )
        options = []

        # Add specific dates (next 6 days)
        for i in range(1, 7):
            date = base_date + timedelta(days=i)
            day_name = date.strftime("%A")
            month_abbr = date.strftime("%b")
            options.append(
                f"{date.strftime('%Y-%m-%d')} ({day_name}, {month_abbr} {date.day})",
            )

        # Add "Next Week" (next Monday)
        next_monday = base_date + timedelta(days=7)
        options.append(
            f"Next Week (Monday {next_monday.day} {next_monday.strftime('%b')})",
        )

        # Add "Next Month" (approximately 31 days)
        next_month = base_date + timedelta(days=31)
        options.append(
            f"Next Month (Thursday {next_month.day} {next_month.strftime('%b')})",
        )

        return options

    def on_date_focus_in(self, _event):
        """Clear placeholder text when combobox gets focus."""
        if self.date_var.get() == "Select a date or type YYYY-MM-DD":
            self.date_var.set("")

    def on_date_selected(self, _event):
        """Handle date selection from dropdown."""
        if self.date_var.get():
            self.priority_var.set("6-Waiting")
        else:
            self.priority_var.set("1-Today")  # Reset to default if date is cleared
        # Placeholder for future enhancements

    def on_date_changed(self, _event):
        """Update priority when date is selected."""
        if self.date_var.get():
            self.priority_var.set("6-Waiting")
        else:
            self.priority_var.set("1-Today")  # Reset to default if date is cleared

    def extract_date_from_selection(self, date_selection):
        """Extract the actual date (YYYY-MM-DD) from the formatted selection."""
        if not date_selection:
            return ""

        # Check if it's a direct YYYY-MM-DD format
        if re.match(r"^\d{4}-\d{2}-\d{2}$", date_selection):
            return date_selection

        # Extract date from formatted strings like "2025-08-19 (Tuesday, Aug 19)"
        date_match = re.search(r"^(\d{4}-\d{2}-\d{2})", date_selection)
        if date_match:
            return date_match.group(1)

        # Handle "Next Week" and "Next Month" options
        if "Next Week" in date_selection:
            # Calculate next Monday from current date
            perth_tz = timezone(timedelta(hours=8))
            base_date = datetime.now(tz=perth_tz).replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
            next_monday = base_date + timedelta(days=7)
            return next_monday.strftime("%Y-%m-%d")

        if "Next Month" in date_selection:
            # Calculate next month (approximately 31 days)
            perth_tz = timezone(timedelta(hours=8))
            base_date = datetime.now(tz=perth_tz).replace(
                hour=0,
                minute=0,
                second=0,
                microsecond=0,
            )
            next_month = base_date + timedelta(days=31)
            return next_month.strftime("%Y-%m-%d")

        return date_selection

    def validate_date(self, date_string):
        """Validate date format (YYYY-MM-DD)."""
        if not date_string:
            return True  # Empty date is optional

        # Simple regex validation to avoid timezone issues
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_string):
            return False

        try:
            # Just check if the date is valid without creating a datetime object
            year, month, day = map(int, date_string.split("-"))
            datetime(year, month, day, tzinfo=timezone.utc)
        except ValueError:
            return False
        else:
            return True

    def parse_natural_date_to_yyyy_mm_dd(self, date_text):
        """Parse natural date words to a YYYY-MM-DD string.

        Supports: "today", "tomorrow", "next week", or direct "YYYY-MM-DD".
        Returns empty string if input isn't recognized/valid.
        """
        if not date_text:
            return ""

        normalized = date_text.strip().lower()

        # Perth timezone base date (midnight)
        perth_tz = timezone(timedelta(hours=8))
        base_date = datetime.now(tz=perth_tz).replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

        if normalized == "today":
            return base_date.strftime("%Y-%m-%d")
        if normalized == "tomorrow":
            return (base_date + timedelta(days=1)).strftime("%Y-%m-%d")
        if normalized == "next week":
            # Match existing app behavior: next Monday approximation (+7 days from base)
            return (base_date + timedelta(days=7)).strftime("%Y-%m-%d")

        # If it's already a valid YYYY-MM-DD
        if self.validate_date(date_text):
            return date_text

        return ""

    def parse_natural_language_title(self):
        """If title starts with priority like '1,', parse CSV to prefill fields.

        Format: "<priority_digit>, <note title>, <next action>[, <scheduled>]"
        """
        raw_title_input = self.title_var.get().strip()
        if not raw_title_input:
            return

        # Must begin with one of the supported priority digits followed by a comma
        if not re.match(r"^[12356]\s*,", raw_title_input):
            return

        # Split into at most 4 parts: priority, title, next, scheduled?
        parts = [p.strip() for p in raw_title_input.split(",", 3)]
        if len(parts) < 2:
            return

        priority_digit = parts[0]
        priority_map = {
            "1": "1-Today",
            "2": "2-ThisWeek",
            "3": "3-Soon",
            "5": "5-Someday",
            "6": "6-Waiting",
        }

        # Update priority
        mapped_priority = priority_map.get(priority_digit)
        if not mapped_priority:
            return
        self.priority_var.set(mapped_priority)

        # Update title
        note_title = parts[1]
        self.title_var.set(note_title)

        # Update next action if provided
        if len(parts) >= 3 and parts[2]:
            self.action_var.set(parts[2])

        # Update scheduled date if provided and recognized
        if len(parts) == 4 and parts[3]:
            parsed_date = self.parse_natural_date_to_yyyy_mm_dd(parts[3])
            if parsed_date:
                self.date_var.set(parsed_date)

    def on_title_focus_out(self, _event):
        """Handle leaving the title field by attempting natural language parsing."""
        self.parse_natural_language_title()

    def create_widgets(self):
        """Create and configure the GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title field
        ttk.Label(
            main_frame,
            text="Note Title (natural: Priority, title, next, date): ",
        ).grid(
            row=0,
            column=0,
            sticky=tk.W,
            pady=(0, 5),
        )
        self.title_var = tk.StringVar()
        self.title_entry = ttk.Entry(main_frame, textvariable=self.title_var, width=50)
        self.title_entry.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky=(tk.W, tk.E),
            pady=(0, 15),
        )
        # Immediate focus attempt and delayed enhanced focus
        self.title_entry.focus_set()
        self._focus_title_entry()
        # Parse natural language input when leaving the title field
        self.title_entry.bind("<FocusOut>", self.on_title_focus_out)

        # Next action field
        ttk.Label(main_frame, text="Next Action:").grid(
            row=2,
            column=0,
            sticky=tk.W,
            pady=(0, 5),
        )
        self.action_var = tk.StringVar()
        self.action_entry = ttk.Entry(
            main_frame,
            textvariable=self.action_var,
            width=50,
        )
        self.action_entry.grid(
            row=3,
            column=0,
            columnspan=2,
            sticky=(tk.W, tk.E),
            pady=(0, 15),
        )

        # Scheduled date field
        ttk.Label(main_frame, text="Scheduled Date (optional - YYYY-MM-DD):").grid(
            row=6,
            column=0,
            sticky=tk.W,
            pady=(0, 5),
        )
        self.date_var = tk.StringVar()
        self.date_combobox = ttk.Combobox(
            main_frame,
            textvariable=self.date_var,
            values=self.date_options,
            width=47,
        )
        self.date_combobox.grid(
            row=7,
            column=0,
            columnspan=2,
            sticky=(tk.W, tk.E),
            pady=(0, 15),
        )
        # Allow manual entry in the combobox
        self.date_combobox.configure(state="normal")

        # Bind events to clear placeholder text and update priority
        self.date_combobox.bind("<FocusIn>", self.on_date_focus_in)
        self.date_combobox.bind("<<ComboboxSelected>>", self.on_date_selected)
        self.date_combobox.bind("<KeyRelease>", self.on_date_changed)

        # Priority field
        ttk.Label(main_frame, text="Priority:").grid(
            row=8,
            column=0,
            sticky=tk.W,
            pady=(0, 5),
        )
        self.priority_frame = ttk.Frame(main_frame)
        self.priority_frame.grid(
            row=9,
            column=0,
            columnspan=2,
            sticky=(tk.W, tk.E),
            pady=(0, 15),
        )
        for i, option in enumerate(self.priority_options):
            ttk.Radiobutton(
                self.priority_frame,
                text=option,
                value=option,
                variable=self.priority_var,
                command=lambda opt=option: self.priority_var.set(opt),
            ).grid(row=0, column=i, sticky=tk.W)

        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=10, column=0, columnspan=2, pady=(10, 0))

        ttk.Button(button_frame, text="Create Note", command=self.create_note).pack(
            side=tk.LEFT,
            padx=(0, 10),
        )
        ttk.Button(button_frame, text="Cancel", command=self.root.quit).pack(
            side=tk.LEFT,
        )

        # Bind Enter key to create note
        self.root.bind("<Return>", lambda _: self.create_note())
        self.root.bind("<Escape>", lambda _: self.root.quit())

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

    def sanitize_filename(self, filename):
        """Remove or replace characters that aren't valid in filenames."""
        # Replace invalid characters with underscores
        filename = re.sub(r'[<>:"/\\|?*]', "_", filename)
        # Remove any trailing periods or spaces
        return filename.strip(". ")

    def create_note(self):
        """Create a new Obsidian markdown note with the provided information."""
        # Ensure any natural-language title input is parsed before validation
        self.parse_natural_language_title()

        title = self.title_var.get().strip()
        action = self.action_var.get().strip()
        priority = self.priority_var.get()
        scheduled_date_selection = self.date_var.get().strip()

        # Validate inputs
        if not title:
            messagebox.showerror("Error", "Note title is required!")
            self.title_entry.focus()
            return

        if not action:
            messagebox.showerror("Error", "Next action is required!")
            self.action_entry.focus()
            return

        # Extract and validate the actual date
        scheduled_date = self.extract_date_from_selection(scheduled_date_selection)
        if scheduled_date and not self.validate_date(scheduled_date):
            messagebox.showerror("Error", "Date must be in YYYY-MM-DD format!")
            self.date_combobox.focus()
            return

        # Create full path
        full_todo_path = Path(self.vault_path)
        full_todo_path.mkdir(parents=True, exist_ok=True)

        # Create filename
        safe_filename = self.sanitize_filename(title)
        filepath = full_todo_path / f"{safe_filename}.md"

        # Check if file already exists
        if filepath.exists() and not messagebox.askyesno(
            "File Exists",
            f"File '{safe_filename}.md' already exists. Overwrite?",
        ):
            return

        # Create frontmatter
        frontmatter = "---\n"
        frontmatter += f"Next: {action}\n"
        if scheduled_date:
            frontmatter += f"Scheduled: {scheduled_date}\n"
        frontmatter += "---\n"

        # Create note content
        if scheduled_date:
            content = frontmatter + "Scheduled: `INPUT[date:Scheduled]`\n"
        else:
            content = frontmatter

        # Add priority line after frontmatter
        content += f"#Home - [[{priority}]]\n"
        content += "# Next: `INPUT[text(placeholder(''), class('my-mb-h1')):Next]`\n\n"

        try:
            with filepath.open("w", encoding="utf-8") as f:
                f.write(content)

            # Close the application on success
            self.root.destroy()

        except OSError as e:
            messagebox.showerror("Error", f"Failed to create note:\n{e!s}")

    def run(self):
        """Start the GUI application main loop."""
        # Final activation attempt before starting mainloop
        self.root.after(50, self._final_activation)
        self.root.mainloop()

    def _final_activation(self):
        """Activate Final window activation and focus attempt."""
        try:
            # Windows-specific activation

            # Get window handle
            hwnd = int(self.root.winfo_id())

            # Bring to foreground
            ctypes.windll.user32.SetForegroundWindow(hwnd)
            ctypes.windll.user32.ShowWindow(hwnd, 9)  # SW_RESTORE
            ctypes.windll.user32.SetActiveWindow(hwnd)

        except (ImportError, AttributeError):
            # Fallback for non-Windows or if ctypes fails
            pass

        # Tkinter fallback methods
        self.root.lift()
        self.root.focus_force()
        if hasattr(self, "title_entry"):
            self.title_entry.focus_force()


if __name__ == "__main__":
    # Update the vault_path in the __init__ method before running
    app = ObsidianTodoCreator()
    app.run()
