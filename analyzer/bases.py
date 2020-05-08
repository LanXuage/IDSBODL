#!/usr/bin/env python
#coding:utf-8
import datetime

from sqlalchemy import Column, String, Integer, BigInteger, DateTime, Text
from sqlalchemy.dialects.postgresql import DOUBLE_PRECISION
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Users(Base):
    def __init__(self):
        super.__init__(self)
    
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(45))
    password = Column(String(45))
    email = Column(String(45))
    phone = Column(String(45))

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'email': self.email,
            'phone': self.phone
        }


class Nids_protocol_type(Base):
    def __init__(self):
        super.__init__(self)
    
    __tablename__ = 'nids_protocol_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    protocol_name = Column(String(45))

    def to_dict(self):
        return {
            'id': self.id,
            'protocol_name': self.protocol_name,
        }
    

class Nids_service(Base):
    def __init__(self):
        super.__init__(self)
    
    __tablename__ = 'nids_service'

    id = Column(Integer, primary_key=True, autoincrement=True)
    service_name = Column(String(45))

    def to_dict(self):
        return {
            'id': self.id,
            'service_name': self.service_name,
        }


class Nids_flag(Base):
    def __init__(self):
        super.__init__(self)
    
    __tablename__ = 'nids_flag'

    id = Column(Integer, primary_key=True, autoincrement=True)
    flag_name = Column(String(45))

    def to_dict(self):
        return {
            'id': self.id,
            'flag_name': self.flag_name,
        }


class Nids_label(Base):
    def __init__(self):
        super.__init__(self)
    
    __tablename__ = 'nids_label'

    id = Column(Integer, primary_key=True, autoincrement=True)
    label_name = Column(String(45))

    def to_dict(self):
        return {
            'id': self.id,
            'label_name': self.label_name,
        }


class Nids_data(Base):
    def __init__(self, **entries):
        self.__dict__.update(entries)

    # Tablename
    __tablename__ = 'nids_data'


    # Table structure
    id = Column(Integer, primary_key=True, autoincrement=True)
    src = Column(String(45))
    dst = Column(String(45))
    sport = Column(Integer)
    dport = Column(Integer)
    fk_nids_protocol_type_id = Column(Integer)
    urgent = Column(Integer)
    hot = Column(Integer)
    src_bytes = Column(BigInteger)
    dst_bytes = Column(BigInteger)
    data_number = Column(String(45))
    fk_nids_service_id = Column(Integer)
    fk_nids_flag_id = Column(Integer)
    duration = Column(Integer)
    time = Column(DateTime)
    count = Column(Integer)
    srv_count = Column(Integer)
    serror_rate = Column(DOUBLE_PRECISION)
    rerror_rate = Column(DOUBLE_PRECISION)
    same_srv_rate = Column(DOUBLE_PRECISION)
    diff_srv_rate = Column(DOUBLE_PRECISION)
    srv_serror_rate = Column(DOUBLE_PRECISION)
    srv_rerror_rate = Column(DOUBLE_PRECISION)
    srv_diff_host_rate = Column(DOUBLE_PRECISION)
    dst_host_count = Column(Integer)
    dst_host_srv_count = Column(Integer)
    dst_host_same_srv_rate = Column(DOUBLE_PRECISION)
    dst_host_diff_srv_rate = Column(DOUBLE_PRECISION)
    dst_host_same_src_port_rate = Column(DOUBLE_PRECISION)
    dst_host_serror_rate = Column(DOUBLE_PRECISION)
    dst_host_rerror_rate = Column(DOUBLE_PRECISION)
    dst_host_srv_diff_host_rate = Column(DOUBLE_PRECISION)
    dst_host_srv_serror_rate = Column(DOUBLE_PRECISION)
    dst_host_srv_rerror_rate = Column(DOUBLE_PRECISION)
    fk_nids_label_id = Column(Integer)
    capture_date = Column(DateTime, default=datetime.datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'src': self.src,
            'dst': self.dst,
            'sport': self.sport,
            'dport': self.dport,
            'fk_nids_protocol_type_id': self.fk_nids_protocol_type_id,
            'urgent': self.urgent,
            'hot': self.hot,
            'src_bytes': self.src_bytes,
            'dst_bytes': self.dst_bytes,
            'data_number': self.data_number,
            'fk_nids_service_id': self.fk_nids_service_id,
            'fk_nids_flag_id': self.fk_nids_flag_id,
            'duration': self.duration,
            'time': self.time,
            'count': self.count,
            'srv_count': self.srv_count,
            'serror_rate': self.serror_rate,
            'rerror_rate': self.rerror_rate,
            'same_srv_rate': self.same_srv_rate,
            'diff_srv_rate': self.diff_srv_rate,
            'srv_serror_rate': self.srv_serror_rate,
            'srv_rerror_rate': self.srv_rerror_rate,
            'srv_diff_host_rate': self.srv_diff_host_rate,
            'dst_host_count': self.dst_host_count,
            'dst_host_srv_count': self.dst_host_srv_count,
            'dst_host_same_srv_rate': self.dst_host_same_srv_rate,
            'dst_host_diff_srv_rate': self.dst_host_diff_srv_rate,
            'dst_host_same_src_port_rate': self.dst_host_same_src_port_rate,
            'dst_host_serror_rate': self.dst_host_serror_rate,
            'dst_host_rerror_rate': self.dst_host_rerror_rate,
            'dst_host_srv_diff_host_rate': self.dst_host_srv_diff_host_rate,
            'dst_host_srv_serror_rate': self.dst_host_srv_serror_rate,
            'dst_host_srv_rerror_rate': self.dst_host_srv_rerror_rate,
            'fk_nids_label_id': self.fk_nids_label_id,
            'capture_date': self.capture_date
        }


