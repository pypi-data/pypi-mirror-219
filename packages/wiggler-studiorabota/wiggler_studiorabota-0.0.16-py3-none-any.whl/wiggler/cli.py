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
        shutil.copyfile(scriptFile, '/usr/bin/start_wiggler.sh')
        shutil.copyfile(serviceFile, '/etc/systemd/system/start_wiggler.service')
        os.system('systemctl enable start_wiggler')