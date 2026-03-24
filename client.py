import socket
import pickle
import ssl

def display_menu(menu):
    print("Menu:")
    for item_id, item in menu.items():
        print(f"{item_id}: {item['name']} - ₹{item['price']}")

def place_order():
    order = {}
    while True:
        item_id = input("Enter item ID to order (0 to finish): ")
        if item_id == '0':
            break
        quantity = int(input("Enter quantity: "))
        order[int(item_id)] = quantity
    return order

def show_bill(total_price):
    print(f"Total Price: ₹{total_price}")

def main():
    host = "192.168.4.145"
    port = 8080

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    ssl_socket = ssl_context.wrap_socket(client_socket, server_hostname=host)

    try:
        ssl_socket.connect((host, port))
        print("Connected to server.")

        while True:
            print("\nOptions:")
            print("1. Show Menu")
            print("2. Order Food")
            print("5. Exit")

            option = input("Select an option: ")

            if option == '1':
                ssl_socket.send(pickle.dumps(option))
                menu = pickle.loads(ssl_socket.recv(1024))
                display_menu(menu)
            elif option == '2':
                ssl_socket.send(pickle.dumps(option))
                order = place_order()
                ssl_socket.send(pickle.dumps(order))
                total_price = pickle.loads(ssl_socket.recv(1024))
                show_bill(total_price)
            elif option == '5':
                ssl_socket.send(pickle.dumps(option))
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")

    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        ssl_socket.close()

if __name__ == "__main__":
    main()
