from .ota_updater import OTAUpdater
from machine import reset

def download_and_install_update_if_available():
    token = "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"
    config_data = config()
    if 'ssid' in config_data:
        o = OTAUpdater(github_repo='https://github.com/kumar-dheeraj/smart-school-bell',github_src_dir='src',main_dir='app',headers={'Authorization': 'token {}'.format(token)})
        o.check_for_update_to_install_during_next_reboot()
        status = o.install_update_if_available_after_boot(config_data['ssid'], config_data['password'])
        if status:
            reset()
    else:
        print('No WIFI configured, skipping updates check')



def config():
    with open('wifi.dat') as f:
        lines = f.readlines()
    f.close()
    config_data = {}
    for line in lines:
        ssid, password = line.strip("\n").split(";")
    config_data['ssid']=ssid
    config_data['password']=password
    return config_data
