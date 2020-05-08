import asyncio
from analyzer import predict_data

d = {'duration': 0, 'protocol_type': 'tcp', 'service': 'http', 'flag': 'SF', 'src_bytes': 232, 'dst_bytes': 8153, 'urgent': 0, 'hot': 0, 'count': 0, 'srv_count': 0, 'serror_rate': 0, 'srv_serror_rate': 0, 'rerror_rate': 0, 'srv_rerror_rate': 0, 'same_srv_rate': 0, 'diff_srv_rate': 0, 'srv_diff_host_rate': 0, 'dst_host_count': 0, 'dst_host_srv_count': 0, 'dst_host_same_srv_rate': 0, 'dst_host_diff_srv_rate': 0, 'dst_host_same_src_port_rate': 0.0, 'dst_host_srv_diff_host_rate': 0.0, 'dst_host_serror_rate': 0.0, 'dst_host_srv_serror_rate': 0.0, 'dst_host_rerror_rate': 0, 'dst_host_srv_rerror_rate': 0.0}


asyncio.run(predict_data(d))
