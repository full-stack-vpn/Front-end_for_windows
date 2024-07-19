import subprocess
import configparser

def check_vpn_connection_exists(vpn_name):
    try:
        check_command = f'PowerShell -Command "Get-VpnConnection -Name \'{vpn_name}\'"'
        result = subprocess.run(check_command, shell=True, capture_output=True, text=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        return False

def remove_vpn_connection(vpn_name):
    try:
        remove_command = f'PowerShell -Command "Remove-VpnConnection -Name \'{vpn_name}\' -Force"'
        subprocess.run(remove_command, shell=True, check=True)
        print(f"VPN подключение {vpn_name} удалено.")
    except subprocess.CalledProcessError as e:
        print(f"VPN подключение {vpn_name} не было найдено для удаления.")

def create_vpn_connection(vpn_name, server_address, auth_method, encryption_level, remember_credential, split_tunneling):
    try:
        if check_vpn_connection_exists(vpn_name):
            print(f"VPN подключение {vpn_name} уже существует.")
            return

        create_vpn_command = (
            f'PowerShell -Command "Add-VpnConnection -Name \'{vpn_name}\' -ServerAddress \'{server_address}\' '
            f'-TunnelType L2TP -AuthenticationMethod {auth_method} -EncryptionLevel {encryption_level} '
            f'-RememberCredential $True -SplitTunneling $({str(split_tunneling).lower()})"'
        )

        subprocess.run(create_vpn_command, shell=True, check=True)
        print(f"VPN подключение {vpn_name} создано с параметром SplitTunneling={split_tunneling}.")

    except subprocess.CalledProcessError as e:
        print(f"Ошибка при создании VPN подключения: {e}")

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('vpn_config.ini')

    vpn_name = config['VPN']['vpn_name']
    server_address = config['VPN']['server_address']
    auth_method = config['VPN'].get('authentication_method', 'PAP')  # Default to PAP if not specified
    encryption_level = config['VPN'].get('encryption_level', 'Required')
    remember_credential = config['VPN'].getboolean('remember_credential', True)
    split_tunneling = config['VPN'].getboolean('split_tunneling', False)

    # Удаляем существующее VPN подключение, если оно есть
    remove_vpn_connection(vpn_name)

    # Создаем VPN подключение
    create_vpn_connection(vpn_name, server_address, auth_method, encryption_level, remember_credential, split_tunneling)
