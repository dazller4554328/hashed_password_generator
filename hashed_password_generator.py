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
        elif current_step == 0 and key in range(32, 127):  # Append printable characters
            input_text.append(chr(key))

if __name__ == "__main__":
    curses.wrapper(curses_interface)
