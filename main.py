from other_python_module import test_technologies_for_connecting_to_VPN

if __name__ == "__main__":
    config_path = 'vpn_config.ovpn'

    # Запуск менеджера процесса VPN
    test_technologies_for_connecting_to_VPN.vpn_process_manager(config_path)
