import curses
import hashlib
import random
import string

def generate_password_from_text(input_text, password_length=16):
    """Generates a deterministic password from the input text."""
    # Step 1: Hash the input text
    hashed_text = hashlib.sha256(input_text.encode()).hexdigest()

    # Step 2: Define a set of characters to use in the password (letters, numbers, symbols)
    characters = string.ascii_letters + string.digits + "!@#$%^&*()"

    # Step 3: Create a password by selecting from the hashed characters
    random.seed(hashed_text)  # Seed random with the hash to ensure reproducibility
    password = ''.join(random.choice(characters) for _ in range(password_length))
    
    return password

def virtual_keyboard(stdscr):
    """Simulates an on-screen keyboard in a terminal with Shift for capitals and special characters."""
    curses.curs_set(0)
    stdscr.clear()

    # Define keyboard layout as a grid of individual keys (including special characters)
    keyboard = [
        list("1234567890!@#$%^&*()"),
        list("qwertyuiop[]{}\\|"),
        list("asdfghjkl;:'\""),
        list("zxcvbnm,./<>?"),
        ["SPACE", "BACKSPACE", "ENTER", "SHIFT"]
    ]
    
    # Mapping for characters, including special characters
    key_mapping = {
        "1": "1", "2": "2", "3": "3", "4": "4", "5": "5", "6": "6", "7": "7", "8": "8", "9": "9", "0": "0",
        "!": "!", "@": "@", "#": "#", "$": "$", "%": "%", "^": "^", "&": "&", "*": "*", "(": "(", ")": ")",
        "[": "[", "]": "]", "{": "{", "}": "}", "\\": "\\", "|": "|",
        "q": "q", "w": "w", "e": "e", "r": "r", "t": "t", "y": "y", "u": "u", "i": "i", "o": "o", "p": "p",
        "a": "a", "s": "s", "d": "d", "f": "f", "g": "g", "h": "h", "j": "j", "k": "k", "l": "l",
        ";": ";", ":": ":", "'": "'", "\"": "\"",
        "z": "z", "x": "x", "c": "c", "v": "v", "b": "b", "n": "n", "m": "m",
        ",": ",", ".": ".", "/": "/", "<": "<", ">": ">", "?": "?",
        "SPACE": " ", "BACKSPACE": "BACKSPACE", "ENTER": "ENTER", "SHIFT": "SHIFT"
    }

    rows = len(keyboard)
    cols = [len(row) for row in keyboard]

    # Keyboard display start positions
    start_y = 5
    start_x = 5

    # Cursor position
    cursor_y, cursor_x = 0, 0

    # Captured input
    input_text = []

    # Shift state
    shift_active = False

    while True:
        # Clear screen
        stdscr.clear()
        stdscr.addstr(0, 0, "Virtual Keyboard - Use arrow keys to navigate, ENTER to select.")
        stdscr.addstr(2, 0, "Current Input: " + "".join(input_text))

        # Render keyboard with Shift functionality
        for row_idx, row in enumerate(keyboard):
            for col_idx, char in enumerate(row):
                # If Shift is active, capitalize letters or symbols
                display_char = char.upper() if shift_active and char.isalpha() else char
                if row_idx == cursor_y and col_idx == cursor_x:
                    stdscr.addstr(start_y + row_idx, start_x + col_idx * 3, display_char, curses.A_REVERSE)
                else:
                    stdscr.addstr(start_y + row_idx, start_x + col_idx * 3, display_char)

        stdscr.refresh()

        # Handle user input (capturing only virtual keyboard actions)
        key = stdscr.getch()

        if key == curses.KEY_UP:
            cursor_y = max(0, cursor_y - 1)
            cursor_x = min(cursor_x, cols[cursor_y] - 1)  # Adjust cursor_x for shorter rows
        elif key == curses.KEY_DOWN:
            cursor_y = min(rows - 1, cursor_y + 1)
            cursor_x = min(cursor_x, cols[cursor_y] - 1)
        elif key == curses.KEY_LEFT:
            cursor_x = max(0, cursor_x - 1)
        elif key == curses.KEY_RIGHT:
            cursor_x = min(cols[cursor_y] - 1, cursor_x + 1)
        elif key == 10 or key == 13:  # ENTER key
            selected_key = keyboard[cursor_y][cursor_x]
            if selected_key == "ENTER":
                break
            elif selected_key == "BACKSPACE":
                if input_text:
                    input_text.pop()
            elif selected_key == "SHIFT":
                # Toggle shift state
                shift_active = not shift_active
            else:
                # Add selected character to input, capitalize if Shift is active
                char_to_add = key_mapping[selected_key]
                if shift_active and char_to_add.isalpha():
                    char_to_add = char_to_add.upper()
                input_text.append(char_to_add)
        elif key == ord('q'):  # Quit on 'q'
            break

    return "".join(input_text)

def curses_interface(stdscr):
    """Curses-based interface to securely input text and select password length."""
    curses.curs_set(0)  # Hide the cursor
    stdscr.clear()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

    stdscr.addstr(0, 0, "Password Generator (Use this tool to securely generate passwords)", curses.A_BOLD)
    stdscr.addstr(2, 0, "Step 1: Enter a word or phrase to generate the password.")
    stdscr.addstr(3, 0, "Step 2: Choose the password length.")
    stdscr.addstr(4, 0, "Step 3: Generate and display the password securely.")
    stdscr.addstr(6, 0, "Press ENTER to confirm, BACKSPACE to delete, and UP/DOWN to adjust length.")

    input_text = []
    password_length = 16
    current_step = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Password Generator", curses.A_BOLD)
        
        if current_step == 0:
            stdscr.addstr(2, 0, "Enter your text (current: {}):".format("".join(input_text)), curses.A_BOLD)
            stdscr.addstr(4, 0, "".join(input_text) + "_")
        elif current_step == 1:
            stdscr.addstr(2, 0, f"Select Password Length (current: {password_length}):", curses.A_BOLD)
            stdscr.addstr(4, 0, "Use UP/DOWN to increase/decrease.")
        elif current_step == 2:
            stdscr.addstr(2, 0, "Generated Password:", curses.A_BOLD)
            stdscr.addstr(4, 0, generate_password_from_text("".join(input_text), password_length), curses.color_pair(1))
            stdscr.addstr(6, 0, "Press Q to quit or ENTER to restart.")

        stdscr.refresh()
        key = stdscr.getch()

        if key == curses.KEY_BACKSPACE or key == 127:  # Handle BACKSPACE
            if current_step == 0 and input_text:
                input_text.pop()
        elif key == curses.KEY_ENTER or key in [10, 13]:  # Handle ENTER
            if current_step < 2:
                current_step += 1
            else:
                return  # Exit after showing the password
        elif key == curses.KEY_UP and current_step == 1:  # Increase password length
            password_length = min(password_length + 1, 64)
        elif key == curses.KEY_DOWN and current_step == 1:  # Decrease password length
            password_length = max(password_length - 1, 8)
        elif key == ord('q') or key == ord('Q'):  # Quit
            return
        elif current_step == 0:  # Use the virtual keyboard for text input
            input_text = list(virtual_keyboard(stdscr))

if __name__ == "__main__":
    curses.wrapper(curses_interface)
