import sys
import serial.tools.list_ports

def get_uart_ports():
    ports = serial.tools.list_ports.comports()
    uart_ports = []
    sys.stdout.write('[')
    for port, desc, hwid in sorted(ports):
        if 'Silicon Labs CP210x USB to UART Bridge' not in desc:
            continue
        sys.stdout.write(f'("{port}", "{desc}", "{hwid}"),') 
        uart_ports.append(port)
    sys.stdout.write(']')
    return uart_ports

if __name__ == '__main__':
    get_uart_ports()