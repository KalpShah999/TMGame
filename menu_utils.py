"""
Interactive Menu Utilities
Provides arrow key navigation for menus with fallback to text input.
"""

import sys
import os


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def interactive_menu(title, options, descriptions=None, show_indices=True):
    """
    Display an interactive menu with arrow key navigation.
    
    Args:
        title: Menu title
        options: List of option strings
        descriptions: Optional list of descriptions for each option
        show_indices: Whether to show [1], [2], etc.
    
    Returns:
        Selected option index (0-based)
    """
    # Try to use curses for arrow key navigation
    try:
        import curses
        return _curses_menu(title, options, descriptions, show_indices)
    except (ImportError, Exception):
        # Fallback to simple input
        return _simple_menu(title, options, descriptions, show_indices)


def _curses_menu(title, options, descriptions, show_indices):
    """Arrow key navigation menu using curses."""
    import curses
    
    def menu_screen(stdscr):
        curses.curs_set(0)  # Hide cursor
        current_row = 0
        
        while True:
            stdscr.clear()
            h, w = stdscr.getmaxyx()
            
            # Display title
            stdscr.addstr(0, 0, "=" * min(70, w-1))
            stdscr.addstr(1, 0, title[:w-1])
            stdscr.addstr(2, 0, "=" * min(70, w-1))
            stdscr.addstr(3, 0, "")
            
            # Display options
            for idx, option in enumerate(options):
                y = 4 + idx * 2
                if y >= h - 4:  # Leave room for footer
                    break
                    
                if show_indices:
                    prefix = f"  [{idx + 1}] "
                else:
                    prefix = "  "
                
                # Highlight current selection
                if idx == current_row:
                    stdscr.addstr(y, 0, ">>", curses.A_BOLD)
                    stdscr.addstr(y, 3, prefix + option, curses.A_REVERSE)
                else:
                    stdscr.addstr(y, 0, "  ")
                    stdscr.addstr(y, 3, prefix + option)
                
                # Add description if provided
                if descriptions and idx < len(descriptions) and descriptions[idx]:
                    desc_y = y + 1
                    if desc_y < h - 3:
                        stdscr.addstr(desc_y, 6, descriptions[idx][:w-7], curses.A_DIM)
            
            # Display footer
            footer_y = min(h - 2, 4 + len(options) * 2 + 1)
            if footer_y < h - 1:
                stdscr.addstr(footer_y, 0, "=" * min(70, w-1))
                stdscr.addstr(footer_y + 1, 0, 
                             "Use ↑/↓ arrows to navigate, ENTER to select, or type number: "[:w-1])
            
            stdscr.refresh()
            
            # Get input
            key = stdscr.getch()
            
            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(options) - 1:
                current_row += 1
            elif key in [curses.KEY_ENTER, 10, 13]:  # Enter key
                return current_row
            elif ord('1') <= key <= ord('9'):  # Number keys
                num = key - ord('0')
                if 1 <= num <= len(options):
                    return num - 1
            elif key == ord('q') or key == ord('Q'):
                if 'quit' in [opt.lower() for opt in options]:
                    return options.index([opt for opt in options if opt.lower() == 'quit'][0])
                return -1  # Quit signal
    
    try:
        return curses.wrapper(menu_screen)
    except KeyboardInterrupt:
        return -1


def _simple_menu(title, options, descriptions, show_indices):
    """Fallback menu without arrow keys."""
    print("=" * 70)
    print(title)
    print("=" * 70)
    print()
    
    for idx, option in enumerate(options):
        if show_indices:
            print(f"  [{idx + 1}] {option}")
        else:
            print(f"  {option}")
        
        if descriptions and idx < len(descriptions) and descriptions[idx]:
            print(f"      {descriptions[idx]}")
        print()
    
    print("=" * 70)
    
    while True:
        try:
            choice = input("\nEnter your choice (number or name): ").strip()
            
            # Try as number
            try:
                num = int(choice)
                if 1 <= num <= len(options):
                    return num - 1
            except ValueError:
                pass
            
            # Try as option name (case insensitive)
            choice_lower = choice.lower()
            for idx, option in enumerate(options):
                if option.lower() == choice_lower or option.lower().startswith(choice_lower):
                    return idx
            
            print(f"Invalid choice. Please enter a number (1-{len(options)}) or option name.")
        
        except KeyboardInterrupt:
            return -1


def confirm_prompt(message, default=False):
    """
    Display a yes/no confirmation prompt.
    
    Args:
        message: The question to ask
        default: Default answer if user just presses Enter
    
    Returns:
        True for yes, False for no
    """
    suffix = " [Y/n]: " if default else " [y/N]: "
    
    while True:
        try:
            response = input(message + suffix).strip().lower()
            
            if not response:
                return default
            
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            else:
                print("Please enter 'y' or 'n'")
        
        except KeyboardInterrupt:
            return False


def display_info(title, content, width=70):
    """Display formatted information box."""
    print()
    print("=" * width)
    print(title)
    print("=" * width)
    
    if isinstance(content, str):
        print(content)
    elif isinstance(content, list):
        for line in content:
            print(line)
    
    print("=" * width)
    print()


def wait_for_key(message="Press Enter to continue..."):
    """Wait for user to press Enter."""
    try:
        input(message)
    except KeyboardInterrupt:
        pass

