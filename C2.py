import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import customtkinter
from tkinter import simpledialog

class Device:
    all_devices = []

    def __init__(self, name, device_type):
        print('hello')
        self.name = name
        self.device_type = device_type
class Connection:
    adjacency_list = {}
    objects = []
    def insert_vertex(self, my_obj):
        Connection.adjacency_list[my_obj.name] = []
        Connection.objects.append(my_obj)
    def add_edge(self, from_, to):
        if Connection.adjacency_list.get(from_) is None or Connection.adjacency_list.get(to) is None:
            print("Edge can't be added between non-existent nodes")
            return
        if to in Connection.adjacency_list[from_]:
            print("Already Connected")
            return
        Connection.adjacency_list[from_].append(to)
        Connection.adjacency_list[to].append(from_)
    def show_graph(self):
        print(Connection.adjacency_list)
d=['PC', 'DNS', 'Switch', 'HUB', 'Email Server', 'HTTP Server']
c= ['red', 'green', 'blue', 'yellow', 'orange', 'purple']
# s=['*','s', '^', 'v','d', '8']
s=['s','o','^','>','v','<','d','p','h','8']
counter = {device_type: 0 for device_type in ['PC', 'DNS', 'Switch', 'HUB', 'Email Server', 'HTTP Server']}
def add_device(device_type):
    global cn
    global G
    global counter
    counter[device_type] += 1
    color,shape=c[d.index(device_type)],s[d.index(device_type)]
    device_name = f'{device_type}{counter[device_type]}'
    if device_name not in Device.all_devices:
        G.add_node(device_name, device_type=device_type, node_color=color)
        ob = Device(device_name, device_type)
        print(f"{device_name} has been added")
        Device.all_devices.append(device_name)
        cn.insert_vertex(ob)
    refresh_graph()

def refresh_graph():
    global G
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    fig, ax = plt.subplots(facecolor='white')
    ax.set_axis_off()
    nx.draw_networkx_nodes(G, pos, ax=ax)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=[G.nodes[node]['node_color'] for node in G.nodes])
    #
    nx.draw_networkx_edges(G, pos, ax=ax)
    nx.draw_networkx_labels(G, pos, font_weight='bold',font_size= 20, ax=ax)
    canvas = FigureCanvasTkAgg(fig, master=root_tk)
    canvas.draw()
    width=0.8
    height=1
    canvas.get_tk_widget().place(relx=0.5, rely=0, anchor=tk.N,relheight=height,relwidth=width)

connection_of_nodes=[None, None]
def combobox_1_callback(choice):
    global connection_of_nodes
    print("combobox dropdown clicked:", choice)
    connection_of_nodes[0]=choice
def combobox_2_callback(choice):
    global connection_of_nodes
    print("combobox2 dropdown clicked", choice)
    connection_of_nodes[1]=choice
def connect_now():
    global connection_of_nodes, G
    print(f"Connection will be built from {connection_of_nodes[0]} to {connection_of_nodes[1]}")
    G.add_edge(connection_of_nodes[0],connection_of_nodes[1])
    refresh_graph()
root_tk = tk.Tk()
root_tk.geometry("800x600")
root_tk.title("CustomTkinter Test")
cn = Connection()
G = nx.Graph()

# Create buttons for adding devices
add_pc_button = customtkinter.CTkButton(master=root_tk, text="Add PC", corner_radius=10, command=lambda: add_device('PC'))
add_pc_button.place(relx=0.05, rely=0.2, anchor=tk.CENTER)

add_dns_button = customtkinter.CTkButton(master=root_tk, text="Add DNS", corner_radius=10, command=lambda: add_device('DNS'))
add_dns_button.place(relx=0.05, rely=0.3, anchor=tk.CENTER)

add_email_button = customtkinter.CTkButton(master=root_tk, text="Add Email Server", corner_radius=10, command=lambda: add_device('Email Server'))
add_email_button.place(relx=0.05, rely=0.4, anchor=tk.CENTER)

add_switch_button = customtkinter.CTkButton(master=root_tk, text="Add Switch", corner_radius=10, command=lambda: add_device('Switch'))
add_switch_button.place(relx=0.05, rely=0.5, anchor=tk.CENTER)

add_hub_button = customtkinter.CTkButton(master=root_tk, text="Add HUB", corner_radius=10, command=lambda: add_device('HUB'))
add_hub_button.place(relx=0.05, rely=0.6, anchor=tk.CENTER)

add_http_button = customtkinter.CTkButton(master=root_tk, text="Add HTTP server", corner_radius=10, command=lambda: add_device('HTTP Server'))
add_http_button.place(relx=0.05, rely=0.7, anchor=tk.CENTER)

# Create a button to show the graph
graph_button = customtkinter.CTkButton(master=root_tk, text="Show Graph", corner_radius=10, command=lambda: refresh_graph())
graph_button.place(relx=0.05, rely=0.95, anchor=tk.CENTER)
connect_button = customtkinter.CTkButton(master=root_tk, text="Start Connection", corner_radius=10, command=lambda: combo_boxes())
connect_button.place(relx=0.95, rely=0.1, anchor=tk.CENTER)
# Create combo boxes for "From" and "To" devices
def combo_boxes():
    from_combobox_var = tk.StringVar()
    to_combobox_var = tk.StringVar()
    from_combobox = customtkinter.CTkComboBox(master=root_tk,values=Device.all_devices,command=lambda x:combobox_1_callback(x),variable=from_combobox_var)
    from_combobox.place(relx=0.95, rely=0.2, anchor=tk.CENTER)
    to_combobox = customtkinter.CTkComboBox(master=root_tk,values=Device.all_devices,command=lambda x:combobox_2_callback(x),variable=to_combobox_var)
    to_combobox.place(relx=0.95, rely=0.3, anchor=tk.CENTER)
    connection_button = customtkinter.CTkButton(master=root_tk, text="Connect", corner_radius=10,command=lambda: connect_now())
    connection_button.place(relx=0.95, rely=0.4, anchor=tk.CENTER)

# combobox = customtkinter.CTkComboBox(master=root_tk,values=Device.all_devices,command=combobox_callback,variable=combobox_var)
# def shhh():
#     import networkx as nx
#     import matplotlib.pyplot as plt2
#
#     # Create a sample graph
#     G1 = nx.Graph()
#     G1.add_edges_from([(1, 2), (2, 3), (3, 1)])
#
#     # Define node colors as a dictionary
#     node_colors = {1: 'red', 2: 'green', 3: 'blue'}
#
#     # Draw the graph with custom node colors using draw_networkx_nodes
#     pos = nx.spring_layout(G1)
#     nx.draw_networkx_nodes(G1, pos, node_color=[node_colors[node] for node in G1.nodes], ax=plt2.gca())
#     nx.draw_networkx_edges(G1, pos, ax=plt2.gca())
#     nx.draw_networkx_labels(G1, pos, font_weight='bold', ax=plt2.gca())
#
#     # Show the plot
#     plt2.show()

root_tk.mainloop()
# import networkx as nx
# import matplotlib.pyplot as plt
#
# # Create a sample graph
# G = nx.Graph()
# G.add_edges_from([(1, 2), (2, 3), (3, 1)])
#
# # Define node colors as a dictionary
# node_colors = {1: 'red', 2: 'green', 3: 'blue'}
#
# # Draw the graph with custom node colors
# nx.draw(G, with_labels=True, node_color=[node_colors[node] for node in G.nodes], font_color='white')
#
# # Show the plot
# plt.show()
