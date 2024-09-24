try:
    import subprocess
    import serial
    import serial.tools.list_ports
    import time
    import customtkinter
    import sys
    import asyncio
    import os
except:
    import sys
    import os
    os.system('pip install -r requirements.txt')
    import serial
    import serial.tools.list_ports
    import time
    import asyncio
    import customtkinter


def connect():
    try:
        global com
        com = serial.Serial(menu_port.get(), 9600, timeout=1)
        btn_conectar.destroy()
        global btn_desconectar
        btn_desconectar = customtkinter.CTkButton(
            master=app, text='Desconectar', command=disconnect)
        btn_desconectar.grid(row=0, column=0, padx=20, pady=10)
        btn_desconectar.configure(font=('Arial', 20))
        btn_desconectar.configure(height=80, width=120)
        label1.configure(text='Conectado ao módulo RF.')
    except:
        label1.configure(
            text='Não foi possível conectar, verifique a porta especificada.')
        pass
    else:
        # ping()
        recebido()


def disconnect():
    com.close()
    btn_desconectar.destroy()
    btn_conectar = customtkinter.CTkButton(
        master=app, text='Conectar', command=connect)
    btn_conectar.grid(row=0, column=0, padx=20, pady=10)
    btn_conectar.configure(font=('Arial', 20))
    btn_conectar.configure(height=80, width=120)
    label1.configure(text='Desconectado.')
    label2.configure(text='')


def ping():
    start = time.perf_counter()
    app.update()
    try:
        com.isOpen()
        com.reset_output_buffer()
        com.write('0'.encode())
        msg = str(com.read_until())
        msg = msg[2:-5]
        if msg != '1':
            raise
    except:
        label2.configure(text='Falha na conexão.')
        app.after(100, ping)
        pass
    else:
        now = time.perf_counter()
        pingN = (now-start)*1000
        label2.configure(text=f'Latência: {pingN:.0f}ms')
        app.after(100, ping)


def ativar():
    try:
        com.isOpen()
        btn_ativar.destroy()
        global state
        state = True
        global btn_cancelar
        btn_cancelar = customtkinter.CTkButton(
            master=app, text='Cancelar', command=cancelar)
        btn_cancelar.grid(row=0, column=2, padx=20, pady=10)
        btn_cancelar.configure(font=('Arial', 20))
        btn_cancelar.configure(height=80, width=120)
        cont = 0
        while cont < 11:
            if state:
                if cont < 10:
                    label1.configure(text='Ativando em: ' + str(10-cont))
                if cont == 10:
                    com.reset_output_buffer()
                    com.write('2'.encode())
                    msg = str(com.readline())
                    msg = msg[2:-5]
                    label1.configure(text=msg)
                    desativar()
                    break
            else:
                disconnect()
                connect()
                break
            cont += 1
            app.update()
            time.sleep(0.8)
    except:
        label1.configure(text='Falha na conexão.')
        app.update()
        pass


def desativar():
    t = 0
    while t < 5:
        t += 1
        app.update()
        time.sleep(1)
    com.reset_output_buffer()
    com.write('3'.encode())
    msg = str(com.readline())
    msg = msg[2:-5]
    label1.configure(text=msg)
    btn_cancelar.destroy()
    btn_ativar = customtkinter.CTkButton(
        master=app, text='Ativar', command=ativar)
    btn_ativar.grid(row=0, column=2, padx=20, pady=10)
    btn_ativar.configure(font=('Arial', 20))
    btn_ativar.configure(height=80, width=120)


def recebido():
    try:
        def check_usb_connection():
            ports = [port.device for port in list(
                serial.tools.list_ports.comports())]
            if menu_port.get() in ports:
                None
            else:
                label1.configure(text='Desconectado do módulo RF.')
                label2.configure(text='Desconectado do Ignitor')
                raise Exception('Desconectado do módulo RF.')

        check_usb_connection()
        com.isOpen()
        com.reset_output_buffer()
        com.write('a'.encode())
        msg = str(com.readline())
        msg = msg[2:-5]
        label3.configure(text=msg)

        if msg != '':
            label2.configure(text='Conectado ao Ignitor')
        else:
            label2.configure(text='Desconectado do Ignitor')

        app.after(100, recebido)
    except:
        label3.configure(text='Falha na conexão.')
        disconnect()
        pass


def cancelar():
    label1.configure(text='Ativação cancelada.')
    com.write('3'.encode())
    btn_cancelar.destroy()
    btn_ativar = customtkinter.CTkButton(
        master=app, text='Ativar', command=ativar)
    btn_ativar.grid(row=0, column=2, padx=20, pady=10)
    btn_ativar.configure(font=('Arial', 20))
    btn_ativar.configure(height=80, width=120)
    app.update()
    global state
    state = False


def update_ports():
    if sys.platform.startswith('win'):
        menu_port.configure(values=get_com_ports())
        app.after(1000, update_ports)
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        menu_port.configure(values=get_usb_ports())
        app.after(1000, update_ports)
    else:
        raise EnvironmentError('Unsupported platform')


def get_com_ports():
    return [port.device for port in list(serial.tools.list_ports.comports())]


def get_usb_ports():
    ports = [port.device for port in list(serial.tools.list_ports.comports())]
    return [port for port in ports if '/dev/ttyUSB' in port]


if __name__ == '__main__':
    customtkinter.set_appearance_mode('System')
    customtkinter.set_default_color_theme('blue')
    app = customtkinter.CTk()
    app.title('Ignitor')
    app.geometry('1280x720')

    for i in range(3):
        app.grid_columnconfigure(i, weight=1)
    for i in range(4):
        app.grid_rowconfigure(i, weight=1)

    if sys.platform.startswith('win'):
        menu_port = customtkinter.CTkOptionMenu(
            app, values=[port.device for port in list(serial.tools.list_ports.comports())])
        menu_port.grid(row=3, column=0, padx=20, pady=10)
        menu_port.set('Portas')
        update_ports()
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = [port.device for port in list(
            serial.tools.list_ports.comports())]
        portsUSB = []
        for port in ports:
            if '/dev/ttyUSB' in port:
                portsUSB.append(port)
        menu_port = customtkinter.CTkOptionMenu(app, values=portsUSB)
        menu_port.grid(row=3, column=0, padx=20, pady=10)
        menu_port.set('Portas')
        update_ports()
    else:
        raise EnvironmentError('Unsupported platform')

    btn_conectar = customtkinter.CTkButton(
        master=app, text='Conectar', command=connect)
    btn_conectar.grid(row=0, column=0, padx=20, pady=10)
    btn_conectar.configure(height=80, width=120)
    btn_conectar.configure(font=('Arial', 20))
    btn_ativar = customtkinter.CTkButton(
        master=app, text='Iniciar contagem', command=ativar)
    btn_ativar.grid(row=0, column=2, padx=20, pady=10)
    btn_ativar.configure(font=('Arial', 20))
    btn_ativar.configure(height=80, width=120)

    label1 = customtkinter.CTkLabel(master=app, text='Aguardando conexão.')
    label1.grid(row=1, column=1, padx=20, pady=10)
    label1.configure(font=('Arial', 30))
    label2 = customtkinter.CTkLabel(master=app, text='')
    label2.grid(row=3, column=2, padx=20, pady=10)
    label2.configure(font=('Arial', 20))
    label3 = customtkinter.CTkLabel(master=app, text='')
    label3.grid(row=2, column=1, padx=20, pady=10)
    label3.configure(font=('Arial', 30))

    app.mainloop()
    com.close()
