import curses
from ui.view import View, ScrollOffsetException
from decorator import with_curses


# keys we'll respond to, grouped by action
#TODO ESC has delay for escape sequences
action_keys = {
    'quit':   set((ord('q'),)),
    'resize': set((curses.KEY_RESIZE,)),
    'up':     set((ord('k'), curses.KEY_UP,)),
    'down':   set((ord('j'), curses.KEY_DOWN,)),
    'left':   set((ord('h'), curses.KEY_LEFT,)),
    'right':  set((ord('l'), curses.KEY_RIGHT,)),
}
movement_keys = set(
    key
    for action in ('up', 'down', 'left', 'right')
    for key in action_keys[action]
)


@with_curses
def interface(stdscr, *csv_models):
    views = [View(csv_model) for csv_model in csv_models]
    view = views[0]

    # hide cursor
    curses.curs_set(0)

    # initial screen
    view.render(stdscr)

    ## main loop
    while True:
        # stdscr.getch() calls stdscr.refresh()
        key = stdscr.getch()

        if key in action_keys['quit']:
            break  # exit main loop

        if key in action_keys['resize']:
            # repaint the screen in case it got larger for clipped content
            view.render(stdscr)

        elif key in movement_keys:
            if key in action_keys['up']:
                scroll_method = view.scroll_up
            elif key in action_keys['down']:
                scroll_method = view.scroll_down
            elif key in action_keys['left']:
                scroll_method = view.scroll_left
            elif key in action_keys['right']:
                scroll_method = view.scroll_right

            try:
                scroll_method()
            except ScrollOffsetException:
                continue

            # update screen buffer
            view.render(stdscr)
