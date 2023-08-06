import argparse
import os
import shutil
from pathlib import Path

def main():
  
    parser = argparse.ArgumentParser(prog ='wiggler', description ='WiggleR API')

    parser.add_argument('-s', '--server', action='store_true')
    parser.add_argument('-b', '--boot', action='store_true')
    
    args = parser.parse_args()
  
    if args.server:
        os.system(f"uvicorn wiggler.main:app --reload --host 0.0.0.0")

    if args.boot:
        scriptFile = Path(__file__).parent / f"start_wiggler.sh"
        serviceFile = Path(__file__).parent / f"start_wiggler.service"
        os.system(f'sudo cp {scriptFile} /usr/bin/start_wiggler.sh')
        os.system(f'sudo cp {serviceFile} /etc/systemd/user/start_wiggler.service')
        os.system('systemctl --user enable start_wiggler.service')