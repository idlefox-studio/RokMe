# RokMe - @mastyDev 2023.01
import curses
import json
import cat
import status

menu = [' Categories ',' Status ',' EXIT '] # missing Settings

# main menu
def print_menu(sw, selected_row_idx):
    # with open('services.json') as json_file:
    #     data = json.load(json_file)
    h,w=sw.getmaxyx()
    # load title function
    print_title(sw,h,w)
    for idx,row in enumerate(menu):
        x=w//2-len(row)//2
        y=h//2-len(menu)//2+idx*2
        if idx == selected_row_idx:
            sw.attron(curses.color_pair(5))
            sw.addstr(y,x,row)
            sw.attroff(curses.color_pair(5))
        else:
            sw.addstr(y,x,row)
    sw.refresh()

# title
def print_title(sw,h,w):
    sw.clear()
    services=open('data.json',"r")
    data=json.loads(services.read())
    x=w//2
    y=h//2-5
    sw.addstr(y-1,x-len(data['title'][0]['t'])//2, f"{data['title'][0]['t']}",curses.color_pair(3))
    sw.addstr(y,x-len(data['title'][1]['t'])//2, f"{data['title'][1]['t']}",curses.color_pair(4))
    sw.addstr(y+1,x-(len(data['title'][2]['t'])//2), f"{data['title'][2]['t']}",curses.color_pair(1))
    # sw.addstr(h-2,x-(len(data['title'][3]['t'])//2), f"{data['title'][3]['t']}",curses.color_pair(1))
    services.close()
    sw.refresh()

# Categories
def print_categories(sw):
    sw.clear()
    h, w = sw.getmaxyx()
    x = w//2# - len(http_connect.main_http(sw))//2
    y = h//2
    sw.addstr(y, x, str(cat.main(sw)))
    sw.refresh()

# Status
def print_status(sw):
    sw.clear()
    h, w = sw.getmaxyx()
    x = w//2# - len(http_connect.main_http(sw))//2
    y = h//2
    sw.addstr(y, x, str(status.main(sw)))
    sw.refresh()

# Initialize RokMe
def main(sw):
    curses.curs_set(0)
    # initialize sets of background/foreground colors
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(5, curses.COLOR_BLACK, curses.COLOR_YELLOW)
    curses.init_pair(6, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(7, curses.COLOR_RED, curses.COLOR_YELLOW)
    curses.init_pair(8, curses.COLOR_BLACK, curses.COLOR_BLACK)
    # background standard screen
    sw.bkgd(curses.color_pair(1))

    # load main menu
    current_row=len(menu)-1
    print_menu(sw,current_row)
    sw.refresh()
    
    # navigate main menu
    while 1:
        key = sw.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_UP and current_row == 0:
            current_row += len(menu)-1
        elif key == curses.KEY_DOWN and current_row == len(menu)-1:
            current_row -= len(menu)-1
        elif key == curses.KEY_DOWN and current_row < len(menu)-1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            # if user selected last row, exit the program
            if current_row == len(menu)-1:
                break
            elif menu[current_row] == menu[0]:
                print_categories(sw)
            elif menu[current_row] == menu[1]:
                print_status(sw)

        print_menu(sw, current_row)
        sw.refresh()

if __name__ == "__main__":
    curses.wrapper(main)