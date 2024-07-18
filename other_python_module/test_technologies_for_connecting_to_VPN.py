import subprocess
import os
import configparser


def create_vpn_connection(vpn_name, server_address):
    try:
        create_vpn_command = (
            f'PowerShell -Command "Add-VpnConnection -Name \'{vpn_name}\' -ServerAddress \'{server_address}\' '
            f'-TunnelType IKEv2 -AuthenticationMethod MachineCertificate -EncryptionLevel Required '
            f'-SplitTunneling $False -RememberCredential"'
        )

        subprocess.run(create_vpn_command, shell=True, check=True)
        print(f"VPN подключение {vpn_name} создано.")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании VPN подключения: {e}")


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('vpn_config.ini')

    vpn_name = config['VPN']['vpn_name']
    server_address = config['VPN']['server_address']

    # Создаем VPN подключение
    create_vpn_connection(vpn_name, server_address)
