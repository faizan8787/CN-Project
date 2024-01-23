import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import matplotlib.pyplot as plt
import networkx as nx
import customtkinter
import time
from tkinter import simpledialog

class Device:
    all_devices = []
    all_ips=[]
    all_device_objects={}
    ips_table={}
    Registered_Emails={}
    all_emails=[]
    def __init__(self, name, device_type):
        print('hello')
        self.files={}
        self.ftp_server_files=None
        if device_type=="HTTP":
            message=f"I am HTTP:\n Like a waiter for your web browser,\n fetching pages and serving content with a smile."
            self.http_file=[message]
        if device_type=="FTP":
            self.ftp_server_files={}
        self.name = name
        self.device_type = device_type
        self.is_IP_set=False
        self.ip=None
        self.email_address=None
        self.email_configured=False
        self.email_inbox={}
        self.vpn=False
        self.email_store={}
        self.services={}
        self.attached_dns=None
        self.blocks_list=[]
        self.files_manager={'file1.txt':f"This is default System File of {self.name}!!"}
    def add_addressing(self, ip, subnet, DNS):
        ip=ip.get()
        self.subnet='255.255.255.0'
        if len(DNS)>0:
            self.attached_dns=DNS
        if ip and (ip not in Device.all_ips):
            # Remove spaces from the entered IP address
            ip = ip.replace(" ", "")
            # Split the IP address into octets
            octets = ip.split('.')

            # Check if it has four octets
            if len(octets) == 4:
                try:
                    # Convert each octet to an integer
                    octet1, octet2, octet3, octet4 = map(int, octets)
                    # Check if the first octet is in the range 192 to 223
                    if 192 <= octet1 <= 223:
                        print("Valid IP")
                        self.ip = ip
                        Device.all_ips.append(ip)
                        print(f"IP {self.ip} assigned to {self.name}")
                        Device.ips_table[ip] = self.name
                        self.is_IP_set=True
                    else:
                        print("Invalid IP - First octet not in the range 192 to 223")
                        messagebox.showwarning("Wrong IP")
                except ValueError:
                    messagebox.showwarning("Invalid IP - Octets must be integers")
            else:
                messagebox.showwarning("Invalid IP - Octets must be integers")
        else:
            messagebox.showwarning("Invalid Already Assigned")
    def POP3(self): #Email Inbox
        inbox_window = tk.Toplevel(root_tk)
        title = f"Email Inbox {self.name}"
        inbox_window.title(title)
        output_text = tk.Text(inbox_window, wrap=tk.WORD, height=30, width=200)
        output_text.pack(padx=10, pady=10)

        def fetch(fromm,to, path):
            # if receiver.name in cn.adjacency_list[fromm]:
            #     print("Ping Successful")
            #     return
            if not self.is_IP_set:
                messagebox.showwarning("IP not set")
                return
            for i in cn.adjacency_list[fromm]:
                if i[0:5] == "Email":
                    print(i)
                    server = Device.all_device_objects[i]
                    # server.email_store[receiver_name] = content
                    # print("Email Sent To ", server, )
                    print(server.email_store[self.name])
                    output_text.insert(tk.END, f"{server.email_store[self.name]}\n\n")
                    return
            if any('Switch' in element for element in cn.adjacency_list[fromm]):
                print("Sent to Switch")
                for i in cn.adjacency_list[fromm]:
                    if i[0:6] == "Switch":
                        print(f"Sent to {i}")
                        path.append(to)
                        fetch(i, to, path)
                        return
            print("Server Not Found")
        fetch(self.name, 'emailserver', [])
    def configure_email(self):
        print(f"Email Configuration", f"This is the email Configuration command by {self.name}")
        new_window = tk.Toplevel(root_tk)
        title = f"{self.name}'s Email Configuration"
        new_window.title(title)
        custom_font = ('Helvetica', 14, 'bold')

        name_label = tk.Label(new_window, text="Enter Your Name:", font=custom_font)
        email_address_label = tk.Label(new_window, text="Chose an email address", font=custom_font)

        name_label.place(x=400, y=60, anchor=tk.E)
        email_address_label.place(x=400, y=130, anchor=tk.E)

        entry_font = ('Helvetica', 14)
        name_entry = customtkinter.CTkEntry(new_window, height=50, width=500, font=entry_font)
        email_address_entry = customtkinter.CTkEntry(new_window, height=50, width=500, font=entry_font)

        name_entry.place(x=500, y=50)
        email_address_entry.place(x=500, y=120)
        def saving(address):
            try:
                if address[-10:]=="@gmail.com" and address not in Device.all_emails:
                    self.email_address=address
                    self.email_configured=True
                    Device.all_emails.append(address)
                    Device.Registered_Emails[address]=self.name
                else:
                    messagebox.showwarning("Invalid Address")
            except:
                messagebox.showwarning("Invalid")
        button_font = ('Helvetica', 14, 'bold')
        button = customtkinter.CTkButton(master=new_window, text="Save", font=button_font,
                                         command=lambda :saving(email_address_entry.get()))
        button.place(x=680, y=200)
    def Send_email(self):
        print(f"Email Composition", f"This is the email Composition command by {self.name}")
        new_window = tk.Toplevel(root_tk)
        title = f"{self.name}'s Email Composition"
        new_window.title(title)
        custom_font = ('Helvetica', 14, 'bold')
        receiver_label = tk.Label(new_window, text="Receiver's Email:", font=custom_font)
        Enter_here_label = tk.Label(new_window, text="Type here", font=custom_font)

        receiver_label.place(x=400, y=60, anchor=tk.E)
        Enter_here_label.place(x=400, y=130, anchor=tk.E)

        entry_font = ('Helvetica', 14)
        receiver_add_entry = customtkinter.CTkEntry(new_window, height=50, width=500, font=entry_font)
        email_content_entry = customtkinter.CTkEntry(new_window, height=50, width=500, font=entry_font)

        receiver_add_entry.place(x=500, y=50)
        email_content_entry.place(x=500, y=120)
        def sending(receiver_address, content):
            try:
                if receiver_address in Device.all_emails:
                    receiver_name=Device.Registered_Emails[receiver_address]
                    receiver=Device.all_device_objects[receiver_name]
                    print(f"The receiver Device is {receiver.name}")
                    content=f"By {self.name}: {content}"
                    def SMTP(fromm, to, path):
                        # if receiver.name in cn.adjacency_list[fromm]:
                        #     print("Ping Successful")
                        #     return
                        for i in cn.adjacency_list[fromm]:
                            if i[0:5]=="Email":
                                print(i)
                                server=Device.all_device_objects[i]
                                if self.is_IP_set and server.is_IP_set:
                                    server.email_store[receiver_name]=content
                                    print("Email Sent To ", server,)
                                    return
                                messagebox.showwarning("IP not Set")
                                return
                        if any('Switch' in element for element in cn.adjacency_list[fromm]):
                            print("Sent to Switch")
                            for i in cn.adjacency_list[fromm]:
                                if i[0:6] == "Switch":
                                    print(f"Sent to {i}")
                                    path.append(to)
                                    SMTP(i, to, path)
                                    return
                        print("Server Not Found")
                    SMTP(self.name,receiver_name,[])
                else:
                    messagebox.showerror("Invalid Email!!!")
            except:
                print("Invalid Address")
        button_font = ('Helvetica', 14, 'bold')
        button = customtkinter.CTkButton(master=new_window, text="Send", font=button_font,
                                         command=lambda :sending(receiver_add_entry.get(),email_content_entry.get()))
        button.place(x=680, y=200)


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
d=['PC', 'DNS', 'Switch', 'FTP', 'Email', 'HTTP']
c= ['red', 'green', 'blue', 'yellow', 'orange', 'purple']
# s=['*','s', '^', 'v','d', '8']
s=['s','o','^','>','v','<','d','p','h','8']
counter = {device_type: 0 for device_type in ['PC', 'DNS', 'Switch', 'FTP', 'Email', 'HTTP']}
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
    cn.show_graph()
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
    if connection_of_nodes[0][0:2]=="PC" and (len(Connection.adjacency_list[connection_of_nodes[0]])>0):
        messagebox.showwarning("The port is not available")
        return
    if connection_of_nodes[1][0:2]=="PC" and (len(Connection.adjacency_list[connection_of_nodes[1]])>0):
        messagebox.showwarning("The port is not available")
        return
    if (connection_of_nodes[0][0:5]=="Email" and (len(Connection.adjacency_list[connection_of_nodes[0]])>0)) or (connection_of_nodes[1][0:5]=="Email" and len(Connection.adjacency_list[connection_of_nodes[1]])>0):
        messagebox.showwarning("The Port is not available")
        return
    if connection_of_nodes[0][0:6]=="Switch" and connection_of_nodes[1][0:6]=="Switch":
        if any('Switch' in element for element in cn.adjacency_list[connection_of_nodes[0]]) or any('Switch' in element for element in cn.adjacency_list[connection_of_nodes[1]]):
            messagebox.showwarning("NO more than two switches can be added")
            return
    print("Connection of nodes", connection_of_nodes)
    G.add_edge(connection_of_nodes[0],connection_of_nodes[1])
    cn.add_edge(connection_of_nodes[0],connection_of_nodes[1])
    refresh_graph()
def remove_now():
    global connection_of_nodes, G
    G.remove_edge(connection_of_nodes[0],connection_of_nodes[1])
    cn.remove_edge(connection_of_nodes[0],connection_of_nodes[1])
    refresh_graph()
root_tk = tk.Tk()
root_tk.geometry("800x600")
root_tk.title("CustomTkinter Test")
cn = Connection()
G = nx.Graph()

# Create buttons for adding devices
add_pc_button = customtkinter.CTkButton(master=root_tk, text="Add PC", corner_radius=10, command=lambda: add_device('PC'))
add_pc_button.place(relx=0.05, rely=0.05, anchor=tk.CENTER)

add_dns_button = customtkinter.CTkButton(master=root_tk, text="Add DNS", corner_radius=10, command=lambda: add_device('DNS'))
add_dns_button.place(relx=0.05, rely=0.15, anchor=tk.CENTER)

add_email_button = customtkinter.CTkButton(master=root_tk, text="Add Email Server", corner_radius=10, command=lambda: add_device('Email'))
add_email_button.place(relx=0.05, rely=0.25, anchor=tk.CENTER)

add_switch_button = customtkinter.CTkButton(master=root_tk, text="Add Switch", corner_radius=10, command=lambda: add_device('Switch'))
add_switch_button.place(relx=0.05, rely=0.35, anchor=tk.CENTER)

add_hub_button = customtkinter.CTkButton(master=root_tk, text="Add FTP", corner_radius=10, command=lambda: add_device('FTP'))
add_hub_button.place(relx=0.05, rely=0.45, anchor=tk.CENTER)

add_http_button = customtkinter.CTkButton(master=root_tk, text="Add HTTP server", corner_radius=10, command=lambda: add_device('HTTP'))
add_http_button.place(relx=0.05, rely=0.55, anchor=tk.CENTER)

# Create a button to show the graph
graph_button = customtkinter.CTkButton(master=root_tk, text="Rearrange Devices", corner_radius=10, command=lambda: refresh_graph())
graph_button.place(relx=0.05, rely=0.75, anchor=tk.CENTER)

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
    from_combo_box_title_label = customtkinter.CTkLabel(root_tk, text="From")
    from_combo_box_title_label.place(relx=0.95, rely=0.17, anchor=tk.CENTER)
    to_combo_box_title_label = customtkinter.CTkLabel(root_tk, text="To")
    to_combo_box_title_label.place(relx=0.95, rely=0.27, anchor=tk.CENTER)
    connection_button = customtkinter.CTkButton(master=root_tk, text="Connect", corner_radius=10,command=lambda: connect_now())
    connection_button.place(relx=0.95, rely=0.4, anchor=tk.CENTER)
    remove_connection_button = customtkinter.CTkButton(master=root_tk, text="Remove Connection", corner_radius=10,command=lambda: remove_now())
    remove_connection_button.place(relx=0.95, rely=0.5, anchor=tk.CENTER)
    simulate_button = customtkinter.CTkButton(master=root_tk, text="Simulate", corner_radius=10,
                                                       command=lambda: simulate_setup())
    simulate_button.place(relx=0.95, rely=0.6, anchor=tk.CENTER)
def combo_box_to_select_device():
    comb_b_3_var=tk.StringVar()
    combo_box_3_title_label = tk.Label(root_tk, text="Open any device here")
    combo_box_3_title_label.place(relx=0.95, rely=0.75, anchor=tk.CENTER)
    combo_box3= customtkinter.CTkComboBox(master=root_tk,values=Device.all_devices,command=lambda x:combobox_3_callback(x),variable=comb_b_3_var)
    combo_box3.place(relx=0.95, rely=0.8, anchor=tk.CENTER)

def open_new_window(device):
    if device.device_type=="Switch":
        messagebox.showerror("Can't open this device")
        return
    new_window = tk.Toplevel(root_tk)
    new_window.title(device.name)
    
    ip_config_button = customtkinter.CTkButton(new_window, text="IP Configuration", corner_radius=10,
                                               command=lambda: ip_config_command(device))
    ip_config_button.pack(pady=10, anchor=tk.W)  # Use anchor=tk.W to align to the left
    if device.device_type=="DNS":
        services_button = customtkinter.CTkButton(new_window, text="Services", corner_radius=10,
                                                        command=lambda: Services(device))
        services_button.pack(pady=10, anchor=tk.W)
        Block_button = customtkinter.CTkButton(new_window, text="Block", corner_radius=10,
                                                   command=lambda: Block(device))
        Block_button.pack(pady=10, anchor=tk.W)
        return
    # Add Command Prompt button
    command_prompt_button = customtkinter.CTkButton(new_window, text="Command Prompt", corner_radius=10,
                                                    command=lambda: open_command_prompt(device))
    command_prompt_button.pack(pady=10, anchor=tk.W)

    # Add Web Browser button
    web_browser_button = customtkinter.CTkButton(new_window, text="Web Browser", corner_radius=10,
                                                 command=lambda: web_browser_command(device))
    web_browser_button.pack(pady=10, anchor=tk.W)

    # Add Email button
    configure_email_button = customtkinter.CTkButton(new_window, text=" Configure Email", corner_radius=10,
                                                   command=lambda: device.configure_email())
    configure_email_button.pack(pady=10, anchor=tk.W)
    compose_email_button = customtkinter.CTkButton(new_window, text=" Compose Email", corner_radius=10,
                                           command=lambda: device.Send_email())
    compose_email_button.pack(pady=10, anchor=tk.W)
    inbox_email_button = customtkinter.CTkButton(new_window, text="Inbox", corner_radius=10,
                                                   command=lambda: device.POP3())
    inbox_email_button.pack(pady=10, anchor=tk.W)
    # Add Text Editor button
    text_editor_button = customtkinter.CTkButton(new_window, text="Text Editor", corner_radius=10,
                                                 command=lambda: text_editor_command(device))
    # text_editor_button.pack(pady=10, anchor=tk.W)

    # Add Files Manager button
    files_manager_button = customtkinter.CTkButton(new_window, text="Files Manager", corner_radius=10,
                                                   command=lambda: files_manager_command(device))
    # files_manager_button.pack(pady=10, anchor=tk.W)
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%55d", device.device_type)

    about_text = tk.Text(new_window, width=40, height=10)
    about_text.place(x=50, y=400)
    # Add About button
    about_button = customtkinter.CTkButton(new_window, text="About", corner_radius=10,
                                           command=lambda: about_command(device,about_text))
    about_button.pack(pady=10, anchor=tk.W)
def Block(device):
    print(f"\Blocks", f"This is the Blocks command by {device.name}")
    new_window = tk.Toplevel(root_tk)
    title = f"{device.name}'s Services"
    new_window.title(title)
    custom_font = ('Helvetica', 14, 'bold')
    ip_label = tk.Label(new_window, text="IP Address:", font=custom_font)
    ip_label.place(x=400, y=60, anchor=tk.E)
    entry_font = ('Helvetica', 14)
    ip_entry = customtkinter.CTkEntry(new_window, height=50, width=500, font=entry_font)
    ip_entry.place(x=500, y=50)
    button_font = ('Helvetica', 14, 'bold')
    button = customtkinter.CTkButton(master=new_window, text="Block", font=button_font,
                                     command=lambda: block_it(ip_entry.get()))
    button.place(x=680, y=200)
    def block_it(ip):
        device.blocks_list.append(ip)



def ip_config_command(device):
    print(f"IP Configuration", f"This is the IP Configuration command by {device.name}")
    new_window = tk.Toplevel(root_tk)
    title = f"{device.name}'s Configuration"
    new_window.title(title)
    custom_font = ('Helvetica', 14, 'bold')

    ip_label = tk.Label(new_window, text="IP Address:", font=custom_font)
    subnet_label = tk.Label(new_window, text="Subnet Mask:", font=custom_font)
    DNS_label = tk.Label(new_window, text="DNS", font=custom_font)

    ip_label.place(x=400, y=60, anchor=tk.E)
    subnet_label.place(x=400, y=110, anchor=tk.E)
    DNS_label.place(x=400, y=170, anchor=tk.E)

    entry_font = ('Helvetica', 14)
    ip_entry = customtkinter.CTkEntry(new_window, height=50, width=500, font=entry_font)
    subnet_entry = customtkinter.CTkEntry(new_window, height=50, width=500, font=entry_font)
    DNS_entry = customtkinter.CTkEntry(new_window, height=50, width=500, font=entry_font)

    ip_entry.place(x=500, y=50)
    subnet_entry.place(x=500, y=100)
    DNS_entry.place(x=500, y=150)

    button_font = ('Helvetica', 14, 'bold')
    button = customtkinter.CTkButton(master=new_window, text="Save", font=button_font, command=lambda: device.add_addressing(ip_entry, subnet_entry.get(), DNS_entry.get()))
    button.place(x=680, y=200)


def open_command_prompt(device):
    command_prompt_window = tk.Toplevel(root_tk)
    title=f"Command Prompt {device.name}"
    command_prompt_window.title(title)

    output_text = tk.Text(command_prompt_window, wrap=tk.WORD, height=30, width=200)
    output_text.pack(padx=10, pady=10)
    input_entry = customtkinter.CTkEntry(command_prompt_window, height=40, width=500, font=('default', 30))
    # input_entry = customtkinter.CTkEntry(command_prompt_window, width=80, corner_radius=5)
    input_entry.pack(padx=10, pady=10)
    def execute_command():
        command = input_entry.get()
        output_text.insert(tk.END, f"\n>>> {command}\n")
        try:
            if command[0:5]=='ping ':
                print("------>",command[5:])
                pointed_device=Device.ips_table[command[5:]]
                if pointed_device not in Device.all_devices:
                    output_text.insert(tk.END, "Invalid IP\n\n")
                    return
                print("The entered Ip is of ",pointed_device)
                print(Device.all_device_objects[pointed_device].name, Device.all_device_objects[pointed_device].device_type)
                # path=[]
                def ping(fromm, to, path):
                    if pointed_device in cn.adjacency_list[fromm]:
                        
                        message=f"Packet Sent------> Packet Received! at time {time.time()}\n\n"
                        output_text.insert(tk.END, message)
                        print("Ping Successful")
                        return
                    if any('Switch' in element for element in cn.adjacency_list[fromm]):
                        print("Sent to Switch")
                        for i in cn.adjacency_list[fromm]:
                            if i[0:6]=="Switch":
                                print(f"Sent to {i}")
                                path.append(to)
                                ping(i,to,path)
                                return
                    output_text.insert(tk.END, ""
                                               "Packet not Received!\n\n")
                    print("Ping Unseccessfull")
                if device.device_type=="PC":
                    if device.is_IP_set==True:
                        ping(device.name, pointed_device,[device.name])
                        
                        ping(device.name, pointed_device,[device.name])
                        
                        ping(device.name, pointed_device,[device.name])
                        
                        ping(device.name, pointed_device,[device.name])
                    else:
                        output_text.insert(tk.END, ""
                                                   "sender has no ip\n\n")
                else:
                    output_text.insert(tk.END, ""
                                               "Invalid Device\n\n")
            elif command[0:4]=='ftp ':
                print("------>", command[4:])
                def get_mac(ip):
                    return Device.ips_table[ip]
                mac_of_server = get_mac(command[4:])
                if mac_of_server not in cn.adjacency_list:
                    output_text.insert(tk.END, ""
                                               "Invalid Ip for FTP\n\n")
                    return
                obj=Device.all_device_objects[mac_of_server]
                if obj.device_type!="FTP":
                    output_text.insert(tk.END, ""
                                               "Pointed Device is not FTP!!\n\n")
                    return
                if not nx.has_path(G, device.name, mac_of_server):
                    output_text.insert(tk.END, "No Server in range!!:(")
                    return
                if not device.is_IP_set:
                    output_text.insert(tk.END, "First Set your IP!!")
                    return
                def return_command(entry):
                    return command

                output_text.insert(tk.END, f"\n>>> Enter User Name (by default: device name)\n")
                command = simpledialog.askstring("FTP Login", "Enter User Name (by default: device name): ")
                if not command==device.name:
                    output_text.insert(tk.END, f"\n Invalid User Name\n")
                    return
                # command = input_entry.get()
                output_text.insert(tk.END, f"\n>>> Enter Password: By default: 123\n")
                command = simpledialog.askstring("FTP Login", "Enter Password (by default: 123): ")
                if not command=='123':
                    output_text.insert(tk.END, f"\n Invalid User Name\n")
                    return
                output_text.insert(tk.END, f"\nYou can use FTP services Now\n")
                command = simpledialog.askstring("FTP services","Write you put/get command here!!")
                action=command[0:4]
                if action=='put ':
                    file_name=command[4:]
                    if file_name not in device.files_manager:
                        output_text.insert(tk.END, f"\nNo Such File found\n")
                        return
                    obj.ftp_server_files[file_name]=device.files_manager[file_name]
                    output_text.insert(tk.END, f"\nFile Successfully Uploaded\n")
                if action=='get ':
                    file_name = command[4:]
                    if file_name in obj.ftp_server_files:
                        output_text.insert(tk.END, f"\n\n {obj.ftp_server_files[file_name]}\n")
                    else:
                        output_text.insert(tk.END, f"\n\n Server does not have this File\n")
                pass
            else:
                output_text.insert(tk.END, ""
                                           "Invalid Command\n\n")
        except:
            messagebox.showwarning("invalid")
            output_text.insert(tk.END, ""
                                   "Invalid Command\n\n")
    def on_entry_return(event):
        execute_command()
    input_entry.delete(0, tk.END)
    input_entry.bind("<Return>", on_entry_return)
    run_button = customtkinter.CTkButton(command_prompt_window, text="Run", corner_radius=10, command=execute_command)
    run_button.pack(pady=10)

def web_browser_command(device):
    web_browser_window = tk.Toplevel(root_tk)
    title = f"Web Browser {device.name}"
    
    web_browser_window.title(title)
    output_text = tk.Text(web_browser_window, wrap=tk.WORD, height=30, width=200)
    output_text.pack(padx=10, pady=10)
    search_entry = customtkinter.CTkEntry(web_browser_window, height=40, width=500, font=('default', 30))
    search_entry.pack(padx=10, pady=10)
    search_button = customtkinter.CTkButton(web_browser_window, text="Search", corner_radius=10, command=lambda :decision_to_go_dns())
    search_button.pack(pady=10)
    toggle_var = tk.IntVar()
    def toggle():
        if toggle_var.get():
            label.config(text="Toggle is ON")
            device.vpn=True
        else:
            label.config(text="Toggle is OFF")
            device.vpn=False
    # Create a Checkbutton for the toggle switch
    toggle_button = tk.Checkbutton(web_browser_window, text="VPN", variable=toggle_var, command=toggle)
    toggle_button.pack()

    # Create a label to display the current state of the toggle switch
    label = tk.Label(web_browser_window, text="VPN")
    label.pack()

    def get_mac(ip):
        return Device.ips_table[ip]
    def HTTP_protocol(the_ip):
        if the_ip not in Device.all_ips:
            output_text.insert(tk.END, "OOps! Server Did Not respond:(")
            return
        mac=get_mac(the_ip)
        if not nx.has_path(G, device.name, mac):
            output_text.insert(tk.END, "No Server in range!!:(")
            return
        if not device.is_IP_set:
            output_text.insert(tk.END, "Your IP is not Set:(")
            return
        obj=Device.all_device_objects[mac]
        output_text.insert(tk.END, str(obj.http_file))
    def decision_to_go_dns():
        if search_entry.get()[0:3]!='www':
            HTTP_protocol(search_entry.get())
            return
        if not device.attached_dns:
            output_text.insert(tk.END, "DNS is not active")
            return
        mac_of_dns=get_mac(device.attached_dns)
        if not nx.has_path(G, device.name, mac_of_dns):
            output_text.insert(tk.END, "No DNS in range!!:(")
            return
        dns_obj=Device.all_device_objects[mac_of_dns]
        if device.ip in dns_obj.blocks_list:
            if device.vpn==False:
                output_text.insert(tk.END, "You are blocked!!")
                return
            else:
                output_text.insert(tk.END, "Using")
                
        if search_entry.get() not in dns_obj.services:
            output_text.insert(tk.END, "DNS does not know this Domain name")
            return
        fetched_ip=dns_obj.services[search_entry.get()]
        HTTP_protocol(fetched_ip)
def Services(device):
    print(f"\Services", f"This is the Services command by {device.name}")
    new_window = tk.Toplevel(root_tk)
    title = f"{device.name}'s Services"
    new_window.title(title)
    custom_font = ('Helvetica', 14, 'bold')
    ip_label = tk.Label(new_window, text="IP Address:", font=custom_font)
    domain_name_label = tk.Label(new_window, text="Domain Name", font=custom_font)
    ip_label.place(x=400, y=60, anchor=tk.E)
    domain_name_label.place(x=400, y=110, anchor=tk.E)
    entry_font = ('Helvetica', 14)
    ip_entry = customtkinter.CTkEntry(new_window, height=50, width=500, font=entry_font)
    domain_name_entry = customtkinter.CTkEntry(new_window, height=50, width=500, font=entry_font)
    ip_entry.place(x=500, y=50)
    domain_name_entry.place(x=500, y=100)
    button_font = ('Helvetica', 14, 'bold')
    button = customtkinter.CTkButton(master=new_window, text="Add", font=button_font,
                                     command=lambda: save_services(domain_name_entry.get(),ip_entry.get()))
    button.place(x=680, y=200)
    def save_services(domain_name,ip):
        device.services[domain_name]=ip
        print(f"{domain_name} has been allocated to ip {ip}")

def email_command(device):
    simpledialog.messagebox.showinfo("Email", "This is the Email command. BY ", device.name)

def text_editor_command(device):
    print(f"Text Editor: This is the Text Editor command. By {device.name}")
    messagebox.showinfo("I will be functional soon")

def files_manager_command(device):
    print(f"Files Manager: This is the Files Manager command. By {device.name}")

# def about_command(device):
#     print(f"About", "This is the About command. By {device.name}"
def about_command(device, about_text):
    random_info = f"\nDevice Name: {device.name}\nDevice Type: {device.device_type}\nIP: {device.ip}\n {device.attached_dns}\nServices={device.services}"
    about_text.insert(tk.END, random_info)
def initialize_graph(graph):
    # Set a default color for edges
    for u, v in graph.edges():
        graph[u][v]['color'] = 'black'

def simulate_data_transfer(graph, pos, source_node, destination_node):
    path = nx.shortest_path(graph, source=source_node, target=destination_node)
    ob1=Device.all_device_objects[source_node]
    ob2=Device.all_device_objects[destination_node]
    if not ob1.is_IP_set or not ob1.is_IP_set:
        messagebox.showerror("Sorry!! Can't Proceed with this")
        return
    for i in range(len(path) - 1):
        current_node = path[i]
        next_node = path[i + 1]

        # Highlight the edge
        graph[current_node][next_node]['color'] = 'red'

        # Update the plot with annotations
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color=[graph[u][v]['color'] for u, v in graph.edges()])
        nx.draw_networkx_edge_labels(graph, pos, edge_labels={(current_node, next_node): 'Message'}, font_color='red')
        plt.pause(2)  # Pause for 2 seconds to slow down the transfer

    # Simulate acknowledgment by changing the color of the path
    for i in range(len(path) - 1, 0, -1):
        current_node = path[i]
        previous_node = path[i - 1]

        # Change the color of the path to indicate acknowledgment
        graph[current_node][previous_node]['color'] = 'green'

        # Update the plot with annotations
        nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color=[graph[u][v]['color'] for u, v in graph.edges()])
        nx.draw_networkx_edge_labels(graph, pos, edge_labels={(current_node, previous_node): 'Acknowledgment'}, font_color='green')
        plt.pause(2)  # Pause for 2 seconds to slow down the acknowledgment

    # Draw the final state of the graph without clearing the plot
    nx.draw(graph, pos, with_labels=True, node_color='lightblue', edge_color=[graph[u][v]['color'] for u, v in graph.edges()])
    plt.show()

def simulate_setup():
    global connection_of_nodes
    pos = nx.spring_layout(G)
    plt.clf()
    nx.draw(G, pos, with_labels=True, node_color='lightblue')
    initialize_graph(G)
    plt.close('all')
    simulate_data_transfer(G, pos, connection_of_nodes[0], connection_of_nodes[1])
root_tk.mainloop()
