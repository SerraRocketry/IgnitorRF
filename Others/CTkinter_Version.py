import sys
import threading
import time
import serial
import serial.tools.list_ports
import customtkinter as Ctk
from datetime import datetime


class IgnitorRFApp(Ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Ignitor RF')
        self.geometry('1280x720')
        self.event = threading.Event()
        self.com = None

        self._configure_ui()

    def _configure_ui(self):
        self._configure_grid()
        self._configure_buttons()
        self._configure_labels()
        self._update_ports()

    def _configure_grid(self):
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)

    def _configure_buttons(self):
        self.btn_conectar = self._create_button('Conectar', self.connect, 0, 0)
        self.btn_ativar = self._create_button(
            'Iniciar contagem', self.start_countdown, 0, 2)
        self.btn_fechar = self._create_button('Fechar', self.quit, 3, 2)
        self.btn_save_log = self._create_button(
            'Salvar Log', self.save_log, 3, 1)
        self.btn_tare = self._create_button(
            'Tare', self.send_tare, 2, 2, hidden=True)
        self.btn_reiniciar = self._create_button(
            'Reiniciar', self.restart, 2, 0, hidden=True)

    def _create_button(self, text, command, row, col, hidden=False):
        button = Ctk.CTkButton(
            self, text=text, command=command, height=80, width=120, font=('Arial', 20))
        button.grid(row=row, column=col, padx=20, pady=10)
        if hidden:
            button.grid_remove()
        return button

    def _configure_labels(self):
        self.label_status = Ctk.CTkLabel(
            self, text='Aguardando conexão.', font=('Arial', 30))
        self.label_status.grid(row=1, column=1, padx=20, pady=10)

        self.label_message = Ctk.CTkTextbox(
            self, width=620, corner_radius=0, font=('Courier', 20))
        self.label_message.grid(row=2, column=1, padx=20, pady=10)

    def _update_ports(self):
        ports = check_usb_connection()
        self.menu_port = Ctk.CTkOptionMenu(self, values=ports)
        self.menu_port.grid(row=3, column=0, padx=20, pady=10)
        self.menu_port.set('/dev/ttyUSB0')

    def connect(self):
        port = self.menu_port.get()
        if port != 'Portas':
            self.com = connect(port, self)
            self.label_status.configure(text='Aguardando comando.')
            self.btn_conectar.configure(
                text='Desconectar', command=self.disconnect)
            self.btn_tare.grid()
            self.btn_reiniciar.grid()
        else:
            self.label_status.configure(text='Selecione uma porta.')

    def disconnect(self):
        if self.com:
            disconnect(self.com, self)
            self.btn_conectar.configure(text='Conectar', command=self.connect)
            self.btn_tare.grid_remove()
            self.btn_reiniciar.grid_remove()
    
    def restart(self):
        esp_reboot(self)

    def quit(self):
        if self.com:
            disconnect(self.com, self)
        self.destroy()

    def start_countdown(self):
        if self.com:
            self.event.clear()
            threading.Thread(target=count_down, args=(self.com, self)).start()
            self.btn_ativar.configure(text='Cancelar', command=self.cancel)
        else:
            self.label_status.configure(text='Conecte-se primeiro.')

    def cancel(self):
        self.event.set()
        self.btn_ativar.configure(
            text='Iniciar contagem', command=self.start_countdown)

    def save_log(self):
        save_serial_log(self.label_message.get("1.0", "end-1c"))

    def send_tare(self):
        if self.com:
            esp_tare()

def handle_msg(msg: str):
    global comma
    msg = msg.decode("utf-8").strip()

    if msg in {'Ativado.', 'Desativado.', 'Iniciando contagem.', 'Zerando célula.', 'Comando desconhecido.', 'Reiniciando.'}:
        comma = None

    return msg

def get_date_time() -> str:
    return datetime.now().strftime('%H:%M:%S.%f')[:-3] + ' -> '


def connect(port: str, app: IgnitorRFApp) -> serial.Serial:
    try:
        com = serial.Serial(
            port,
            baudrate=9600,
            timeout=0.5,
            xonxoff=False,
            rtscts=False,
            write_timeout=0.5,
            dsrdtr=False,
            inter_byte_timeout=None
        )
        global comma
        comma = None
        threading.Thread(target=recebido, args=(com, app), daemon=True).start()
        return com
    except serial.SerialException as e:
        app.label_status.configure(text=f'Erro ao conectar: {e}')
        raise

def disconnect(com: serial.Serial, app: IgnitorRFApp):
    com.close()
    app.label_status.configure(text='Desconectado.')


def recebido(com: serial.Serial, app: IgnitorRFApp):
    while check_still_connect(com):
        global comma
        try:
            start_time = datetime.now()
            com.reset_output_buffer()
            com.reset_input_buffer()

            command = comma or b'A'

            com.write(command)
            msg = com.readline()
            hmsg = handle_msg(msg)
            print(f'Msg: {hmsg}', end=' | ')
            end_time = datetime.now()

            ping = (end_time - start_time).total_seconds() * 1000
            print(f'Ping: {ping:.2f} ms')

            log_message = get_date_time() + (hmsg if hmsg else 'Desconectado do Ignitor.') + '\n'
            app.label_message.insert("0.0", log_message)

            if hmsg == 'Ativado.':
                app.label_status.configure(text='Ativado.')
            elif hmsg == 'Desativado.': 
                app.label_status.configure(text='Aguardando comando.')

        except serial.SerialException as e:
            print(f'Erro de comunicação: {e}')
        except Exception as e:
            app.label_status.configure(text=f'Erro inesperado: {e}')
            raise
        time.sleep(ping / 1000)


def send_command(command: bytes):
    global comma
    comma = command
    

def fire():
    send_command(b'1')
    print('Ativado.')


def deactivate(app: IgnitorRFApp):
    send_command(b'0')
    app.cancel()
    print('Desativado.')


def count_down(com: serial.Serial, app: IgnitorRFApp):
    try:
        send_command(b'C')
        for cont in range(4):
            if app.event.is_set():
                deactivate(app)
                break
            if cont < 3:
                app.label_status.configure(text=f'Ativando em: {3 - cont}')
            else:
                fire()
                app.event.wait(3)
                deactivate(app)
                break
            app.event.wait(1)
    except serial.SerialException:
        app.label_status.configure(text='Falha na conexão.')


def esp_tare():
    send_command(b'E')
    print('Tare enviado.')

def esp_reboot(app: IgnitorRFApp):
    send_command(b'R')
    app.label_status.configure(text='Reiniciando ESP32...')
    print('Reiniciando ESP32...')

def save_serial_log(msg: str):
    try:
        filename = f'log_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.txt'
        with open(filename, 'w') as file:
            file.write(msg)
    except Exception as e:
        print('Falha ao salvar log.', e)


def check_usb_connection() -> list:
    if sys.platform.startswith('win'):
        return [port.device for port in serial.tools.list_ports.comports()]
    elif sys.platform.startswith(('linux', 'cygwin')):
        return [port.device for port in serial.tools.list_ports.comports() if '/dev/ttyUSB' in port.device]
    return []


def check_still_connect(com: serial.Serial) -> bool:
    try:
        com.isOpen()
        com.port in check_usb_connection()
        return True
    except serial.SerialException:
        print('Falha na conexão.')
        return False


if __name__ == '__main__':
    # if check_usb_connection():
    Ctk.set_appearance_mode('System')
    Ctk.set_default_color_theme('blue')
    app = IgnitorRFApp()
    app.mainloop()
    # else:
    #     print('Nenhuma porta disponível.')
    #     sys.exit(1)
