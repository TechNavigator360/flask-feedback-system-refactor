# Styling cell for consistent UI design across the application.

# Window Sizes
# Defines the main window dimensions for the application.
MAIN_WINDOW_WIDTH = 800
MAIN_WINDOW_HEIGHT = 600

# Colors
# Sets primary, secondary, and background colors for styling elements like buttons and labels.
PRIMARY_COLOR = "#4CAF50"
SECONDARY_COLOR = "#333333"
BACKGROUND_COLOR = "#F2F2F2"
HOVER_COLOR = "#45a049"
ERROR_COLOR = "#FF6347"
SUCCESS_COLOR = "green"

# Fonts
# Specifies font styles and sizes for titles, main text, and smaller labels.
FONT_MAIN = ("Helvetica", 12)
FONT_TITLE = ("Helvetica", 30, "bold")
FONT_SMALL = ("Helvetica", 10)

# Title Font Color
TITLE_COLOR = "#4CAF50"


# Button Style Function without pack()
# `apply_button_style`: Configures the appearance of buttons, including background color, text color, and padding.
def apply_button_style(button):
    button.config(bg=PRIMARY_COLOR, fg="white", font=FONT_MAIN, padx=10, pady=5)

# `get_button_width`: Dynamically calculates button width based on the window size.
def get_button_width():
    # Adjust the percentage as needed
    return int((MAIN_WINDOW_WIDTH * 0.50) / 10)  # Convert pixels to character units

# Label Style Function with Capitalization
# `apply_label_style`: Configures label appearance, with uppercase text and specific styling for titles.
def apply_label_style(label, title=False):
    font = FONT_TITLE if title else FONT_MAIN
    fg_color = TITLE_COLOR if title else SECONDARY_COLOR

    # Set the label text to uppercase if it's a title
    if title:
        label.config(text=label.cget("text").upper(), fg=fg_color, font=font, bg=BACKGROUND_COLOR)
    else:
        label.config(fg=fg_color, font=font, bg=BACKGROUND_COLOR)

# Entry Field Style without pack()
# `apply_entry_style`: Styles input fields with consistent font, colors, and borders.
def apply_entry_style(entry):
    entry.config(font=FONT_MAIN, bg="white", fg=SECONDARY_COLOR, borderwidth=0.5, relief="solid")

# Hover Effect Function for Buttons
# `add_hover_effect`: Adds interactivity to buttons, changing the background color on mouse hover.
def add_hover_effect(widget):
    def on_enter(_event):
        widget.config(bg=HOVER_COLOR)
    def on_leave(_event):
        widget.config(bg=PRIMARY_COLOR)
    widget.bind("<Enter>", on_enter)
    widget.bind("<Leave>", on_leave)