#!/bin/env python3
# -*- coding: utf-8 -*-
# -*- author: 14568 -*-
# -*- create_time: 2020/4/14 22:21
import os
import time
import json

import numpy
import tensorflow as tf
import pandas as pd
import numpy as np


LOG_DIR = './logs'
CHECKPOINT_PATH = './checkpoint/{epoch:02d}-{val_loss:.2f}.ckpt'

T = str(int(time.time()))

CALLBACKS = [
    tf.keras.callbacks.TensorBoard(log_dir=LOG_DIR, histogram_freq=1),
    tf.keras.callbacks.ModelCheckpoint(filepath=CHECKPOINT_PATH, save_weights_only=True, verbose=1, period=5),
]

SERVICES = {'tcpmux': 0, 'rje': 1, 'echo': 2, 'discard': 3, 'systat': 4, 'daytime': 5, 'netstat': 6, 'qotd': 7, 'msgsend': 8, 'chargen': 9, 'ftp_d': 10, 'ftp': 11, 'ssh': 12, 'telnet': 13, 'smtp': 72, 'rsftp': 15, 'print': 16, 'time': 17, 'rlp': 18, 'grap': 19, 'wins': 20, 'whois': 21, 'tacacs': 22, 'dns': 23, 'rap': 24, 'mtp': 25, 'dhcp': 26, 'dhcp_c': 27, 'mftp': 28, 'gopher': 29, 'finger_p': 30, 'http': 31, 'tor': 32, 'tor_c': 33, 'kerberos': 86, 'hostname': 35, 'iso_tsap': 36, 'rtelnet': 37, 'pop': 38, 'pop3': 39, 'sun_rpcp': 40, 'ident': 41, 'sftp': 42, 'uucp': 105, 'sql': 44, 'nntp': 45, 'ntp': 46, 'epmap': 47, 'netbios_name': 48, 'netbios_data': 49, 'netbios_sess': 50, 'imap4': 51, 'bftp': 52, 'sgmp': 53, 'ssql': 54, 'dmsp': 55, 'snmp': 56, 'snmp_t': 57, 'printt': 58, 'bgp': 59, 'irc': 60, 'appletalk': 61, 'quickmailtp': 62, 'ipx': 63, 'mpp': 64, 'imap3': 65, 'esro': 66, 'bgmp': 67, 'novastor': 68, 'applesat': 69, 'tsp': 70, 'immp': 71, 'rpc2': 73, 'clearcase': 74, 'hpopenviewhttps': 75, 'arnss': 76, 'aurp': 77, 'ldap': 78, 'ups': 79, 'dchub': 80, 'dc_c': 81, 'gpsp': 82, 'https': 83, 'snpp': 84, 'ms_smb': 85, 'tls': 87, 'tcpnethaspsrv': 88, 'dantz': 89, 'isakm': 90, 'modbus': 91, 'comsat': 92, 'who': 93, 'syslog': 94, 'lpdp': 95, 'talk': 96, 'ntalk': 97, 'efs': 98, 'netwares': 99, 'timed': 100, 'rpc': 101, 'aolirc': 102, 'netnews': 103, 'netwall': 104, 'commerceapp': 106, 'klogin': 107, 'kshell': 108, 'dhcpv6c': 109, 'dhcpv6s': 110, 'afp': 111, 'net_rwho': 112, 'rtsp': 113, 'brunhoff': 114, 'rmonitor': 115, 'monitor': 116, 'nntps': 117, 'smtp_send': 118, 'filemaker': 119, 'httprpcem': 120, 'tunnel': 121, 'ipp': 122, 'ldaps': 123, 'msdp': 124, 'ldp': 125, 'dhcpfp': 126, 'rrp': 127, 'dtcp': 128, 'aodv': 129, 'rdrf': 130, 'doom': 131, 'acap': 132, 'mser': 133, 'hyperwaveisp': 134, 'ieeemmsssl': 135, 'olsr': 136, 'accessnetwoek': 137, 'epp': 138, 'lmp': 139, 'irisoverbeep': 140, 'samba': 141, 'vmware_sc': 142, 'vmwaressc': 143, 'nca': 144, 'frps_d': 145, 'ftps_c': 146, 'nas': 147, 'telnets': 148, 'imaps': 149, 'pop3s': 150, 'nfs': 151, 'msdcs': 152, 'nim': 153, 'nimreg': 154, 'socks': 155, 'javarc': 156, 'phonecc': 157, 'openvpn': 158, 'tgp': 159, 'mom2005': 160, 'rtgp': 161, 'msdb': 162, 'oracledb': 163, 'mms': 164, 'cft': 165, 'ssdp': 166, 'rtmp': 167, 'nfss': 168, 'gnunet': 169, 'mysql': 170, 'rdp': 171, 'mdns': 172, 'auth': 173, 'courier': 174, 'csnet_ns': 175, 'eco_i': 176, 'ecr_i': 177, 'exec': 178, 'harvest': 179, 'http_2784': 180, 'http_8001': 181, 'link': 182, 'login': 183, 'name': 184, 'nnsp': 185, 'other': 186, 'pm_dump': 187, 'private': 188, 'red_i': 189, 'shell': 190, 'remote_job': 191, 'supdup': 192, 'urh_i': 193, 'uucp_path': 194, 'X11': 195, 'Z39_50': 196}
s = {'aol': 102, 'ctf': 165, 'domain': 23, 'domain_u': 172, 'finger': 30, 'ftp_data': 10, 'hostnames': 35,
     'http_443': 83, 'IRC': 60, 'netbios_dgm': 49, 'netbios_ns': 48, 'netbios_ssn': 50, 'ntp_u': 117, 'pop_2': 38,
     'pop_3': 39, 'printer': 16, 'sunrpc': 40, 'sql_net': 44, 'tftp_u': 28, 'tim_i': 100, 'urp_i': 77, 'vmnet': 142}
SERVICES.update(s)
FLAGS = {'SF': 0, 'OTH': 1, 'REJ': 2, 'RSTO': 3, 'RSTOS0': 4, 'RSTR': 5, 'S0': 6, 'S1': 7, 'S2': 8, 'S3': 9, 'SH': 10}
PROTOCOLS = {'icmp': 0, 'tcp': 1, 'udp': 2}
MAXS = {'urgent': 14, 'hot': 101, 'duration': 58329, 'dst_bytes': 1309937401, 'src_bytes': 1379963888, 'count': 511, 'srv_count': 511, 'dst_host_count': 255, 'dst_host_srv_count': 255}


def prepare_data(train_file):
    df_train = pd.read_csv(train_file)
    df_train['protocol_type'] = df_train['protocol_type'].map(PROTOCOLS)/len(PROTOCOLS)
    df_train['service'] = df_train['service'].map(SERVICES)/len(SERVICES)
    df_train['flag'] = df_train['flag'].map(FLAGS)/len(FLAGS)
    df_train.pop('land')
    df_train.pop('wrong_fragment')
    df_train.pop('num_failed_logins')
    df_train.pop('logged_in')
    df_train.pop('num_compromised')
    df_train.pop('root_shell')
    df_train.pop('su_attempted')
    df_train.pop('num_root')
    df_train.pop('num_file_creations')
    df_train.pop('num_shells')
    df_train.pop('num_access_files')
    df_train.pop('num_outbound_cmds')
    df_train.pop('is_host_login')
    df_train.pop('is_guest_login')
    df_train.pop('level')
    labels_train = df_train.pop('labels')
    y_train = pd.get_dummies(labels_train)
    with open('../model/' + T + '.labels', 'w') as f:
        f.write(json.dumps(list(y_train.columns.values)))
    y_train = y_train.to_numpy()
    for i in MAXS:
        df_train[i] = df_train[i]/MAXS[i]
    print(sorted(df_train.columns.values))
    df_train = df_train[sorted(df_train.columns.values)]
    print(df_train.columns.values)
    x_train = df_train.to_numpy()
    x_test = x_train[-1000:]
    y_test = y_train[-1000:]
    return (x_train, y_train), (x_test, y_test)


def lstm_data(x_train, y_train, x_test, y_test, time_stamp):
    new_x_train = []
    new_y_train = []
    new_x_test = []
    new_y_test = []
    for i in range(time_stamp, len(x_train)):
        new_x_train.append(x_train[i - time_stamp:i])
        new_y_train.append(y_train[i - 1])
    for i in range(time_stamp, len(x_test)):
        new_x_test.append(x_test[i - time_stamp:i])
        new_y_test.append(y_test[i - 1])
    return (numpy.array(new_x_train), numpy.array(new_y_train)), (numpy.array(new_x_test), numpy.array(new_y_test))


def train():
    (x_train, y_train), (x_test, y_test) = prepare_data('dataSet/KDDTrain+.txt')
    #
    # # MLP Model
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(120, input_dim=27, activation='relu'))
    model.add(tf.keras.layers.Dense(40, activation='relu'))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(23, activation='softmax'))
    model.summary()
    model.compile(optimizer=tf.keras.optimizers.Adam(0.003), loss='categorical_crossentropy', metrics='accuracy')
    train_history = model.fit(x=x_train, y=y_train, batch_size=100, validation_split=0.2,
                              callbacks=CALLBACKS, epochs=20)

    # LSTM Model
    # model = tf.keras.Sequential()
    # (x_train, y_train), (x_test, y_test) = lstm_data(x_train, y_train, x_test, y_test, 16)
    # model.add(tf.keras.layers.LSTM(120, return_sequences=True, input_shape=(16, 41), dropout=0.2))
    # model.add(tf.keras.layers.LSTM(40, dropout=0.2))
    # model.add(tf.keras.layers.Dense(23, activation='softmax'))
    # model.summary()
    # model.compile(optimizer=tf.keras.optimizers.Adam(0.003), loss='categorical_crossentropy',
    #               metrics='accuracy')
    # train_history = model.fit(x=x_train, y=y_train, batch_size=100, validation_split=0.2,
    #                           callbacks=CALLBACKS, epochs=20)

    # GRU
    # model = tf.keras.Sequential()
    # (x_train, y_train), (x_test, y_test) = lstm_data(x_train, y_train, x_test, y_test, 16)
    # model.add(tf.keras.layers.GRU(120, return_sequences=True, input_shape=(16, 41)))
    # model.add(tf.keras.layers.GRU(40, dropout=0.3))
    # model.add(tf.keras.layers.Dense(23, activation='softmax'))
    # model.summary()
    # model.compile(optimizer=tf.keras.optimizers.Adam(0.003), loss='categorical_crossentropy',
    #               metrics='accuracy')
    # train_history = model.fit(x=x_train, y=y_train, batch_size=100, validation_split=0.2,
    #                           callbacks=CALLBACKS, epochs=20)

    # BLSTM
    # model = tf.keras.Sequential()
    # (x_train, y_train), (x_test, y_test) = lstm_data(x_train, y_train, x_test, y_test, 16)
    # model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(120, return_sequences=True), input_shape=(16, 41)))
    # model.add(tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(40, dropout=0.6)))
    # model.add(tf.keras.layers.Dense(23, activation='softmax'))
    # model.summary()
    # model.compile(optimizer=tf.keras.optimizers.Adam(0.003), loss='categorical_crossentropy',
    #               metrics='accuracy')
    # train_history = model.fit(x=x_train, y=y_train, batch_size=100, validation_split=0.2,
    #                           callbacks=CALLBACKS, epochs=20)

    # BGRU
    # model = tf.keras.Sequential()
    # (x_train, y_train), (x_test, y_test) = lstm_data(x_train, y_train, x_test, y_test, 16)
    # model.add(tf.keras.layers.Bidirectional(tf.keras.layers.GRU(120, return_sequences=True), input_shape=(16, 41)))
    # model.add(tf.keras.layers.Bidirectional(tf.keras.layers.GRU(40, dropout=0.6)))
    # model.add(tf.keras.layers.Dense(23, activation='softmax'))
    # model.summary()
    # model.compile(optimizer=tf.keras.optimizers.Adam(0.003), loss='categorical_crossentropy',
    #               metrics='accuracy')
    # train_history = model.fit(x=x_train, y=y_train, batch_size=100, validation_split=0.2,
    #                           callbacks=CALLBACKS, epochs=20)

    # LSTM+MLP
    # model = tf.keras.Sequential()
    # (x_train, y_train), (x_test, y_test) = lstm_data(x_train, y_train, x_test, y_test, 16)
    # model.add(tf.keras.layers.LSTM(120, input_shape=(16, 41)))
    # model.add(tf.keras.layers.Dense(40, activation='relu'))
    # model.add(tf.keras.layers.Dropout(0.2))
    # model.add(tf.keras.layers.Dense(23, activation='softmax'))
    # model.summary()
    # model.compile(optimizer=tf.keras.optimizers.Adam(0.003), loss='categorical_crossentropy',
    #               metrics='accuracy')
    # train_history = model.fit(x=x_train, y=y_train, batch_size=100, validation_split=0.2,
    #                           callbacks=CALLBACKS, epochs=20)
    # model.evaluate(x_test, y_test)
    # model.load_weights()
    # with open(t + '.json', 'w') as f:
    #     f.write(model.to_json())
    # model.set_weights(t + '.ckpt')
    # pre_y = model.predict()
    # with open('1588166701.json', 'r') as f:
    #     ms = f.read()
    # model = tf.keras.models.model_from_json(ms)
    # latest = tf.train.latest_checkpoint(os.path.dirname(CHECKPOINT_PATH))
    # print(latest)
    # print(model.load_weights(latest))
    # model.summary()
    model.save('../model/' + T + '.h5')
    # model = tf.keras.models.load_model('../model/1588171584.h5')
    # model.summary()
    # model.evaluate(x_test, y_test)


if __name__ == '__main__':
    train()



