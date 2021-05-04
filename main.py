from tkinter import *
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import csv
import time
import random
import traceback

global client
global y, lavelll, canvas
global phone1
global code_input_from_telegram
global from_groups, group_s, to_group, dict1
global adding_from, adding_to
global take_members_from, add_members_to, adding_members_to_save
global users, frame_labels
global file_name_from, file_name_to


def tkinter_label(yazi, n):
    global y, lavelll
    print("1")
    lavelll = Label(canvas, text=yazi, width=60, height=4, bg="red", borderwidth=2, relief="groove", compound=RIGHT)
    lavelll.grid(row=n, column=0)
    print("2")
    canvas.create_window(0, y, window=lavelll, anchor=NW)
    print("3")
    scrollbar = Scrollbar(canvas, orient=VERTICAL, command=canvas.yview)
    scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
    canvas.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, y))
    print("tkinter label ()")
    print(yazi)


def starting():
    global y
    # text = "Text "
    # for a in range(200):
    #     print("start")
    #     text2= text + str(a)
    #     tkinter_label(text2, a)
    #     y += 60
    #     print(f"a = {a}")
    #     time.sleep(5)
    # print("starting")
    mode = 2
    n = 0
    for user in users:
        n += 1
        print(n)
        if n % 50 == 0:
            time.sleep(900)
        try:
            print("Adding {}".format(user['id']))

            if mode == 1:
                print("mod 1")
                if user['username'] == "":
                    continue
                user_to_add = client.get_input_entity(user['username'])
            elif mode == 2:
                print("mod 2")
                # defining user id as a
                a = user["id"]
                user_to_add = InputPeerUser(user['id'], user['access_hash'])
            else:
                print("mod 3'")
                sys.exit("Invalid Mode Selected. Please Try Again.")
            client(InviteToChannelRequest(adding_members_to_save, [user_to_add]))
            seconds = random.randrange(60, 180)
            text = "adding " + str(a) + " to " + str(adding_members_to_save.title) + " and waiting " + str(
                seconds) + " seconds"
            tkinter_label(text, n)
            y += 60
            time.sleep(seconds)
        except PeerFloodError:
            print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
        except UserPrivacyRestrictedError:
            print("The user's privacy settings do not allow you to do this. Skipping.")
        except:
            traceback.print_exc()
            print("Unexpected Error")
            continue


def check_member_and_add():
    global users
    users = []
    with open(f"members from {take_members_from}.csv", 'r', encoding='utf8') as t1, open(
            f"members to {add_members_to}.csv", 'r', encoding='utf8') as t2:
        fileone = t1.readlines()
        filetwo = t2.readlines()

    with open('update.csv', 'w', encoding='utf8') as outFile:
        for line in fileone:
            if line not in filetwo:
                outFile.write(line)
    users = []
    with open("update.csv", encoding='UTF-8') as f:
        rows = csv.reader(f, delimiter=",", lineterminator="\n")
        next(rows, None)
        for row in rows:
            user = {}
            user['username'] = row[0]
            user['id'] = int(row[1])
            user['access_hash'] = int(row[2])
            user['name'] = row[3]
            users.append(user)
    print("USERS list created")
    starting()


def start_adding():
    print("1.1")
    global take_members_from, add_members_to, file_name_from, file_name_to, adding_members_to_save
    take_members_from = adding_from.get()
    print(f"adding members from: {take_members_from}")
    add_members_to = adding_to.get()
    print(f"adding members to: {add_members_to}")
    index_from = dict1[take_members_from]
    index_to = dict1[add_members_to]
    taking_members_from_save = group_s[index_from]
    adding_members_to_save = group_s[index_to]
    file_name_from = take_members_from
    file_name_to = add_members_to
    all_participants_from = client.get_participants(taking_members_from_save, aggressive=True)
    all_participants_to = client.get_participants(adding_members_to_save, aggressive=True)
    with open(f"members from {take_members_from}.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'name', 'group'])
        print("downloading from")
        for user in all_participants_from:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            name = (first_name + ' ' + last_name).strip()

            writer.writerow([username, user.id, user.access_hash, name, taking_members_from_save.title])
        print("downloading from finished")

    with open(f"members to {add_members_to}.csv", "w", encoding='UTF-8') as f:
        writer = csv.writer(f, delimiter=",", lineterminator="\n")
        writer.writerow(['username', 'user id', 'access hash', 'name', 'group'])
        print("downloading to")
        for user in all_participants_to:
            if user.username:
                username = user.username
            else:
                username = ""
            if user.first_name:
                first_name = user.first_name
            else:
                first_name = ""
            if user.last_name:
                last_name = user.last_name
            else:
                last_name = ""
            name = (first_name + ' ' + last_name).strip()
            writer.writerow([username, user.id, user.access_hash, name, taking_members_from_save.title])
        print("downloading to finished")
    check_member_and_add()


def dropdown_menu():
    global adding_from, adding_to, frame_labels, y, canvas
    y = 0
    frame_dropdown = Frame(root, bd=2, bg="Blue", width=300, height=200)
    frame_dropdown.pack(pady=10)
    frame_dropdown1 = Frame(frame_dropdown)
    frame_dropdown1.grid(row=0, column=0, padx=5, pady=5)
    frame_dropdown2 = Frame(frame_dropdown)
    frame_dropdown2.grid(row=0, column=2, padx=5, pady=5)
    adding_from = StringVar()
    adding_from.set("From Group")
    adding_to = StringVar()
    adding_to.set("To Group")
    drop1 = OptionMenu(frame_dropdown1, adding_from, *from_groups)
    drop1.pack()
    drop2 = OptionMenu(frame_dropdown2, adding_to, *from_groups)
    drop2.pack()
    frame_labels = Frame(root, bd=2, bg="Blue", width=300, height=400)
    # frame_labels.update()
    frame_labels.pack(pady=10)
    canvas = Canvas(frame_labels, bg="Blue", width=root.winfo_width(), height=root.winfo_height())
    canvas.pack()
    select_button = Button(frame_dropdown, text="start adding", command=start_adding)
    select_button.grid(row=1, column=1)


def get_chats():
    global from_groups, group_s, to_group, dict1
    chats = []
    last_date = None
    chunk_size = 200
    group_s = []
    from_groups = []
    to_group = []
    list_len = []
    result = client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=chunk_size,
        hash=0
    ))
    chats.extend(result.chats)
    for chat in chats:
        try:
            if chat.megagroup:
                group_s.append(chat)
        except:
            continue
    i = 0
    for group in group_s:
        a = (str(i) + '- ' + group.title[:15])
        from_groups.append(a)
        list_len.append(i)
        i += 1
    for c in from_groups:
        dict1 = {from_groups[c]: list_len[c] for c in range(0, len(group_s), 1)}
    print("get chat finished")
    dropdown_menu()


def connect():
    client.sign_in(phone1, code_input_from_telegram.get())
    get_chats()


def update():
    global client, phone1, code_input_from_telegram
    api_id = api_key.get()
    api_hash = secret_key.get()
    phone1 = phone.get()
    client = TelegramClient(phone1, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone1)
        frame3 = Frame(root, bd=2, bg="blue", width=300, height=200)
        frame3.pack(pady=10)
        frame3_text_label = Frame(frame3, bg="red")
        frame3_text_label.grid(row=0, column=0)
        frame3_input = Frame(frame3, bg="blue")
        frame3_input.grid(row=0, column=1)
        code_from_telegram = Label(frame3_text_label, text="Enter Code", bg="red")
        code_from_telegram.grid(row=0, column=0)
        code_input_from_telegram = Entry(frame3_input, width=30)
        code_input_from_telegram.grid(row=0, column=1)
        enter_code = Button(root, text="connect", fg="red", command=connect)
        enter_code.pack(pady=10)
    else:
        get_chats()


root = Tk()
root.title("Telegram Adder")
root.iconbitmap("source/yang.ico")
root.geometry("500x700+150+80")

frame = Frame(root, bd=3, bg="blue", width=300, height=400)
frame.pack(pady=10)
frame1 = Frame(frame, bg="red")
frame1.grid(row=0, column=0)
frame2 = Frame(frame, bg="blue")
frame2.grid(row=0, column=1)

# creating text labels
api_key_label = Label(frame1, text="Api ID", bg="red")
api_key_label.grid(row=0, column=0)
secret_key_label = Label(frame1, text="Api Hash", bg="red")
secret_key_label.grid(row=1, column=0)
phone_label = Label(frame1, text="Phone", bg="red")
phone_label.grid(row=2, column=0)

# create text boxes
api_key = Entry(frame2, width=30)
# api_key.insert(END, '3779290')
api_key.grid(row=0, column=1, padx=20)
secret_key = Entry(frame2, width=30)
# secret_key.insert(END, '8ffe3d2a28f35e337efb7c93b8a8cefd')
secret_key.grid(row=1, column=1)
phone = Entry(frame2, width=30)
# phone.insert(END, '+46700546553')
phone.grid(row=2, column=1)

redbutton = Button(root, text="Start", fg="red", command=update)
redbutton.pack(pady=20)

root.mainloop()
