from module import *
from datetime import datetime
import time
import threading


def get_date_time() -> str:
    return datetime.now().strftime('%H:%M:%S.%f')[:-3] + ' -> '


def log_message(message: str):
    msg = get_date_time() + message
    print(msg)
    ui.textCursor.insertText(msg+'\n')


def save_log(msg: str):
    try:
        filename = f'/log_{datetime.now().strftime("%d-%m-%Y_%H-%M-%S")}.txt'
        with open(filename, 'w') as file:
            file.write(msg)
    except Exception as e:
        print('Falha ao salvar log.', e)


def thread_p2p():
    global comma
    comma = None
    while com.check_connection():
        ping = 0
        try:
            start = datetime.now()
            com.send_command(comma or b'A')
            response = com.read_response()
            handle_response(response)
            stop = datetime.now()
            ping = (stop - start).total_seconds() * 1000
        except Exception as e:
            log_message(f'Erro na conexão: {e}')

        ui.pingLabel.setText(f'{ping:.2f} ms')
        time.sleep(ping / 1000 if ping > 0 else 0.5)


def thread_countdown():
    global comma
    com.send_command(b'C')
    for cont in range(11):
        if com.check_connection():
            if cont < 10:
                ui.receivedLabel.setText(f'Ativando em {10 - cont}')
            else:
                set_queue_command(b'1')
                time.sleep(3)
                set_queue_command(b'0')
                countdown_reset()
                break
            time.sleep(1)
        else:
            log_message('Falha na conexão.')
            break


def start_countdown():
    ui.countdownButton.setText('Desativar')
    ui.countdownButton.clicked.connect(lambda: print('Desativar'))
    threading.Thread(target=thread_countdown, daemon=True).start()


def countdown_reset():
    ui.countdownButton.setText('Contagem Regressiva')
    ui.countdownButton.clicked.connect(lambda: start_countdown())


def handle_response(response: str):
    global comma
    log_message(response or 'Sem resposta.')
    options = {
        'Ativado.', 'Desativado.', 'Zerando célula.', 'Comando desconhecido.', 'Reiniciando.'
    }
    if response in options:
        comma = None
        ui.receivedLabel.setText(f'{response}')


def set_queue_command(command: bytes):
    global comma
    comma = command


def connect(port: str):
    global com
    try:
        com = apc220(port)
    except Exception as e:
        log_message(f'Falha ao conectar: {e}')
        ui.receivedLabel.setText('Falha ao conectar.')
        return
    ui.receivedLabel.setText('Conectado.')
    ui.statusLabel.setText('Conectado')
    setup_buttons_on_connect()
    threading.Thread(target=thread_p2p, daemon=True).start()


def reset_ui_on_disconnect():
    ui.receivedLabel.setText('Desconectado.')
    ui.statusLabel.setText('Desconectado')
    ui.logButton.setEnabled(False)
    ui.connectButton.setEnabled(True)
    ui.disconnectButton.setEnabled(False)
    ui.portsBox.setEnabled(True)
    ui.activateButton.setEnabled(False)
    ui.desactivateButton.setEnabled(False)
    ui.countdownButton.setEnabled(False)
    ui.tareButton.setEnabled(False)
    ui.rebootButton.setEnabled(False)
    ui.pingLabel.setText('0.00 ms')


def disconnect(com: apc220):
    com.close()
    reset_ui_on_disconnect()


def setup_buttons_on_connect():
    ui.logButton.setEnabled(True)
    ui.connectButton.setEnabled(False)
    ui.disconnectButton.setEnabled(True)
    ui.portsBox.setEnabled(False)
    ui.activateButton.setEnabled(True)
    ui.desactivateButton.setEnabled(True)
    ui.countdownButton.setEnabled(True)
    ui.tareButton.setEnabled(True)
    ui.rebootButton.setEnabled(True)


def setup_buttons_commands():
    ui.connectButton.clicked.connect(
        lambda: connect(ui.portsBox.currentText()))
    ui.disconnectButton.clicked.connect(lambda: disconnect(com))
    ui.activateButton.clicked.connect(lambda: set_queue_command(b'1'))
    ui.desactivateButton.clicked.connect(lambda: set_queue_command(b'0'))
    ui.countdownButton.clicked.connect(lambda: start_countdown())
    ui.tareButton.clicked.connect(lambda: set_queue_command(b'E'))
    ui.rebootButton.clicked.connect(lambda: set_queue_command(b'R'))
    ui.logButton.clicked.connect(lambda: save_log(ui.textEdit.toPlainText()))


if __name__ == "__main__":
    ports = list_ports()
    app = QApplication([])
    MainWindow = QMainWindow()
    ui = Ui_IgnitorRF(IgnitorRF=MainWindow, ports=ports)
    setup_buttons_commands()
    MainWindow.show()
    app.exec()
