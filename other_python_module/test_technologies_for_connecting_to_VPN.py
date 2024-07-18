import subprocess
import os
import configparser


def delete_vpn_connection(vpn_name):
    try:
        delete_vpn_command = (
            f'PowerShell -Command "Remove-VpnConnection -Name \'{vpn_name}\' -Force"'
        )
        subprocess.run(delete_vpn_command, shell=True, check=True)
        print(f"VPN подключение {vpn_name} удалено.")
    except subprocess.CalledProcessError as e:
        # Если VPN подключение не найдено, ошибка будет игнорироваться
        pass


def create_vpn_connection(vpn_name, server_address, tunnel_type, auth_method, encryption_level, remember_credential):
    try:
        # Удаляем существующее VPN подключение, если оно уже существует
        delete_vpn_connection(vpn_name)

        # Создаем новое VPN подключение
        create_vpn_command = (
            f'PowerShell -Command "Add-VpnConnection -Name \'{vpn_name}\' -ServerAddress \'{server_address}\' '
            f'-TunnelType {tunnel_type} -AuthenticationMethod {auth_method} -EncryptionLevel {encryption_level} '
            f'-RememberCredential $True"'
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
    tunnel_type = config['VPN'].get('tunnel_type', 'IKEv2')
    auth_method = config['VPN'].get('authentication_method', 'MachineCertificate')
    encryption_level = config['VPN'].get('encryption_level', 'Required')
    remember_credential = config['VPN'].getboolean('remember_credential', True)

    # Создаем VPN подключение
    create_vpn_connection(vpn_name, server_address, tunnel_type, auth_method, encryption_level, remember_credential)
