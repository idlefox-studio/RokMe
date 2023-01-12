# @mastyDev 2023.01
from pyngrok import conf, ngrok
import psutil
import time
import yaml
import os

#ngrok config
ngrok_process = ngrok.get_ngrok_process()
ngrok.set_auth_token(os.environ["NGROK_TOKEN"])

# start Ngrok
def start_ngrok():
    conf.get_default().region = "eu"
    tunnel = yaml.safe_load(open("config.yml", "r"))
    # Start ngrok tunnel
    ulr = ngrok.connect(tunnel['TPORT'], f"{tunnel['TYPE']}")
    link = str(ulr)
    link = link.split("\"",1)[1]
    link = link.split("\"",1)[0]
    time.sleep(1)
    for process in psutil.process_iter():
        if process.name() == 'ngrok':
            ngrok_pid=process.pid

    # update config with link
    config={'ACTIVE':True,
            'CAT':int(tunnel['CAT']),
            'NAME':tunnel['NAME'],
            'TPORT':int(tunnel['TPORT']),
            'TUNNEL':link,
            'TYPE':tunnel['TYPE'],
            'PID':ngrok_pid
            }
    with open('config.yml','w') as yaml_file:
        yaml.dump(config, yaml_file, default_flow_style=False) 
    time.sleep(3)

if __name__ == "__main__":
    start_ngrok()
    try:
        ngrok_process.proc.wait()
    except:
        ngrok.kill()