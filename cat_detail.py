# RokMe - @mastyDev 2023.01
import service
import curses
import json

# Services for the selected category
def print_service_list(sw,service_row,cat_name,menu):
    sw.clear()
    h,w=sw.getmaxyx()
    x=w//4
    sw.addstr(h//2-len(menu)//2-3,x,cat_name,curses.color_pair(5))
    for idx,row in enumerate(menu): 
        y=h//2-len(menu)//2+idx
        if idx == service_row:
            sw.attron(curses.color_pair(2))
            sw.addstr(y,x,row[1:])
            sw.attroff(curses.color_pair(2))
        else:
            sw.addstr(y,x,row[1:])
    sw.refresh()

# Category Details - cat_detail.py
def print_service(sw,cat_id):
    sw.clear()
    h, w = sw.getmaxyx()
    sw.addstr(h//2,w//2,str(service.main(sw,cat_id)))
    # sw.refresh()

# Services List Main
def main(sw,cat_row):
    # filter services with same category
    services=open('data.json',"r")
    data=json.loads(services.read())
    cat_name=f"{data['categories'][cat_row-1]['name']}"
    menu=[" [Q] Back"]
    for i in data['services']:
        if i['type'] == 'http' and i['cat'] == cat_row:
            menu.append(f"{cat_row}[{i['type']}][{i['port']}] {i['desc']}")
        if i['type'] == 'tcp' and i['cat'] == cat_row:
            menu.append(f"{cat_row}[{i['type']}][{i['port']}] {i['desc']}")
    services.close()
    
    # main detail menu
    service_row=0
    print_service_list(sw,service_row,cat_name,menu)
    sw.refresh()
    
    # navigate menu
    while 1:
        serv = sw.getch()
        if serv == ord('q'):
            break
        elif serv == curses.KEY_UP and service_row > 0:
            service_row -= 1
        elif serv == curses.KEY_UP and service_row == 0:
            service_row += len(menu)-1
        elif serv == curses.KEY_DOWN and service_row == len(menu)-1:
            service_row -= len(menu)-1
        elif serv == curses.KEY_DOWN and service_row < len(menu)-1:
            service_row += 1
        # debug
        # sw.addstr(0,1,f"sel: {service_row}")
        # sw.refresh()
        # on press Enter
        if serv == curses.KEY_ENTER or serv in [10, 13]:
            if service_row == 0:
                break
            elif service_row != 0:
                print_service(sw,menu[service_row])
                # break

        print_service_list(sw,service_row,cat_name,menu)
        sw.refresh()