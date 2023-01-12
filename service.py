# RokMe - @mastyDev 2023.01
import curses
import json
import yaml
import time
import os
import subprocess

# check config status
check = yaml.safe_load(open("config.yml", "r"))
# load data file
services=open('data.json',"r")
data=json.loads(services.read())

# service window
def main(sw,cat_id):
    h, w = sw.getmaxyx()
    sw.clear()
    
    # format service data
    def set_str(section):
        service_name=cat_id.split(" ",1)
        typeport = service_name[0].split('][')
        if section == 'id':
            return typeport[0][0]
        elif section == 'name':
            return service_name[1]
        elif section == 'type':
            type = typeport[0][2:]
            return type
        else:
            port = typeport[1][:-1]
            return port

            
    # STOP SERVICE window         
    def CLOSE_tunnel():
        pw=curses.newwin(16,64,(h//2)-7,(w//2)-32)
        pw.refresh()
        pw.bkgd(curses.color_pair(5))
        y,x = pw.getmaxyx()
        ngrok_command = f"ngrok {set_str('type')} {set_str('port')}"
        pw.attron(curses.A_BOLD)
        pw.addstr(2,x//2-len(f" {set_str('name')} ")//2,f" {set_str('name')} ",curses.color_pair(6))
        pw.addstr(5,x//2-len(f" [{ngrok_command}] ")//2,f" [{ngrok_command}] ",curses.color_pair(1))
        pw.attroff(curses.A_BOLD)
        pw.addstr(y-2,2," [Q] BACK ",curses.color_pair(2))
        pw.addstr(8,x//2-len(f" {data['loading'][11]['l']} ")//2,f" {data['loading'][11]['l']} ",curses.color_pair(5))
        if check['TUNNEL'] != '':
            pw.addstr(10,x//2-len(check['TUNNEL'])//2,f" {check['TUNNEL']} ",curses.color_pair(1))

        pw.addstr(12,x//2-len(data['title'][8]['t'])//2,data['title'][8]['t'],curses.color_pair(2))
        pw.addstr(y-2,x-(len(" CLOSE ")+2)," CLOSE ",curses.color_pair(4))
        pw.refresh()
        while 1:
            clk=pw.getch()
            if clk == curses.KEY_ENTER or clk in [10, 13]:
                # kill the ngrok process
                os.system("kill -9 "+str(check['PID']))   
 
                # reset config.yml
                cover=data['title'][5]['t']
                pw.addstr(10,x//2-len(f"    {cover}    ")//2,f"    {cover}    ",curses.color_pair(5))
                pw.addstr(12,x//2-len(cover)//2,cover,curses.color_pair(5))
                config={'ACTIVE':False,
                    'CAT':0,
                    'NAME':'',
                    'TPORT':0,
                    'TUNNEL':'',
                    'TYPE':'',
                    'PID':0
                    }
                with open('config.yml','w') as yaml_file:
                    yaml.dump(config, yaml_file, default_flow_style=False) 
                pw.refresh()
                time.sleep(1)
                break
            else:
                break

    # START SERVICE window
    def OPEN_tunnel():
        pw=curses.newwin(16,64,(h//2)-7,(w//2)-32)
        pw.refresh() 
        pw.bkgd(curses.color_pair(2))
        y,x = pw.getmaxyx()
        ngrok_command = f"ngrok {set_str('type')} {set_str('port')}"
        pw.attron(curses.A_BOLD)
        pw.addstr(2,x//2-len(f" {set_str('name')} ")//2,f" {set_str('name')} ",curses.color_pair(6))
        pw.addstr(5,x//2-len(f" [{ngrok_command}] ")//2,f" [{ngrok_command}] ",curses.color_pair(1))
        pw.attroff(curses.A_BOLD)
        pw.addstr(y-2,2," [Q] BACK ",curses.color_pair(5))
        pw.addstr(8,x//2-len(f" {data['loading'][0]['l']} ")//2,f" {data['loading'][0]['l']} ",curses.color_pair(2))
        pw.addstr(y-2,x//2+2," press [ENTER] to ",curses.color_pair(2))
        pw.addstr(y-2,x-(len(" ACTIVATE ")+2)," ACTIVATE ",curses.color_pair(5))
        pw.refresh() 
        while 1:
            k=pw.getch()
            # [enter] that start ngrok tunnel
            if k == curses.KEY_ENTER or k in [10, 13]:
                # launch ngrok pytjon script in background
                cmd="python -u ng_connect.py > rokme.log &"
                subprocess.Popen(cmd,shell=True)
                    
                config={'ACTIVE':False,
                        'CAT':int(set_str('id')),
                        'NAME':set_str('name'),
                        'TPORT':int(set_str('port')),
                        'TUNNEL':'',
                        'TYPE':set_str('type'),
                        'PID':0
                        }
                with open('config.yml','w') as yaml_file:
                    yaml.dump(config, yaml_file, default_flow_style=False) 
                        
                cover=data['title'][5]['t']
                for i in data['loading']:
                    pw.addstr(8,x//2-len(f" {i['l']} ")//2,f" {i['l']} ",curses.color_pair(2))
                    time.sleep(.1)
                    pw.refresh()

                pw.addstr(y-2,x-(len(cover)+2),cover,curses.color_pair(8))
                pw.addstr(8,x//2-len(f" {data['loading'][11]['l']} ")//2,f" {data['loading'][11]['l']} ",curses.color_pair(5))
                pw.addstr(12,x//2-len(data['title'][8]['t'])//2,data['title'][8]['t'],curses.color_pair(2))
                time.sleep(2)
                pw.addstr(10,x//2-len(check['TUNNEL'])//2,f" {check['TUNNEL']} ",curses.color_pair(1))
                pw.refresh()
                time.sleep(1)
                CLOSE_tunnel()
                break
            elif k == ord('q'):
                break

    if check['ACTIVE'] == True and check['NAME'] == set_str('name') and set_str('id') != 0:
        CLOSE_tunnel()
    elif check['ACTIVE'] == False or check['PID'] !=0:        
        OPEN_tunnel()
