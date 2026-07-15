import socket
import time
import threading

def parse_resp(data: bytes):
    if not data:
        return None, 0
    
    marker = chr(data[0])
    print(f"Raw data: {data}")
    print(f"Marker: {marker}")
    
    if marker == "$":
        end = data.find(b"\r\n")
        length = int(data[1:end])
        start = end + 2
        value = data[start:start + length].decode()
        consumed = start + length + 2
        return value, consumed
    
    if marker == "*":
        end = data.find(b"\r\n")
        count = int(data[1:end])
        items = []
        consumed = end + 2
        for _ in range(count):
            item, n = parse_resp(data[consumed:])
            items.append(item)
            consumed += n
        return items, consumed
    return None, 0



def serialize_resp(value) -> bytes:
    if value is None:
        return b"$-1\r\n"
    if isinstance(value, int):
        return f":{value}\r\n".encode()
    if isinstance(value, str):
        encoded = value.encode()
        return f"${len(encoded)}\r\n".encode() + encoded + b"\r\n"
    if isinstance(value, Exception):
        return f"-ERR {value}\r\n".encode()
    


store={}
expirations={}

def cmd_ping():
    return "PONG"

def cmd_set(store, key, value):
    store[key] = value
    return "OK"

def cmd_get(store, key):
    if key in store:
        return store[key]
    return None

def cmd_del(store, key):
    if key in store:
        del store[key]
        return 1
    return 0

def cmd_exists(store, key):
    if key in store:
        return 1
    return 0

def cmd_incr(store, key):
    old=store.get(key,0)
    old=int(old)+1
    store[key]=str(old)
    return old

def cmd_expire(store, expirations, key, seconds):
    if key in store:
        expirations[key]=time.time()+seconds
        return 1
    return 0

def cmd_ttl(store, expirations, key):
    if key not in store:
        return -2
    if key not in expirations:
        return -1
    return expirations[key]-time.time()

def maybe_expire(store, expirations, key):
    if key in expirations:
        if time.time()>=expirations[key]:
            del store[key]
            del expirations[key]

COMMANDS = {
    "PING": lambda args: cmd_ping(),
    "SET": lambda args: cmd_set(store, args[0], args[1]),
    "GET": lambda args: cmd_get(store, args[0]),
    "DEL": lambda args: cmd_del(store, args[0]),
    "EXISTS": lambda args: cmd_exists(store, args[0]),
    "INCR": lambda args: cmd_incr(store, args[0]),
    "EXPIRE": lambda args: cmd_expire(store, expirations, args[0], int(args[1])),
    "TTL": lambda args: cmd_ttl(store, expirations, args[0]),
}
def dispatch(command_array):
    name = command_array[0].upper()
    args = command_array[1:]
    handler = COMMANDS.get(name)
    if handler is None:
        return f"Unknown command: {name}"
    return handler(args)

def handle_client(conn):
    data = conn.recv(4096)
    command, _ = parse_resp(data)
    print(f"Command received: {command}")
    result = dispatch(command)
    conn.sendall(serialize_resp(result))
    conn.close()


def run_server(host="127.0.0.1", port=6379):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((host, port))
    server.listen()
    print(f"Server listening on {host}:{port}")
    while True:
        conn, addr = server.accept()
        print(f"Connection from {addr}")
        thread = threading.Thread(target=handle_client, args=(conn,), daemon=True)
        thread.start()
run_server()