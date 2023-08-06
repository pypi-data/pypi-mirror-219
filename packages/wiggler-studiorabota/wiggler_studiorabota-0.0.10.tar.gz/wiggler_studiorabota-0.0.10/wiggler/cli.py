import argparse
import os

def main():
  
    parser = argparse.ArgumentParser(prog ='wiggler', description ='WiggleR API')

    parser.add_argument('-s', '--server', action='store_true')
    parser.add_argument('-b', '--boot', action='store_true')
    
    args = parser.parse_args()
  
    if args.server:
        os.system(f"uvicorn wiggler.main:app --reload --host 0.0.0.0")

    if args.boot:
         os.system(f'cp {os.path.abspath("start_wiggler.sh")} /usr/bin/start_wiggler.sh')
         os.system(f'cp {os.path.abspath("start_wiggler.service")} /etc/systemd/system/start_wiggler.service')
         os.system('systemctl enable start_wiggler')