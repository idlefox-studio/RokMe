# RokMe - @mastyDev 2023.01
import cat_detail
import curses
import json

# services.json - categories
services=open('data.json',"r")
data=json.loads(services.read())
menu=[]
menu.append("[Q] Back\n\n")
for i in data['categories']:
    menu.append(f"[{i['cat']}] {i['name']}")
services.close()

# category menu
def print_categories(sw, selected_row):
    sw.clear()
    h,w=sw.getmaxyx()
    x=w//4
    sw.addstr(h//2-len(menu)//2-1,x,"Categories",curses.color_pair(5))
    for idx,row in enumerate(menu):
        y=h//2-len(menu)//2+idx+2
        if idx == selected_row:
            sw.attron(curses.color_pair(2))
            sw.addstr(y,x,row)
            sw.attroff(curses.color_pair(2))
        else:
            sw.addstr(y,x,row)
    sw.refresh()

# Category Details - cat_detail.py
def print_detail(sw,cat_row):
    sw.clear()
    h, w = sw.getmaxyx()
    x = w//3
    y = h//2
    sw.addstr(y, x, str(cat_detail.main(sw,cat_row)))
    sw.refresh()

# Categories List Main
def main(sw):
    # main menu
    cat_row=0
    print_categories(sw,cat_row)
    sw.refresh()
    # navigate menu
    while 1:
        cat = sw.getch()
        if cat == ord('q'):
            break
        elif cat == curses.KEY_UP and cat_row > 0:
            cat_row -= 1
        elif cat == curses.KEY_UP and cat_row == 0:
            cat_row += len(menu)-1
        elif cat == curses.KEY_DOWN and cat_row == len(menu)-1:
            cat_row -= len(menu)-1
        elif cat == curses.KEY_DOWN and cat_row < len(menu)-1:
            cat_row += 1

        # on press Enter
        if cat == curses.KEY_ENTER or cat in [10, 13]:
            if cat_row == 0:
                break
            elif cat_row != 0:
                print_detail(sw,cat_row)
        
        print_categories(sw, cat_row)
        sw.refresh()