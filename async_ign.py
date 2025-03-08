import os
import sys
import threading
import time
import serial
import serial.tools.list_ports
import customtkinter as Ctk
from datetime import datetime

# Main application class for the Ignitor RF
class IgnitorRFApp(Ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title('Ignitor RF')
        self.geometry('1280x720')
        self.configure_grid()
        self.update_ports()
        self.configure_buttons()
        self.configure_labels()
        self.event = threading.Event()

    # Configure the grid layout for the application
    def configure_grid(self):
        for i in range(3):
            self.grid_columnconfigure(i, weight=1)
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)

    # Configure the buttons in the application
    def configure_buttons(self):
        self.btn_conectar = Ctk.CTkButton(
            master=self, text='Conectar', command=self.connect)
        self.btn_conectar.grid(row=0, column=0, padx=20, pady=10)
        self.btn_conectar.configure(height=80, width=120, font=('Arial', 20))

        self.btn_ativar = Ctk.CTkButton(
            master=self, text='Iniciar contagem', command=self.start_countdown)
        self.btn_ativar.grid(row=0, column=2, padx=20, pady=10)
        self.btn_ativar.configure(height=80, width=120, font=('Arial', 20))

        self.btn_fechar = Ctk.CTkButton(
            master=self, text='Fechar', command=self.quit)
        self.btn_fechar.grid(row=3, column=2, padx=20, pady=10)

        self.btn_save_log = Ctk.CTkButton(
            master=self, text='Salvar Log', command=self.save_log)
        self.btn_save_log.grid(row=3, column=1, padx=20, pady=10)

        # Button to stop logging, initially hidden
        self.btn_stop_log = Ctk.CTkButton(
            master=self, text='Parar Log', command=self.stop_log)
        self.btn_stop_log.grid(row=2, column=0, padx=20, pady=10)
        self.btn_stop_log.grid_remove()

        # Button to send tare command, initially hidden
        self.btn_tare = Ctk.CTkButton(
            master=self, text='Tare', command=self.send_tare)
        self.btn_tare.grid(row=2, column=2, padx=20, pady=10)
        self.btn_tare.grid_remove()

    # Configure the labels in the application
    def configure_labels(self):
        self.label_status = Ctk.CTkLabel(
            master=self, text='Aguardando conexão.')
        self.label_status.grid(row=1, column=1, padx=20, pady=10)
        self.label_status.configure(font=('Arial', 30))

        self.label_message = Ctk.CTkTextbox(
            master=self,  width=620, corner_radius=0)
        self.label_message.grid(row=2, column=1, padx=20, pady=10)
        self.label_message.configure(font=('Courier', 20))

    # Update the available ports in the dropdown menu
    def update_ports(self):
        ports = check_usb_connection()
        self.menu_port = Ctk.CTkOptionMenu(self, values=ports)
        self.menu_port.grid(row=3, column=0, padx=20, pady=10)
        self.menu_port.set('/dev/ttyUSB0')

    # Connect to the selected port
    def connect(self):
        port = self.menu_port.get()
        if port != 'Portas':
            self.com = connect(port, self)
            self.label_status.configure(text='Conectado.')
            self.btn_conectar.configure(
                text='Desconectar', command=self.disconnect)
            self.btn_tare.grid()  # Show the tare button
        else:
            self.label_status.configure(text='Selecione uma porta.')

    # Disconnect from the current port
    def disconnect(self):
        if hasattr(self, 'com'):
            disconnect(self.com, self)
            self.btn_conectar.configure(text='Conectar', command=self.connect)
            self.btn_tare.grid_remove()  # Hide the tare button
        else:
            self.label_status.configure(text='Conecte-se primeiro.')

    # Quit the application
    def quit(self):
        if hasattr(self, 'com'):
            disconnect(self.com, self)
        self.destroy()

    # Start the countdown process
    def start_countdown(self):
        self.event.clear()
        if hasattr(self, 'com'):
            self.countdown = threading.Thread(
                target=count_down, args=(self.com, self)).start()
            self.btn_ativar.configure(text='Cancelar', command=self.cancel)
            self.btn_stop_log.grid()  
        else:
            self.label_status.configure(text='Conecte-se primeiro.')

    # Cancel the countdown process
    def cancel(self):
        self.event.set()
        if hasattr(self, 'com'):
            self.btn_ativar.configure(
                text='Iniciar contagem', command=self.start_countdown)
        else:
            self.label_status.configure(text='Conecte-se primeiro')

    # Save the log from label_message
    def save_log(self):
        log_text = self.label_message.get("1.0", "end-1c")
        save_serial_log(log_text)

    # Stop logging
    def stop_log(self):
        if hasattr(self, 'com'):
            esp_stop_log(self.com, self)
            self.btn_stop_log.grid_remove()  

    # Send tare command
    def send_tare(self):
        if hasattr(self, 'com'):
            esp_tare(self.com, self)

# Get the current date and time as a formatted string
def get_date_time() -> str:
    now = datetime.now()
    return now.strftime('%H:%M:%S.%f')[:-3] + ' -> '

# Connect to the specified serial port
def connect(port: str, app: IgnitorRFApp) -> serial.Serial:
    com = serial.Serial(port, 9600, timeout=1)
    threading.Thread(target=recebido, args=(com, app)).start()
    return com

# Disconnect from the specified serial port
def disconnect(com: serial.Serial, app: IgnitorRFApp):
    com.close()
    app.label_status.configure(text='Desconectado.')

# Continuously read data from the serial port
def recebido(com: serial.Serial, app: IgnitorRFApp):
    while check_still_connect(com):
        try:
            com.isOpen()
            com.reset_output_buffer()
            com.write(b'A')
            msg = com.readline().decode("utf-8").strip()
            if msg:
                app.label_message.insert(
                    index="0.0", text=get_date_time() + msg + '\n')
            else:
                app.label_message.insert(
                    index="0.0", text='Desconectado do Ignitor.\n')
        except serial.SerialException:
            app.label_status.configure(text='Falha na conexão.')
            disconnect(com, app)
            break
        time.sleep(0.5)

# Send a command to the serial port
def send_command(com: serial.Serial, command: bytes, app: IgnitorRFApp):
    try:
        com.isOpen()
        com.reset_output_buffer()
        com.write(command)
        com.reset_input_buffer()
        msg = com.readline().decode("utf-8").strip()
        app.label_status.configure(text=msg)
        app.label_message.insert(
            index="0.0", text=get_date_time() + msg + '\n')
    except serial.SerialException:
        app.label_status.configure(text='Falha na conexão.')

# Send the fire command to the serial port
def fire(com: serial.Serial, app: IgnitorRFApp):
    send_command(com, b'1', app)

# Send the deactivate command to the serial port
def deactivate(com: serial.Serial, app: IgnitorRFApp):
    send_command(com, b'0', app)
    app.cancel()

# Countdown process before firing
def count_down(com: serial.Serial, app: IgnitorRFApp):
    try:
        com.isOpen()
        # esp_save_log(com, app)
        for cont in range(11):
            if cont < 10:
                app.label_status.configure(text=f'Ativando em: {10 - cont}')
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
        app.label_status.configure(text='Falha na conexão.')
        esp_stop_log(com, app)

# Send the save log command to the serial port
def esp_save_log(com: serial.Serial, app: IgnitorRFApp):
    send_command(com, b'C', app)

# Send the stop log command to the serial port
def esp_stop_log(com: serial.Serial, app: IgnitorRFApp):
    send_command(com, b'D', app)

# Send the tare command to the serial port
def esp_tare(com: serial.Serial, app: IgnitorRFApp):
    send_command(com, b'E', app)

# Save the serial log to a file
def save_serial_log(msg: str):
    try:
        dia = datetime.now().strftime('%d-%m-%Y')
        hora = datetime.now().strftime('%H-%M-%S')
        filename = f'log_{dia}_{hora}.txt'
        mode = 'a' if os.path.exists(filename) else 'w'
        with open(filename, mode) as file:
            file.write(f'{msg}')
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
    # if check_usb_connection():
    Ctk.set_appearance_mode('System')
    Ctk.set_default_color_theme('blue')
    app = IgnitorRFApp()
    app.mainloop()
    # else:
    #     print('Nenhuma porta disponível.')
    #     sys.exit(1)