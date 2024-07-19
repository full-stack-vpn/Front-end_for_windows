import subprocess
import logging
import sys
import os
from time import sleep
#from stop import stop_vpn_processes


def start_vpn(config_path, log_file='vpn_output.log'):
    """
    Запускает OpenVPN с указанным конфигурационным файлом и записывает вывод в лог-файл.

    :param config_path: Путь к конфигурационному файлу OpenVPN.
    :param log_file: Путь к файлу для записи логов.
    :return: Объект процесса.
    """
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Путь к openvpn в контейнере
    openvpn_path = '/usr/sbin/openvpn'

    # Проверка, существует ли файл
    if not os.path.isfile(openvpn_path):
        logging.error(f"OpenVPN executable not found at {openvpn_path}")
        sys.stderr.write(f"OpenVPN executable not found at {openvpn_path}\n")
        return None

    command = [openvpn_path, '--config', config_path]

    try:
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        sys.stderr.write(f"An error occurred: {e}\n")
        return None


def vpn_process_manager(config_path, timeout=60):
    """
    Менеджер процесса VPN: запускает и затем корректно останавливает VPN.

    :param config_path: Путь к конфигурационному файлу OpenVPN.
    :param timeout: Время ожидания завершения процесса OpenVPN в секундах.
    """
    # Запуск OpenVPN
    vpn_process = start_vpn(config_path)
    if vpn_process is None:
        logging.error("Не удалось запустить OpenVPN.")
        return

    try:
        print("Ожидание завершения процесса OpenVPN...")
        # Ожидание завершения процесса с таймаутом
        vpn_process.wait(timeout=timeout)
        print("Процесс OpenVPN завершен.")

    except subprocess.TimeoutExpired:
        # Если процесс не завершился в течение таймаута, принудительно завершите его
        print("Время ожидания истекло. Принудительное завершение процесса OpenVPN...")
        vpn_process.terminate()
        vpn_process.wait()  # Убедитесь, что процесс завершен
        print("Процесс OpenVPN принудительно завершен.")

    finally:
        # После завершения процесса OpenVPN, остановите другие связанные процессы
        #stop_vpn_processes()
        pass


if __name__ == "__main__":
    config_path = 'vpn_config.ovpn'

    # Запуск менеджера процесса VPN
    vpn_process_manager(config_path)
