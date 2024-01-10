import heapq
import tkinter as tk
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox

class Customer:
    def __init__(self, customer_id, name, checkin_date, checkout_date):
        self.customer_id = customer_id
        self.name = name
        self.checkin_date = checkin_date
        self.checkout_date = checkout_date

class Room:
    def __init__(self, room_number, capacity):
        self.room_number = room_number
        self.capacity = capacity
        self.is_reserved = False

class HotelFloor:
    def __init__(self, floor_number, rooms):
        self.floor_number = floor_number
        self.rooms = rooms

class Hotel:
    def __init__(self):
        self.floors = []
        self.customers = []
        self.reservation_stack = []
        self.room_priority_queue = []
    def add_floor(self, floor):
        self.floors.append(floor)

    def add_customer(self, customer):
        self.customers.append(customer)

    def reserve_room(self, customer, room):
        customer_room_priority = (customer.checkin_date, room.room_number)
        heapq.heappush(self.room_priority_queue, (customer_room_priority, customer, room))
        self.reservation_stack.append((customer, room))

    def allocate_rooms(self):
        while self.room_priority_queue:
            _, customer, room = heapq.heappop(self.room_priority_queue)
            room.is_reserved = True
            print(f"Room {room.room_number} allocated to {customer.name}")

    #def display_reservations(self):
     #   for i in range(0,len(names)):
    #            print(str(names[i]) + " in " + str(reoom[i]))#

class Token:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

class TokenManager:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if not self.root:
            self.root = Token(value)
        else:
            self._insert_recursive(value, self.root)

    def _insert_recursive(self, value, current_node):
        if value < current_node.value:
            if current_node.left:
                self._insert_recursive(value, current_node.left)
            else:
                current_node.left = Token(value)
        elif value > current_node.value:
            if current_node.right:
                self._insert_recursive(value, current_node.right)
            else:
                current_node.right = Token(value)
        else:
            pass

    def in_order_traversal(self, node, result):
        if node:
            self.in_order_traversal(node.left, result)
            result.append(node.value)
            self.in_order_traversal(node.right, result)

    def get_sorted_tokens(self):
        result = []
        self.in_order_traversal(self.root, result)
        return result

    def find_min_value_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def delete(self, value):
        self.root = self._delete_recursive(self.root, value)

    def _delete_recursive(self, root, value):
        if not root:
            return root

        if value < root.value:
            root.left = self._delete_recursive(root.left, value)
        elif value > root.value:
            root.right = self._delete_recursive(root.right, value)
        else:
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            root.value = self.find_min_value_node(root.right).value
            root.right = self._delete_recursive(root.right, root.value)

        return root


class DishStack:
    def __init__(self):
        self.stack = []
        self.token_manager = TokenManager()

    def push(self, dish_name):
        token = len(self.stack) + 1
        self.token_manager.insert(token)
        self.stack.append((token, dish_name))
        messagebox.showinfo("Restaurant", f'Dish "{dish_name}" stored with token {token}')

    def pop(self, token):
        self.token_manager.delete(token)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == token:
                deleted_dish = self.stack.pop(i)[1]
                messagebox.showinfo("Restaurant", f'Dish "{deleted_dish}" deleted successfully.')
                return
        messagebox.showinfo("Restaurant", f'Dish with token {token} not found.')

    def display_stack(self):
        result = "\nCurrent Stack:"
        for token, dish_name in reversed(self.stack):
            result += f'\nToken {token}: {dish_name}'
        messagebox.showinfo("Restaurant", result)

class GUI:
    def __init__(self):
        self.hotel = Hotel()
        self.dish_stack = DishStack()
        self.names=[]
        self.reoom=[]
        self.root = tk.Tk()
        self.root.title("Hotel & Restaurant Management")

        self.create_tabs()
        
















        
    def create_display_frame(self):
        display_frame = tk.Frame(self.root)
        display_frame.pack(side=tk.BOTTOM, padx=10, pady=10)

        # Labels for displaying tokens, dishes, and reserved rooms
        tk.Label(display_frame, text="Tokens:").grid(row=0, column=0, pady=5)
        self.tokens_label = tk.Label(display_frame, text="")
        self.tokens_label.grid(row=1, column=0, pady=5)

        tk.Label(display_frame, text="Dishes:").grid(row=0, column=1, pady=5)
        self.dishes_label = tk.Label(display_frame, text="")
        self.dishes_label.grid(row=1, column=1, pady=5)

        tk.Label(display_frame, text="Reserved Rooms:").grid(row=0, column=2, pady=5)
        self.rooms_label = tk.Label(display_frame, text="")
        self.rooms_label.grid(row=1, column=2, pady=5)    

    def create_tabs(self):
        notebook = ttk.Notebook(self.root)

        notebook.pack(fill=tk.BOTH, expand=True)

        hotel_tab = tk.Frame(notebook)
        restaurant_tab = tk.Frame(notebook)

        notebook.add(hotel_tab, text='Hotel Management')
        notebook.add(restaurant_tab, text='Restaurant Management')

        self.create_hotel_frame(hotel_tab)
        self.create_restaurant_frame(restaurant_tab)
        self.create_display_frame(hotel_tab)

    def update_display(self):
        # Update tokens label
        tokens = self.dish_stack.token_manager.get_sorted_tokens()
        tokens_str = ", ".join(map(str, tokens))
        self.tokens_label.config(text=f"Tokens: {tokens_str}")

        # Update dishes label
        dishes = [f"{token}: {dish}" for token, dish in reversed(self.dish_stack.stack)]
        dishes_str = "\n".join(dishes)
        self.dishes_label.config(text=f"Dishes: {dishes_str}")

        # Update reserved rooms label
        reservations = [f"{customer.name}: Room {room.room_number}" for customer, room in self.hotel.reservation_stack]
        reservations_str = "\n".join(reservations)
        self.rooms_label.config(text=f"Reserved Rooms: {reservations_str}")     

    def create_hotel_frame(self, hotel_tab):
        tk.Label(hotel_tab, text="Hotel Management", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Button(hotel_tab, text="Add Floor", command=self.add_floor).grid(row=1, column=0, pady=5)
        tk.Button(hotel_tab, text="Add Customer", command=self.add_customer).grid(row=1, column=0, pady=5)
        tk.Button(hotel_tab, text="Reserve Room", command=self.reserve_room).grid(row=2, column=0, pady=5)
        #tk.Button(hotel_tab, text="Allocate Rooms", command=self.allocate_rooms).grid(row=3, column=0, pady=5)
        tk.Button(hotel_tab, text="Display Reservations", command=self.display_reservations).grid(row=4, column=0, pady=5)

        # Labels to display entered values
        self.floor_label = tk.Label(hotel_tab, text="")
        self.floor_label.grid(row=4, column=0, pady=5)

        self.customer_label = tk.Label(hotel_tab, text="")
        self.customer_label.grid(row=5, column=0, pady=5)

        self.reservation_label = tk.Label(hotel_tab, text="")
        self.reservation_label.grid(row=6, column=0, pady=5)
        
        
        self.display_label = tk.Label(hotel_tab, text="")
        self.display_label.grid(row=9, column=0, pady=5)

        

        self.display1_label = tk.Label(hotel_tab, text="")
        self.display1_label.grid(row=10, column=0, pady=5)

    def create_restaurant_frame(self, restaurant_tab):
        tk.Label(restaurant_tab, text="Restaurant", font=("Helvetica", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        tk.Button(restaurant_tab, text="Store Dish", command=self.store_dish).grid(row=1, column=1, pady=5)
        tk.Button(restaurant_tab, text="Delete Dish by Token", command=self.delete_dish).grid(row=2, column=1, pady=5)
        tk.Button(restaurant_tab, text="View Stored Dishes", command=self.view_dishes).grid(row=3, column=1, columnspan=1, pady=5)

        # Labels to display entered values
        self.dish_label = tk.Label(restaurant_tab, text="")
        self.dish_label.grid(row=3, column=0, pady=5)

    def create_display_frame(self, hotel_tab):  # noqa: F811
        display_frame = tk.Frame(hotel_tab)
        display_frame.grid(row=7, column=1, columnspan=2, pady=10)

        # Labels for displaying tokens, dishes, and reserved rooms
        tk.Label(display_frame, text="Tokens:").grid(row=0, column=0, pady=5)
        self.tokens_label = tk.Label(display_frame, text="")
        self.tokens_label.grid(row=1, column=1, pady=5)

        tk.Label(display_frame, text="Dishes:").grid(row=1, column=0, pady=5)
        self.dishes_label = tk.Label(display_frame, text="")
        self.dishes_label.grid(row=1, column=1, pady=5)

        #tk.Label(display_frame, text="Reserved Rooms:").grid(row=2, column = 0, pady=5)
        #self.rooms_label = tk.Label(display_frame, text="")
        #self.rooms_label.grid(row=1, column=2, pady=5)

    
   

    def add_floor(self):
        floor_number = tk.simpledialog.askinteger("Add Floor", "Enter Floor Number:")
        if floor_number is not None:
            room_numbers = tk.simpledialog.askstring("Add Floor", "Enter Room Numbers (comma-separated):")
            if room_numbers is not None:
                room_numbers = [int(num.strip()) for num in room_numbers.split(",")]
                rooms = [Room(room_num, 2) for room_num in room_numbers]
                floor = HotelFloor(floor_number, rooms)
                self.hotel.add_floor(floor)
                self.floor_label.config(text=f"Floor Added: {floor_number}")

    def add_customer(self):
        customer_id = tk.simpledialog.askinteger("Add Customer", "Enter Customer ID:")
        if customer_id is not None:
            name = tk.simpledialog.askstring("Add Customer", "Enter Customer Name:")
            if name is not None:
                checkin_date = tk.simpledialog.askstring("Add Customer", "Enter Check-in Date (YYYY-MM-DD):")
                if checkin_date is not None:
                    checkout_date = tk.simpledialog.askstring("Add Customer", "Enter Check-out Date (YYYY-MM-DD):")
                    if checkout_date is not None:
                        customer = Customer(customer_id, name, checkin_date, checkout_date)
                        self.hotel.add_customer(customer)
                        self.customer_label.config(text=f"Customer Added: {name}")

    def reserve_room(self):
        customer_nam = tk.simpledialog.askstring("Reserve Room", "Enter Customer Name:")
        
        if customer_nam is not None:
            floor_number = tk.simpledialog.askinteger("Reserve Room", "Enter Floor Number:")
            if floor_number is not None:
                room_number = tk.simpledialog.askinteger("Reserve Room", "Enter Room Number:")
                self.names.append(customer_nam)
                self.reoom.append(room_number)
                
                if room_number is not None:
                    
                    #room = next((r for floor in self.hotel.floors if floor.floor_number == floor_number for r in floor.rooms if r.room_number == room_number), None)
                    #if room:
                     #   self.hotel.reserve_room( room)
                        self.reservation_label.config(text=f"Room Reserved: {room_number} for {customer_nam} ")
                        self.update_display()
                        
                        

    def store_dish(self):
        dish_name = tk.simpledialog.askstring("Store Dish", "Enter Dish Name:")
        if dish_name is not None:
            self.dish_stack.push(dish_name)
            self.dish_label.config(text=f"Dish Stored: {dish_name}")
            self.update_display()
  
    def allocate_rooms(self):
        self.hotel.allocate_rooms()
        messagebox.showinfo("Hotel", "Rooms allocated successfully.")

    #def display_reservations(self):
    #    self.hotel.display_reservations()
    def display_reservations(self):
        for i in range(0,len(self.names)-1):
                print(str(self.names[i]) + " in " + str(self.reoom[i]))
                self.display_label.config(text=f"The reservations are: {self.names[i]} in {self.reoom[i]}")
        for i in range(0,len(self.names)) :
            self.display1_label.config(text=f"                      {self.names[i]} in {self.reoom[i]}")
                
    def cus(self,customer_nam):
        self.hotel.customers.append(customer_nam)
    

    def delete_dish(self):
        token = tk.simpledialog.askinteger("Delete Dish", "Enter Token:")
        if token is not None:
            self.dish_stack.pop(token)

    def view_dishes(self):
        self.dish_stack.display_stack()
        self.update_display()

    def run(self):
        self.root.mainloop()
        self.update_display()
        

if __name__ == "__main__":
    gui = GUI()
    gui.run()