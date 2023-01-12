# RokMe - @mastyDev 2023.01
import curses
import os
import time
import yaml
import json
import psutil

# laod yaml file
status = yaml.safe_load(open("config.yml", "r"))
# load json file
services=open('data.json',"r")
data=json.loads(services.read())

def main(sw):
    sw.clear()
    h,w=sw.getmaxyx()
    stw=curses.newwin(16,64,(h//2)-7,(w//2)-32)
    stw.bkgd(curses.color_pair(2))
    stw.refresh()
    wy,wx=stw.getmaxyx()
    y = wy//2
    x = wx//2
    if status['ACTIVE'] == False:
        # stw.addstr(y-5,x-len(f" {} ")//2,f" {} ",curses.color_pair(6))
        stw.addstr(y,x-len(f" {data['title'][6]['t']} ")//2,f" {data['title'][6]['t']} ",curses.color_pair(7))
        while 1:
                clk=stw.getch()
                if clk == curses.KEY_ENTER or clk in [10, 13]:
                    break
                elif clk == ord('q'):
                    break
    else:
        stw.addstr(y-6,x-len(f" {status['NAME']} ")//2,f" {status['NAME']} ",curses.color_pair(5))
        stw.addstr(y-4,x-len(f" {status['TYPE']} {status['TPORT']} ")//2,f" {status['TYPE']} {status['TPORT']} ",curses.color_pair(1))
        stw.addstr(y-2,x-len(f" {status['TUNNEL']} ")//2,f" {status['TUNNEL']} ",curses.color_pair(1),)
        stw.addstr(y,x-len(f" {data['title'][4]['t']} ")//2,f" {data['title'][4]['t']} ",curses.color_pair(6))
        stw.addstr(y,x-len(f" {data['title'][7]['t']} ")//2,f" {data['title'][7]['t']} ",curses.color_pair(6))
        stw.addstr(y+2,x-len(f" PID: {str(status['PID'])} ")//2,f" PID: {str(status['PID'])} ")
        # buttons
        stw.addstr(wy-2,x-29," [Q] BACK ",curses.color_pair(1))
        stw.addstr(wy-2,x-3," press [ENTER] to ",curses.color_pair(2))
        stw.addstr(wy-2,wx-17," CLOSE TUNNEL ",curses.color_pair(4))
        while 1:
                clk=stw.getch()
                if clk == curses.KEY_ENTER or clk in [10, 13]:
                    # kill the ngrok process
                    for process in psutil.process_iter():
                        if process.name() == 'ngrok':
                            os.system("kill -9 "+str(process.pid))
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
                    stw.clear()
                    time.sleep(.5)
                    break
                elif clk == ord('q'):
                    break