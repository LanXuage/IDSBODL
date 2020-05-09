CREATE DATABASE xuange_idsbodl;

\c xuange_idsbodl;

CREATE TABLE users (
   id SERIAL PRIMARY KEY NOT NULL,
   username VARCHAR(45) NOT NULL,
   password VARCHAR(45) NOT NULL,
   email VARCHAR(45) NOT NULL,
   phone VARCHAR(45) NOT NULL
);

CREATE TABLE nids_protocol_types (
   id SERIAL PRIMARY KEY NOT NULL,
   protocol_name VARCHAR(45) NOT NULL
);

CREATE TABLE nids_services (
   id SERIAL PRIMARY KEY NOT NULL,
   service_name VARCHAR(45) NOT NULL
);

CREATE TABLE nids_flags (
   id SERIAL PRIMARY KEY NOT NULL,
   flag_name VARCHAR(45) NOT NULL
);

CREATE TABLE nids_labels (
   id SERIAL PRIMARY KEY NOT NULL,
   label_name VARCHAR(45) NOT NULL
);

CREATE TABLE nids_datas (
   id SERIAL PRIMARY KEY NOT NULL,
   src VARCHAR(45) NOT NULL,
   dst VARCHAR(45) NOT NULL,
   sport INT NOT NULL,
   dport INT NOT NULL,
   fk_nids_protocol_type_id INT REFERENCES nids_protocol_type(id) ON DELETE CASCADE,
   urgent INT NOT NULL,
   hot INT NOT NULL,
   src_bytes BIGINT NOT NULL,
   dst_bytes BIGINT NOT NULL,
   data_number VARCHAR(45) NOT NULL,
   fk_nids_service_id INT REFERENCES nids_service(id) ON DELETE CASCADE,
   fk_nids_flag_id INT REFERENCES nids_flag(id) ON DELETE CASCADE,
   duration INT NOT NULL,
   time TIMESTAMP NOT NULL,
   count INT NOT NULL,
   srv_count INT NOT NULL,
   serror_rate DOUBLE PRECISION NOT NULL,
   rerror_rate DOUBLE PRECISION NOT NULL,
   same_srv_rate DOUBLE PRECISION NOT NULL,
   diff_srv_rate DOUBLE PRECISION NOT NULL,
   srv_serror_rate DOUBLE PRECISION NOT NULL,
   srv_rerror_rate DOUBLE PRECISION NOT NULL,
   srv_diff_host_rate DOUBLE PRECISION NOT NULL,
   dst_host_count INT NOT NULL,
   dst_host_srv_count INT NOT NULL,
   dst_host_same_srv_rate DOUBLE PRECISION NOT NULL,
   dst_host_diff_srv_rate DOUBLE PRECISION NOT NULL,
   dst_host_same_src_port_rate DOUBLE PRECISION NOT NULL,
   dst_host_serror_rate DOUBLE PRECISION NOT NULL,
   dst_host_rerror_rate DOUBLE PRECISION NOT NULL,
   dst_host_srv_diff_host_rate DOUBLE PRECISION NOT NULL,
   dst_host_srv_serror_rate DOUBLE PRECISION NOT NULL,
   dst_host_srv_rerror_rate DOUBLE PRECISION NOT NULL,
   fk_nids_label_id INT REFERENCES nids_label(id) ON DELETE CASCADE,
   capture_date TIMESTAMP NOT NULL
);

INSERT INTO users (username, password, email, phone) VALUES ('xuange', 'xuange', '1456817554@qq.com', '13076481191');

INSERT INTO nids_protocol_types (protocol_name) VALUES ('ICMP'), ('TCP'), ('UDP');

INSERT INTO nids_services (service_name) VALUES ('tcpmux'), ('rje'), ('echo'), ('discard'), ('systat'), ('daytime'), ('netstat'), ('qotd'), ('msgsend'), ('chargen'), ('ftp_d'), ('ftp'), ('ssh'), ('telnet'), ('smtp'), ('rsftp'), ('print'), ('time'), ('rlp'), ('grap'), ('wins'), ('whois'), ('tacacs'), ('dns'), ('rap'), ('mtp'), ('dhcp'), ('dhcp_c'), ('mftp'), ('gopher'), ('finger_p'), ('http'), ('tor'), ('tor_c'), ('kerberos'), ('hostname'), ('iso_tsap'), ('rtelnet'), ('pop'), ('pop3'), ('sun_rpcp'), ('ident'), ('sftp'), ('uucp'), ('sql'), ('nntp'), ('ntp'), ('epmap'), ('netbios_name'), ('netbios_data'), ('netbios_sess'), ('imap4'), ('bftp'), ('sgmp'), ('ssql'), ('dmsp'), ('snmp'), ('snmp_t'), ('printt'), ('bgp'), ('irc'), ('appletalk'), ('quickmailtp'), ('ipx'), ('mpp'), ('imap3'), ('esro'), ('bgmp'), ('novastor'), ('applesat'), ('tsp'), ('immp'), ('rpc2'), ('clearcase'), ('hpopenviewhttps'), ('arnss'), ('aurp'), ('ldap'), ('ups'), ('dchub'), ('dc_c'), ('gpsp'), ('https'), ('snpp'), ('ms_smb'), ('tls'), ('tcpnethaspsrv'), ('dantz'), ('isakm'), ('modbus'), ('comsat'), ('who'), ('syslog'), ('lpdp'), ('talk'), ('ntalk'), ('efs'), ('netwares'), ('timed'), ('rpc'), ('aolirc'), ('netnews'), ('netwall'), ('commerceapp'), ('klogin'), ('kshell'), ('dhcpv6c'), ('dhcpv6s'), ('afp'), ('net_rwho'), ('rtsp'), ('brunhoff'), ('rmonitor'), ('monitor'), ('nntps'), ('smtp_send'), ('filemaker'), ('httprpcem'), ('tunnel'), ('ipp'), ('ldaps'), ('msdp'), ('ldp'), ('dhcpfp'), ('rrp'), ('dtcp'), ('aodv'), ('rdrf'), ('doom'), ('acap'), ('mser'), ('hyperwaveisp'), ('ieeemmsssl'), ('olsr'), ('accessnetwoek'), ('epp'), ('lmp'), ('irisoverbeep'), ('samba'), ('vmware_sc'), ('vmwaressc'), ('nca'), ('frps_d'), ('ftps_c'), ('nas'), ('telnets'), ('imaps'), ('pop3s'), ('nfs'), ('msdcs'), ('nim'), ('nimreg'), ('socks'), ('javarc'), ('phonecc'), ('openvpn'), ('tgp'), ('mom2005'), ('rtgp'), ('msdb'), ('oracledb'), ('mms'), ('cft'), ('ssdp'), ('rtmp'), ('nfss'), ('gnunet'), ('mysql'), ('rdp'), ('mdns'), ('auth'), ('courier'), ('csnet_ns'), ('eco_i'), ('ecr_i'), ('exec'), ('harvest'), ('http_2784'), ('http_8001'), ('link'), ('login'), ('name'), ('nnsp'), ('other'), ('pm_dump'), ('private'), ('red_i'), ('shell'), ('remote_job'), ('supdup'), ('urh_i'), ('uucp_path'), ('X11'), ('Z39_50');

INSERT INTO nids_flags (flag_name) VALUES ('SF'), ('OTH'), ('REJ'), ('RSTO'), ('RSTOS0'), ('RSTR'), ('S0'), ('S1'), ('S2'), ('S3'), ('SH');

INSERT INTO nids_labels (label_name) VALUES ('back'), ('buffer_overflow'), ('ftp_write'), ('guess_passwd'), ('imap'), ('ipsweep'), ('land'), ('loadmodule'), ('multihop'), ('neptune'), ('nmap'), ('normal'), ('perl'), ('phf'), ('pod'), ('portsweep'), ('rootkit'), ('satan'), ('smurf'), ('spy'), ('teardrop'), ('warezclient'), ('warezmaster'); 

