import serial
import time
import sys
import os
import serial.tools.list_ports


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def connect(com_port):
    try:
        global com
        print('Conectando à', com_port)
        com = serial.Serial(com_port, 9600, timeout=1)
    except:
        print('Não foi possível conectar, verifique a porta especificada.')
        pass
    else:
        recebido()


def disconnect():
    com.close()
    print('Desconectado.')


def ativar():
    try:
        com.isOpen()
        cont = 0
        print('Pressione Ctrl+C para cancelar.')
        while cont < 11:
            if cont < 10:
                print('Ativando em:', 10-cont)
                beep()
            if cont == 10:
                com.reset_output_buffer()
                com.write('2'.encode())
                msg = str(com.readline())
                msg = msg[2:-5]
                print(msg)
                desativar()
                break
            cont += 1
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    except:
        print('Falha na conexão.')
        pass


def desativar():
    time.sleep(5)
    com.reset_output_buffer()
    com.write('3'.encode())
    msg = str(com.readline())
    msg = msg[2:-5]
    print(msg)


def recebido():
    try:
        def check_usb_connection():
            ports = [port.device for port in list(
                serial.tools.list_ports.comports())]
            if '/dev/ttyUSB0' in ports:
                print('Conectado ao módulo RF.')
            else:
                print('Desconectado do módulo RF.')
                print('Desconectado do Ignitor.')
                raise Exception('Desconectado do módulo RF.')

        check_usb_connection()
        com.isOpen()
        com.reset_output_buffer()
        com.write('a'.encode())
        msg = str(com.readline())
        msg = msg[2:-5]
        global state
        state = False
        if msg != '':
            print(msg)
            state = True
        else:
            print('Desconectado do Ignitor.')
            state = False

    except:
        print('Falha na conexão.')
        disconnect()
        pass


def cancelar():
    print('Ativação cancelada.')
    com.write('3'.encode())


def update_ports():
    if sys.platform.startswith('win'):
        menu_port = get_com_ports()
        return menu_port
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        menu_port = get_usb_ports()
        return menu_port
    else:
        raise EnvironmentError('Unsupported platform')


def get_com_ports():
    return [port.device for port in list(serial.tools.list_ports.comports())]


def get_usb_ports():
    ports = [port.device for port in list(serial.tools.list_ports.comports())]
    return [port for port in ports if '/dev/ttyUSB' in port or '/dev/serial' in port]


def beep():
    if sys.platform.startswith('win'):
        import winsound
        winsound.Beep(1000, 500)
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        print('\a')
    else:
        raise EnvironmentError('Unsupported platform')


def get_time():
    return time.strftime("%H:%M:%S")


if __name__ == '__main__':
    comOptions = update_ports()
    st = True

    while True:
        print(get_time())
        if st:
            print('1. Conectar')
            print('2. Sair')

            choice = input('Escolha uma opção: ')

            if choice == '1':
                print('Portas disponíveis:')
                for i, port in enumerate(comOptions):
                    print(f'{i+1}. {port}')
                selected_port = input('Escolha uma porta: ')
                if selected_port.isdigit() and int(selected_port) <= len(comOptions):
                    connect(comOptions[int(selected_port)-1])
                    st = False
                else:
                    print('Porta inválida. Tente novamente.')
            elif choice == '2':
                break
            else:
                print('Opção inválida. Tente novamente.')
        else:
            recebido()

            print('1. Desconectar')
            print('2. Verificar conexão')
            print('3. Iniciar contagem')
            print('4. Sair')

            choice = input('Escolha uma opção: ')

            if choice == '1':
                disconnect()
                st = True
            elif choice == '2':
                recebido()
            elif choice == '3':
                if state:
                    ativar()
                else:
                    print('Ignitor fora da rede.')
            elif choice == '4':
                break
            else:
                print('Opção inválida. Tente novamente.')

        time.sleep(2)
        clear_screen()

    if com is not None:
        com.close()
