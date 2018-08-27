from tkinter import *
from model.RequestManager import RequestManager
from model.users import User
import sqlite3
from model.monitor import Monitor
import json
from tkinter import ttk
import threading
import multiprocessing


def run_gui():
    root = Tk()
    root.configure(background='#f4f4f4')
    request_manager = RequestManager()
    requests_available = request_manager.requests_dict

    def get_status():
        disable_all_widgets()
        result_box.delete(1.0, END)
        selected_users_list = selected_users_box.get(0, END)
        selected_requests_list = selected_requests_box.get(0, END)
        for username in selected_users_list:
            result_box.insert(INSERT, '{}:\n'.format(username), "bold")
            monitor = Monitor(username=username, endpoint=endpoint_combobox.get())
            for request_name in selected_requests_list:
                    user = User.get_user_by_name(username=username)
                    monitor.get_status(req_name=request_name, password=user.password)
                    for result in monitor.result_list:
                        if result['status'] == 'Obtained':
                            result_box.insert(INSERT, '    {}: {}\n'.format(request_name, result['status_code']), 'obtained')
                            if show_full_response_variable.get() == 1:
                                result_box.insert(END, json.dumps(monitor.hub.responses[request_name][result['index']], indent=2) + "\n\n")
                        elif result['status'] == 'Failed':
                            result_box.insert(INSERT, '    {}: {}\n'.format(request_name, result['status_code']), 'failed')
                        root.update()
                        if request_name in ('self', 'billing-accounts', 'mobile-subscriptions') and monitor.req_status == 'Failed':
                            break
                    monitor.refresh_status()
        enable_all_widgets()


    def get_paym_list():
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM users WHERE type="PAYM"'
        result = cursor.execute(query)
        data = result.fetchall()
        paym_list = [{'username': row[0], 'password': row[1], 'type': row[2]} for row in data]
        return paym_list


    def get_payg_list():
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'SELECT * FROM users WHERE type="PAYG"'
        result = cursor.execute(query)
        data = result.fetchall()
        payg_list = [{'username': row[0], 'password': row[1], 'type': row[2]} for row in data]
        return payg_list

    def put_paym_data_in_name_field(event):
        if PAYM_combobox.get() != "":
            username = PAYM_combobox.get()
            PAYG_combobox.delete(0, END)
            new_username_entry.delete(0, END)
            new_username_entry.insert(END, username)
            for user in paym_list:
                if user['username'] == username:
                    new_password_entry.delete(0, END)
                    new_type_combobox.delete(0, END)
                    new_password_entry.insert(END, user['password'])
                    new_type_combobox.insert(END, user['type'])
                    add_user_button.config(state=NORMAL)
                    delete_user_button.config(state=NORMAL)

    def put_payg_data_in_name_field(event):
        if PAYG_combobox.get() != "":
            username = PAYG_combobox.get()
            PAYM_combobox.delete(0, END)
            new_username_entry.delete(0, END)
            new_username_entry.insert(END, username)
            for user in payg_list:
                if user['username'] == username:
                    new_password_entry.delete(0, END)
                    new_type_combobox.delete(0, END)
                    new_password_entry.insert(END, user['password'])
                    new_type_combobox.insert(END, user['type'])
                    add_user_button.config(state=NORMAL)
                    delete_user_button.config(state=NORMAL)

    def add_user_to_db():
        new_user = User(username=new_username_entry.get(), password=new_password_entry.get(), type=new_type_combobox.get())
        result = new_user.add_user()
        result_box.delete(1.0, END)
        result_box.insert(END, result)
        payg_list = get_payg_list()
        paym_list = get_paym_list()
        PAYM_user_box.delete(0, END)
        PAYG_user_box.delete(0, END)
        PAYM_combobox_values = []
        PAYG_combobox_values = []
        for user in paym_list:
            PAYM_user_box.insert(END, user['username'])
            PAYM_combobox_values.append(user['username'])
        for user in payg_list:
            PAYG_user_box.insert(END, user['username'])
            PAYG_combobox_values.append(user['username'])
        PAYM_combobox.config(values=PAYM_combobox_values)
        PAYG_combobox.config(values=PAYG_combobox_values)
        root.update_idletasks()

    def delete_user():
        new_user = User(username=new_username_entry.get(), password=new_password_entry.get(), type=new_type_combobox.get())
        result = new_user.delete_user()
        result_box.delete(1.0, END)
        result_box.insert(END, result)
        payg_list = get_payg_list()
        paym_list = get_paym_list()
        PAYM_user_box.delete(0, END)
        PAYG_user_box.delete(0, END)
        PAYM_combobox_values = []
        PAYG_combobox_values = []
        for user in paym_list:
            PAYM_user_box.insert(END, user['username'])
            PAYM_combobox_values.append(user['username'])
        for user in payg_list:
            PAYG_user_box.insert(END, user['username'])
            PAYG_combobox_values.append(user['username'])
        PAYM_combobox.config(values=PAYM_combobox_values)
        PAYG_combobox.config(values=PAYG_combobox_values)
        root.update_idletasks()


    def enable_button(event):
        if new_username_entry.get() == '' or new_password_entry.get() == '' or new_type_combobox.get() == '':
            add_user_button.config(state=DISABLED)
            delete_user_button.config(state=DISABLED)
        else:
            add_user_button.config(state=NORMAL)
            delete_user_button.config(state=NORMAL)


    def disable_all_widgets():
        start_monitoring_button.config(state=DISABLED)
        endpoint_combobox.config(state=DISABLED)
        PAYG_combobox.config(state=DISABLED)
        PAYM_combobox.config(state=DISABLED)
        new_password_entry.config(state=DISABLED)
        new_username_entry.config(state=DISABLED)
        new_type_combobox.config(state=DISABLED)
        if add_user_button['state'] == NORMAL and delete_user_button['state'] == NORMAL:
            add_user_button.config(state=DISABLED)
            delete_user_button.config(state=DISABLED)


    def enable_all_widgets():
        start_monitoring_button.config(state=NORMAL)
        endpoint_combobox.config(state=NORMAL)
        PAYG_combobox.config(state=NORMAL)
        PAYM_combobox.config(state=NORMAL)
        new_password_entry.config(state=NORMAL)
        new_username_entry.config(state=NORMAL)
        new_type_combobox.config(state=NORMAL)
        if add_user_button['state'] == DISABLED and delete_user_button['state'] == DISABLED and new_username_entry.get() != '' and new_password_entry.get() != '':
            add_user_button.config(state=NORMAL)
            delete_user_button.config(state=NORMAL)

    process = multiprocessing.Process(target=get_status)
    process.daemon = True

    paym_list = get_paym_list()
    payg_list = get_payg_list()

    root.title("BF Monitor")
    root.resizable(False, False)

    PAYM_label = Label(root, text='PAYM', padx=3, background='#f4f4f4')
    PAYM_label.grid(row=1, column=1, pady=5)

    PAYM_user_box = Listbox(root, width=23)
    PAYM_user_box.grid(row=2, column=1, padx=10)
    for user in paym_list:
        PAYM_user_box.insert(END, user['username'])

    PAYG_label = Label(root, text='PAYG', padx=3, background='#f4f4f4')
    PAYG_label.grid(row=1, column=5, pady=5)

    PAYG_user_box = Listbox(root, width=23)
    PAYG_user_box.grid(row=2, column=5, padx=10)
    for user in payg_list:
        PAYG_user_box.insert(END, user['username'])

    select_paym_button = Button(root, text='>>', highlightbackground='#f4f4f4', width=1)
    select_paym_button.grid(row=2, column=2)
    select_paym_button.bind('<Button-1>', lambda e: selected_users_box.insert(END, PAYM_user_box.get(ACTIVE)))

    select_payg_button = Button(root, text='<<', highlightbackground='#f4f4f4', width=1)
    select_payg_button.grid(row=2, column=4)
    select_payg_button.bind('<Button-1>', lambda e: selected_users_box.insert(END, PAYG_user_box.get(ACTIVE)))

    selected_users_box = Listbox(root, width=23)
    selected_users_box.grid(row=2, column=3, padx=10)
    selected_users_box.bind('<Delete>', lambda e: selected_users_box.delete(ACTIVE))
    selected_users_box.bind('<BackSpace>', lambda e: selected_users_box.delete(ACTIVE))

    PAYM_request_available_box = Listbox(root, width=23)
    PAYM_request_available_box.grid(row=3, column=1, padx=10, pady=5)
    for request, data in requests_available.items():
        for type in data['user_type']:
            if type == 'PAYM':
                PAYM_request_available_box.insert(END, request)

    select_paym_request_button = Button(root, text='>>', highlightbackground='#f4f4f4', width=1)
    select_paym_request_button.grid(row=3, column=2)
    select_paym_request_button.bind('<Button-1>', lambda e: selected_requests_box.insert(END, PAYM_request_available_box.get(ACTIVE)))

    selected_requests_box = Listbox(root, width=23, selectmode=EXTENDED)
    selected_requests_box.grid(row=3, column=3, pady=5, padx=10)
    selected_requests_box.insert(END, 'self', 'billing-accounts', 'mobile-subscriptions')
    selected_requests_box.bind('<Delete>', lambda e: selected_requests_box.delete(ACTIVE))
    selected_requests_box.bind('<BackSpace>', lambda e: selected_requests_box.delete(ACTIVE))

    select_payg_request_button = Button(root, text='<<', highlightbackground='#f4f4f4', width=1)
    select_payg_request_button.grid(row=3, column=4)
    select_payg_request_button.bind('<Button-1>', lambda e: selected_requests_box.insert(END, PAYG_request_available_box.get(ACTIVE)))

    PAYG_request_available_box = Listbox(root, width=23)
    PAYG_request_available_box.grid(row=3, column=5, padx=5)
    for request, data in requests_available.items():
        for type in data['user_type']:
            if type == 'PAYG':
                PAYG_request_available_box.insert(END, request)

    endpoint_label = Label(root, text='Choose endpoint from the list:', background='#f4f4f4')
    endpoint_label.grid(row=4, column=1, columnspan=2)

    endpoint_combobox = ttk.Combobox(root, values=['digital-ss', 'digital-peacock', 'digital-PPP', 'digital-maruca', 'digital-alaba'], width=21, state='readonly')
    endpoint_combobox.current(0)
    endpoint_combobox.grid(row=4, column=3)

    show_full_response_variable = IntVar()
    show_full_response_variable.set(0)
    show_full_response_checkbox = Checkbutton(root, text='Show a full response', background='#f4f4f4', variable=show_full_response_variable)
    show_full_response_checkbox.grid(row=5, column=3)

    def start_monitoring():
        get_status()

    start_monitoring_button = Button(root, highlightbackground='#f4f4f4', text='START MONITORING', activebackground='red', command=start_monitoring)
    start_monitoring_button.grid(row=6, column=3, sticky=W)

    def stop():
        process.terminate()

    stop_monitoring_button = Button(root, highlightbackground='#f4f4f4', text='STOP', padx=3, command=stop)
    stop_monitoring_button.grid(row=6, column=3, sticky=E)

    result_box = Text(root, width=69, height=55, borderwidth=2, wrap=WORD, takefocus=True)
    result_box.grid(row=2, rowspan=55, column=6, pady=5, sticky=N)
    result_box.tag_config('obtained', background="PaleGreen1", foreground="black")
    result_box.tag_config('failed', background="coral", foreground="black")
    result_box.tag_config('bold', font="Helvetica 14 bold")

    scrollbar = Scrollbar(root, orient=VERTICAL, command=result_box.yview)
    scrollbar.grid(row=2, column=7, sticky="ns", rowspan=55)
    result_box.config(yscrollcommand=scrollbar.set)

    add_user_label = Label(root, text='Manage users:', background='#f4f4f4')
    add_user_label.grid(row=7, column=1, sticky=W, padx=5)

    PAYM_combobox_values = []
    for user in paym_list:
        PAYM_combobox_values.append(user['username'])
    PAYM_combobox = ttk.Combobox(root, values=PAYM_combobox_values, width=25)
    PAYM_combobox.grid(row=8, column=1, columnspan=2, sticky=W, padx=5)
    PAYM_combobox.bind("<<ComboboxSelected>>", put_paym_data_in_name_field)

    PAYG_combobox_values = []
    for user in payg_list:
        PAYG_combobox_values.append(user['username'])
    PAYG_combobox = ttk.Combobox(root, values=PAYG_combobox_values, width=25)
    PAYG_combobox.grid(row=8, column=3, columnspan=2, sticky=W)
    PAYG_combobox.bind("<<ComboboxSelected>>", put_payg_data_in_name_field)

    new_username_entry = Entry(root, width=25)
    new_username_entry.grid(row=10, column=1, columnspan=2, sticky=W, padx=5)
    new_username_entry.bind('<KeyRelease>', enable_button)

    new_username_label = Label(root, text='Username', background='#f4f4f4')
    new_username_label.grid(row=9, column=1, padx=5, sticky=W)

    new_password_label = Label(root, text='Password', background='#f4f4f4')
    new_password_label.grid(row=9, column=3, sticky=W)

    new_password_entry = Entry(root, width=25)
    new_password_entry.grid(row=10, column=3, columnspan=2, sticky=W)
    new_password_entry.bind('<KeyRelease>', enable_button)

    new_type_label = Label(root, text='Type', background='#f4f4f4')
    new_type_label.grid(row=9, column=4, sticky=W)

    new_type_combobox = ttk.Combobox(root, width=6, values=['PAYM', 'PAYG'])
    new_type_combobox.grid(row=10, column=5, columnspan=2, sticky=W)
    new_type_combobox.bind("<<ComboboxSelected>>", enable_button)
    new_type_combobox.bind("<KeyRelease>", enable_button)

    add_user_button = Button(root, text='ADD', highlightbackground='#f4f4f4', state=DISABLED, command=add_user_to_db)
    add_user_button.grid(row=11, column=1, sticky=W, padx=5)

    delete_user_button = Button(root, text='DELETE', highlightbackground='#f4f4f4', state=DISABLED, command=delete_user)
    delete_user_button.grid(row=11, column=3, sticky=W)
    root.mainloop()


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=20)
    gui_process = pool.Process(target=run_gui())