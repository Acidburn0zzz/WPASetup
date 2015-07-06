__author__ = 'ryanvade'
from Tkinter import *
import tkMessageBox
import dbus
import uuid
import os

def path_dbusByteArray(path):
    #Generate a Dbuse ByteArray to be used with ca-cert
    return dbus.ByteArray("file://" + path + "\0")

def WPASETUP():
    user_home = os.getenv("HOME")
    cert_location = user_home + '/.config/SIUE_WPA/ca.crt'
    userUUID = str(uuid.uuid4())

    eid = entryWidget.get()

    s_con = dbus.Dictionary({
        'type': '802-11-wireless',
        'uuid': userUUID,
        'id': 'SIUE-WPA'})

    s_wifi = dbus.Dictionary({
        'ssid': dbus.ByteArray("SIUE-WPA"),
        'security': '802-11-wireless-security'})

    s_wsec = dbus.Dictionary({
        'key-mgmt': 'wpa-eap',
        'auth-alg': 'open'})

    s_8021x = dbus.Dictionary({
        'eap': ['peap'],
        'identity': eid,
        'ca-cert': path_dbusByteArray(cert_location),
        'phase2-auth': 'mschapv2'})

    s_ip4 = dbus.Dictionary({'method': 'auto'})
    s_ip6 = dbus.Dictionary({'method': 'ignore'})

    con = dbus.Dictionary({
        'connection': s_con,
        '802-11-wireless': s_wifi,
        '802-11-wireless-security': s_wsec,
        '802-1x': s_8021x,
        'ipv4': s_ip4,
        'ipv6': s_ip6
        })

    bus = dbus.SystemBus() #dbus connection
    service_name = "org.freedesktop.NetworkManager" #what service in dbus are we using
    proxy = bus.get_object(service_name, "/org/freedesktop/NetworkManager/Settings") #dbus nm settings object
    settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings") #interface for the object

    settings.AddConnection(con) #Finally, the SIUE-WPA NM profile
    tkMessageBox.showinfo(title="Done", message="WPA Setup is Complete")
    root.destroy() #program is done. Exit.

def on_continue_button():

    global entryWidget

    if entryWidget.get().strip() == "":
        tkMessageBox.showerror("Error", "Please enter your EID.")
    else:
        WPASETUP()

if __name__ == "__main__":

    root = Tk()

    root.title("SIUE WPA SETUP TOOL FOR LINUX")
    root["padx"] = 40
    root["pady"] = 20

    # Create a text frame to hold the text Label and the Entry widget
    textFrame = Frame(root)

    #Create a Label to say what the program does
    welcomeLabel = Label(textFrame)
    welcomeLabel["text"] = "Welcome to the SIUE WPA setup tool for Linux!"
    welcomeLabel.pack(side=TOP)

    #Create a Label in textFrame
    entryLabel = Label(textFrame)
    entryLabel["text"] = "Enter your eid:"
    entryLabel.pack(side=LEFT)

    # Create an Entry Widget in textFrame
    entryWidget = Entry(textFrame)
    entryWidget["width"] = 50
    entryWidget.pack(side=LEFT)

    textFrame.pack()

    button = Button(root, text="Submit", command=on_continue_button)
    button.pack()

    root.mainloop()