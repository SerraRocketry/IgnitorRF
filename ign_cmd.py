import os
import sys
import threading
import time
import serial
import serial.tools.list_ports
from datetime import datetime


class IgnitorRFApp:
    def __init__(self):
        self.event = threading.Event()
        self.com = None

    def update_ports(self):
        ports = check_usb_connection()
        return ports

    def connect(self, port):
        if port:
            self.com = connect(port, self)
            print('Conectado.')
        else:
            print('Selecione uma porta.')

    def disconnect(self):
        if self.com:
            disconnect(self.com, self)
            print('Desconectado.')
        else:
            print('Conecte-se primeiro.')

    def quit(self):
        if self.com:
            disconnect(self.com, self)
        print('Aplicação encerrada.')
        sys.exit(0)

    def start_countdown(self):
        self.event.clear()
        if self.com:
            self.countdown = threading.Thread(
                target=count_down, args=(self.com, self)).start()
        else:
            print('Conecte-se primeiro.')

    def cancel(self):
        self.event.set()
        if self.com:
            print('Contagem cancelada.')
        else:
            print('Conecte-se primeiro.')


def get_date_time() -> str:
    now = datetime.now()
    return now.strftime('%H:%M:%S.%f')[:-3] + ' -> '


def connect(port: str, app: IgnitorRFApp) -> serial.Serial:
    com = serial.Serial(port, 9600, timeout=1)
    threading.Thread(target=recebido, args=(com, app)).start()
    return com


def disconnect(com: serial.Serial, app: IgnitorRFApp):
    com.close()
    print('Desconectado.')


def recebido(com: serial.Serial, app: IgnitorRFApp):
    while check_still_connect(com):
        try:
            com.isOpen()
            com.reset_output_buffer()
            com.write(b'A')
            msg = com.readline().decode().strip()
            if msg:
                print(get_date_time() + msg)
            else:
                print('Desconectado do Ignitor.')
        except serial.SerialException:
            print('Falha na conexão.')
            disconnect(com, app)
            break
        time.sleep(0.5)


def send_command(com: serial.Serial, command: bytes, app: IgnitorRFApp):
    try:
        com.isOpen()
        com.reset_output_buffer()
        com.write(command)
        msg = com.readline().decode().strip()
        print(msg)
    except serial.SerialException:
        print('Falha na conexão.')


def fire(com: serial.Serial, app: IgnitorRFApp):
    send_command(com, b'1', app)


def deactivate(com: serial.Serial, app: IgnitorRFApp):
    send_command(com, b'0', app)
    app.cancel()


def count_down(com: serial.Serial, app: IgnitorRFApp):
    try:
        com.isOpen()
        esp_save_log(com, app)
        for cont in range(11):
            if cont < 10:
                print(f'Ativando em: {10 - cont}')
            else:
                fire(com, app)
                time.sleep(5)
                deactivate(com, app)
                break
            time.sleep(1)
            if app.event.is_set():
                deactivate(com, app)
                break
    except serial.SerialException:
        print('Falha na conexão.')
        esp_stop_log(com, app)


def esp_save_log(com: serial.Serial, app: IgnitorRFApp):
    send_command(com, b'C', app)


def esp_stop_log(com: serial.Serial, app: IgnitorRFApp):
    send_command(com, b'D', app)


def save_serial_log(msg: str):
    try:
        dia, hora, *dados = msg.split(';')
        filename = f'log_{dia}_{hora}.txt'
        mode = 'a' if os.path.exists(filename) else 'w'
        with open(filename, mode) as file:
            file.write(f'{msg}\n')
    except Exception as e:
        print('Falha ao salvar log.')
        print(e)


def get_com_ports() -> list:
    return [port.device for port in list(serial.tools.list_ports.comports())]


def get_usb_ports() -> list:
    return [port.device for port in list(serial.tools.list_ports.comports()) if '/dev/ttyUSB' in port.device or '/dev/serial' in port.device]


def check_usb_connection() -> list:
    if sys.platform.startswith('win'):
        return get_com_ports()
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        return get_usb_ports()
    return []


def check_still_connect(com: serial.Serial) -> bool:
    return com.port in check_usb_connection()


if __name__ == '__main__':
    app = IgnitorRFApp()
    while True:
        print("\nMenu:")
        print("1. Listar portas")
        print("2. Conectar")
        print("3. Desconectar")
        print("4. Iniciar contagem")
        print("5. Cancelar contagem")
        print("6. Sair")
        choice = input("Escolha uma opção: ")

        if choice == '1':
            ports = app.update_ports()
            print("Portas disponíveis:", ports)
        elif choice == '2':
            port = input("Digite a porta para conectar: ")
            app.connect(port)
        elif choice == '3':
            app.disconnect()
        elif choice == '4':
            app.start_countdown()
        elif choice == '5':
            app.cancel()
        elif choice == '6':
            app.quit()
        else:
            print("Opção inválida.")
