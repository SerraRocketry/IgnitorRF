import os
import sys
import threading
import time
import serial
import serial.tools.list_ports
from datetime import datetime

# Get the current date and time as a formatted string
def get_date_time() -> str:
    now = datetime.now()
    return now.strftime('%H:%M:%S.%f')[:-3] + ' -> '

# Connect to the specified serial port
def connect(port: str) -> serial.Serial:
    com = serial.Serial(port, 9600, timeout=1)
    threading.Thread(target=recebido, args=(com,)).start()
    return com

# Disconnect from the specified serial port
def disconnect(com: serial.Serial):
    com.close()
    print('Desconectado.')

# Continuously read data from the serial port
def recebido(com: serial.Serial):
    while check_still_connect(com):
        try:
            com.isOpen()
            com.reset_output_buffer()
            start_time = datetime.now()
            com.write(b'A')
            msg = com.readline()
            msg = msg.decode("utf-8").strip()
            end_time = datetime.now()
            ping = (end_time - start_time).total_seconds() * 1000
            if msg:
                print(f'{ping:.2f}ms - {get_date_time()}{msg}')
            else:
                print(get_date_time() + 'Desconectado do Ignitor.')
        except serial.SerialException:
            print('Falha na conexão.')
            disconnect(com)
            break
        # time.sleep(ping / 1000 if ping else 0.5)
        time.sleep(1)

# Send a command to the serial port
def send_command(com: serial.Serial, command: bytes):
    try:
        com.isOpen()
        com.reset_output_buffer()
        com.write(command)
        msg = com.readline()
        msg = msg.decode("utf-8").strip()
        print(get_date_time() + msg)
    except serial.SerialException:
        print('Falha na conexão.')

# Send the fire command to the serial port
def fire(com: serial.Serial):
    send_command(com, b'1')

# Send the deactivate command to the serial port
def deactivate(com: serial.Serial):
    send_command(com, b'0')

# Countdown process before firing
def count_down(com: serial.Serial, event: threading.Event):
    try:
        com.isOpen()
        send_command(com, b'C')
        for cont in range(11):
            if cont < 10:
                print(f'Ativando em: {10 - cont}')
            else:
                fire(com)
                event.wait(1)
                deactivate(com)
                break
            event.wait(1)
            if event.is_set():
                deactivate(com)
                break
    except serial.SerialException:
        print('Falha na conexão.')

# Save the serial log to a file
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

# Get a list of available COM ports
def get_com_ports() -> list:
    return [port.device for port in list(serial.tools.list_ports.comports())]

# Get a list of available USB ports
def get_usb_ports() -> list:
    return [port.device for port in list(serial.tools.list_ports.comports()) if '/dev/ttyUSB' in port.device or '/dev/serial' in port.device]

# Check the available USB connections
def check_usb_connection() -> list:
    if sys.platform.startswith('win'):
        return get_com_ports()
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        return get_usb_ports()
    return []

# Check if the serial port is still connected
def check_still_connect(com: serial.Serial) -> bool:
    return com.port in check_usb_connection()

# Main entry point of the application
if __name__ == '__main__':
    ports = check_usb_connection()
    if ports:
        print('Portas disponíveis:', )
        for i, port in enumerate(ports):
            print(f'{i + 1}: {port}')
        port = input('Selecione uma porta: ')
        try:
            port = ports[int(port) - 1]
        except (ValueError, IndexError):
            print('Porta inválida.')
            sys.exit(1)
        if port in ports:
            com = connect(port)
            event = threading.Event()
            while True:
                command = input('Digite um comando (conectar, desconectar, iniciar, cancelar, sair): ').strip().lower()
                if command == 'conectar':
                    com = connect(port)
                elif command == 'desconectar':
                    disconnect(com)
                elif command == 'iniciar':
                    event.clear()
                    threading.Thread(target=count_down, args=(com, event)).start()
                elif command == 'cancelar':
                    event.set()
                    deactivate(com)
                elif command == 'sair':
                    disconnect(com)
                    break
                else:
                    print('Comando inválido.')
    else:
        print('Nenhuma porta disponível.')
        sys.exit(1)