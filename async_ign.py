import asyncio
import os
import serial


async def send_and_receive():
    port = '/dev/ttyUSB0'  # Altere para a porta serial correta
    baudrate = 9600  # Altere para a taxa de baud correta

    try:
        ser = serial.Serial(port, baudrate)
    except serial.SerialException as e:
        print(f"Erro ao abrir a porta serial: {e}")
        return
    
    async def RW_serial():
        n = 0
        while True:
            n += 1
            ser.write(b'a')
            response = ser.readline().decode('utf-8').strip()
            # os.system('cls' if os.name == 'nt' else 'clear')
            print(f"Recebido: {response} - {n}")
            await asyncio.sleep(0.1)
            
    await asyncio.gather(RW_serial())