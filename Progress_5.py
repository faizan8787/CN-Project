import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx
import customtkinter
from tkinter import simpledialog

class Device:
    all_devices = []
    all_ips=[]
    all_device_objects={}
    def __init__(self, name, device_type):
        print('hello')
        self.name = name
        self.device_type = device_type
    def add_addressing(self, ip, subnet, default_gateway):
        if ip and (ip not in Device.all_ips):
            self.ip=ip
            Device.all_ips.append(ip)
            print(f"IP {self.ip} assigned to {self.name}")
        else:
            messagebox.showwarning("Invalid address")


class Connection:
    adjacency_list = {}
    objects = []
    def insert_vertex(self, my_obj):
        Connection.adjacency_list[my_obj.name] = []
        Connection.objects.append(my_obj)
    def add_edge(self, from_, to):
        if from_ == to:
            print("Can't connect with itself")
            return
        if Connection.adjacency_list.get(from_) is None or Connection.adjacency_list.get(to) is None:
            print("Edge can't be added between non-existent nodes")
            return
        if to in Connection.adjacency_list[from_]:
            print("Already Connected")
            return
        Connection.adjacency_list[from_].append(to)
        Connection.adjacency_list[to].append(from_)
    def remove_edge(self, from_, to):
        if Connection.adjacency_list.get(from_) is None or Connection.adjacency_list.get(to) is None:
            print("Edge can't be removed between non-existent nodes")
            return
        if to in Connection.adjacency_list[from_]:
            Connection.adjacency_list[from_].remove(to)
            Connection.adjacency_list[to].remove(from_)
            return

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
        Device.all_device_objects[device_name]=ob
        cn.insert_vertex(ob)
    refresh_graph()
fig=None
def refresh_graph():
    global fig
    if fig:
        plt.close(fig)
    else:
        print("NO")
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
def combobox_3_callback(choice):
    print("The Selected Device is ", choice)
    print("Its address is ", Device.all_device_objects[choice])
    print("Varification: ", Device.all_device_objects[choice].name)
    open_new_window(Device.all_device_objects[choice])

# def open_new_window(device):
#     new_window = tk.Toplevel(root_tk)
#     new_window.title(device.name)

def connect_now():
    global connection_of_nodes, G
    print(f"Connection will be built from {connection_of_nodes[0]} to {connection_of_nodes[1]}")
    if connection_of_nodes[0]==connection_of_nodes[1]:
        print("Can't connect with itself")
        return
    G.add_edge(connection_of_nodes[0],connection_of_nodes[1])
    cn.add_edge(connection_of_nodes[0],connection_of_nodes[1])
    refresh_graph()
def remove_now():
    global connection_of_nodes, G
    G.remove_edge(connection_of_nodes[0],connection_of_nodes[1])
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

select_device_button = customtkinter.CTkButton(master=root_tk, text="Select Device", corner_radius=10, command=lambda: combo_box_to_select_device())
select_device_button.place(relx=0.95, rely=0.7, anchor=tk.CENTER)
# Create combo boxes for "From" and "To" devices
currently_selected_device=None
def combo_boxes():
    from_combobox_var = tk.StringVar()
    to_combobox_var = tk.StringVar()
    from_combobox = customtkinter.CTkComboBox(master=root_tk,values=Device.all_devices,command=lambda x:combobox_1_callback(x),variable=from_combobox_var)
    from_combobox.place(relx=0.95, rely=0.2, anchor=tk.CENTER)
    to_combobox = customtkinter.CTkComboBox(master=root_tk,values=Device.all_devices,command=lambda x:combobox_2_callback(x),variable=to_combobox_var)
    to_combobox.place(relx=0.95, rely=0.3, anchor=tk.CENTER)
    connection_button = customtkinter.CTkButton(master=root_tk, text="Connect", corner_radius=10,command=lambda: connect_now())
    connection_button.place(relx=0.95, rely=0.4, anchor=tk.CENTER)
    remove_connection_button = customtkinter.CTkButton(master=root_tk, text="Remove Connection", corner_radius=10,command=lambda: remove_now())
    remove_connection_button.place(relx=0.95, rely=0.5, anchor=tk.CENTER)
def combo_box_to_select_device():
    comb_b_3_var=tk.StringVar()
    combo_box3= customtkinter.CTkComboBox(master=root_tk,values=Device.all_devices,command=lambda x:combobox_3_callback(x),variable=comb_b_3_var)
    combo_box3.place(relx=0.95, rely=0.8, anchor=tk.CENTER)

def open_new_window(device):
    new_window = tk.Toplevel(root_tk)
    new_window.title(device.name)

    # Add IP Configuration button
    ip_config_button = customtkinter.CTkButton(new_window, text="IP Configuration", corner_radius=10, command=lambda: ip_config_command(device))
    ip_config_button.pack(pady=10)

    # Add Command Prompt button
    command_prompt_button = customtkinter.CTkButton(new_window, text="Command Prompt", corner_radius=10, command=lambda: open_command_prompt(device))
    command_prompt_button.pack(pady=10)

    # Add Web Browser button
    web_browser_button = customtkinter.CTkButton(new_window, text="Web Browser", corner_radius=10, command=lambda: web_browser_command(device))
    web_browser_button.pack(pady=10)

    # Add Email button
    email_button = customtkinter.CTkButton(new_window, text="Email", corner_radius=10, command=lambda: email_command(device))
    email_button.pack(pady=10)

    # Add Text Editor button
    text_editor_button = customtkinter.CTkButton(new_window, text="Text Editor", corner_radius=10, command=lambda: text_editor_command(device))
    text_editor_button.pack(pady=10)

    # Add Files Manager button
    files_manager_button = customtkinter.CTkButton(new_window, text="Files Manager", corner_radius=10, command=lambda: files_manager_command(device))
    files_manager_button.pack(pady=10)

    # Add About button
    about_button = customtkinter.CTkButton(new_window, text="About", corner_radius=10, command=lambda: about_command(device))
    about_button.pack(pady=10)

def ip_config_command(device):
    print(f"IP Configuration", f"This is the IP Configuration command by {device.name}")
    new_window = tk.Toplevel(root_tk)
    title=f"{device.name}'s Configuration"
    new_window.title(title)
    ip_entry = customtkinter.CTkEntry(new_window, height=50, width=500, font=('default', 30))
    subnet_entry=customtkinter.CTkEntry(new_window, height=50, width=500, font=('default', 30))
    default_gateway=customtkinter.CTkEntry(new_window, height=50, width=500, font=('default', 30))
    button = customtkinter.CTkButton(master=new_window, text="Save", command=lambda: device.add_addressing(ip_entry.get(), subnet_entry.get(),default_gateway.get()))
    ip_entry.place(x=500, y=50)
    subnet_entry.place(x=500, y=100)
    button.place(x=680, y=150)


def open_command_prompt(device):
    command_prompt_window = tk.Toplevel(root_tk)
    title=f"Command Prompt {device.name}"
    command_prompt_window.title(title)

    output_text = tk.Text(command_prompt_window, wrap=tk.WORD, height=20, width=80)
    output_text.pack(padx=10, pady=10)

    input_entry = customtkinter.CTkEntry(command_prompt_window, width=80, corner_radius=5)
    input_entry.pack(padx=10, pady=10)

    def execute_command():
        command = input_entry.get()
        output_text.insert(tk.END, f"\n>>> {command}\n")
        try:
            if command[0:5]=='ping ':
                messagebox.showinfo("valid")
            else:
                messagebox.showwarning("invalid")
        except:
            messagebox.showwarning("invalid")
        output_text.insert(tk.END, "Command executed!\n\n")
        input_entry.delete(0, tk.END)

    run_button = customtkinter.CTkButton(command_prompt_window, text="Run", corner_radius=10, command=execute_command)
    run_button.pack(pady=10)

def web_browser_command(device):
    print(f"Web Browser", "This is the Web Browser command. By{device.name}")

def email_command(device):
    simpledialog.messagebox.showinfo("Email", "This is the Email command. BY ", device.name)

def text_editor_command(device):
    print(f"Text Editor", "This is the Text Editor command. By {device.name}")

def files_manager_command(device):
    print(f"Files Manager", "This is the Files Manager command. By {device.name}")

def about_command(device):
    print(f"About", "This is the About command. By {device.name}")

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
