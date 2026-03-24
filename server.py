import socket
import pickle
import ssl
import tabulate

menu = {
    1: {"name": "South Indian Meal", "price": 60},
    2: {"name": "North Indian Meal", "price": 70},
    3: {"name": "Burger and Fries Combo", "price": 100},
    4: {"name": "Pizza and Soda Combo", "price": 120},
    5: {"name": "Ice Cream", "price": 50},
}

def send_menu(conn):
    conn.send(pickle.dumps(menu))

def handle_order(conn, addr):
    print(f"Connected to {addr}")
    try:
        order = pickle.loads(conn.recv(1024))
        total_price = 0
        ordered_items = []

        for item_id, quantity in order.items():
            if item_id in menu:
                item = menu[item_id]
                total_price += item["price"] * quantity
                ordered_items.append([item["name"], quantity, item["price"] * quantity])

        gst_amount = total_price * 0.05
        total_price += gst_amount

        conn.send(pickle.dumps(total_price))

        headers = ["Item Name", "Quantity", "Total Price"]
        print("\nOrder Details:")
        print(tabulate(ordered_items, headers=headers, tablefmt="grid"))

        print(f"\nTotal Price (incl. 5% GST): ₹{total_price}")
        print(f"GST (5%): ₹{gst_amount}")
    except Exception as e:
        print(f"Error handling order: {e}")

def main():
    host = "0.0.0.0"
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Restaurant Server is running...")
    print("Waiting for connections...")

    while True:
        conn, addr = server_socket.accept()
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")

        try:
            ssl_socket = ssl_context.wrap_socket(conn, server_side=True)
            print("SSL connection established!")

            while True:
                option = ssl_socket.recv(1024)
                if not option:
                    break
                option = pickle.loads(option)

                if option == '1':
                    send_menu(ssl_socket)
                elif option == '2':
                    handle_order(ssl_socket, addr)
                elif option == '5':
                    print("Client disconnected.")
                    break
        except ssl.SSLError as e:
            print(f"SSL Error: {e}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            ssl_socket.close()

if __name__ == "__main__":
    main()
