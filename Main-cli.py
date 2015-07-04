#!/usr/bin/env python2
__author__ = 'ryanvade'

import dbus
import uuid
import os

#for more information: https://wiki.gnome.org/Projects/NetworkManager/Developers

def path_dbusByteArray(path):
    #Generate a Dbuse ByteArray to be used with ca-cert
    return dbus.ByteArray("file://" + path + "\0")

def merge_secrets(proxy, config, setting_name):
    try:
        # returns a dict of dicts mapping name::setting, where setting is a dict
        # mapping key::value.  Each member of the 'setting' dict is a secret
        secrets = proxy.GetSecrets(setting_name)

        # Copy the secrets into our connection config
        for setting in secrets:
            for key in secrets[setting]:
                config[setting_name][key] = secrets[setting][key]
    except Exception, e:
        pass

def dict_to_string(d, indent):
    # Try to trivially translate a dictionary's elements into nice string
    # formatting.
    dstr = ""
    for key in d:
        val = d[key]
        str_val = ""
        add_string = True
        #There are trhee types: dbus Array, dbus Dictionary and just values
        if type(val) == type(dbus.Array([])):
            for elt in val:
                if type(elt) == type(dbus.Byte(1)):
                    str_val += "%s " % int(elt)
                elif type(elt) == type(dbus.String("")):
                    str_val += "%s" % elt
        elif type(val) == type(dbus.Dictionary({})):
            dstr += dict_to_string(val, indent + "    ")
            add_string = False
        else:
            str_val = val
        if add_string:
            dstr += "%s%s: %s\n" % (indent, key, str_val)
    return dstr

def connection_to_string(config):
    # dump a connection configuration to a the console
    for setting_name in config:
        print "        Setting: %s" % setting_name
        print dict_to_string(config[setting_name], "            ")
    print ""


def print_connections(proxy, service_name, settings):
    connection_paths = settings.ListConnections()

    # List each connection's name, UUID, and type
    for path in connection_paths:
        con_proxy = bus.get_object(service_name, path)
        settings_connection = dbus.Interface(con_proxy, "org.freedesktop.NetworkManager.Settings.Connection")
        config = settings_connection.GetSettings()

        merge_secrets(settings_connection, config, '802-11-wireless-security')

        # Get the details of the 'connection' setting
        s_con = config['connection']
        print "    name: %s" % s_con['id']
        print "    uuid: %s" % s_con['uuid']
        print "    type: %s" % s_con['type']
        print "    ------------------------------------------"
        connection_to_string(config)

user_home = os.getenv("HOME")
cert_location = user_home + '/.config/SIUE_WPA/ca.crt'
userUUID = str(uuid.uuid4())

eid = raw_input("Please enter your eid: ")

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

ShowAllConnections = False #Show all of NMs wirelsss connections? For Debugging
bus = dbus.SystemBus() #dbus connection
service_name = "org.freedesktop.NetworkManager" #what service in dbus are we using
proxy = bus.get_object(service_name, "/org/freedesktop/NetworkManager/Settings") #dbus nm settings object
settings = dbus.Interface(proxy, "org.freedesktop.NetworkManager.Settings") #interface for the object

settings.AddConnection(con) #Finally, the SIUE-WPA NM profile

print("NetworkManager configuration file located in /etc/NetworkManager/system-connections/")
print("CA Certificate loacated at " + cert_location)
if ShowAllConnections:
    connection_paths = settings.ListConnections() #all connections
    print("Printing Wireless Connections:")
    print_connections(proxy,service_name, settings)

print("Installation Complete. ")