import socket
import json
from datetime import datetime

# UDP_IP = ''
# UDP_PORT = 5000


def run_server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    sock.bind(server)
    try:
        while True:
            data, address = sock.recvfrom(1024)
            received_time = str(datetime.now())
            data_str = data.decode("utf-8")
            data_dict = {}
            for item in data_str.split("&"):
                key, value = item.split("=")
                data_dict[key] = value
            data_to_write = {received_time: data_dict}
            with open("files/storage/data.json", "a", encoding="utf-8") as f:
                json.dump(data_to_write, f)
                f.write("\n")
            sock.sendto(data, address)
            print(f'Send data: {data.decode()} to: {address}')
    except KeyboardInterrupt:
        print('Stop server')
    finally:
        sock.close()


# if __name__ == "__main__":
#     run_server()
