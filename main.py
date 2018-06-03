#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from lib.net import get_remote_detail
import socket
import base64
import hashlib
import json
import time


def get_headers(data):
    """
    将请求头格式化成字典
    :param data:
    :return:
    """
    header_dict = {}
    data = str(data, encoding='utf-8')

    header, body = data.split('\r\n\r\n', 1)
    header_list = header.split('\r\n')
    for i in range(0, len(header_list)):
        if i == 0:
            if len(header_list[i].split(' ')) == 3:
                header_dict['method'], header_dict['url'], header_dict['protocol'] = header_list[i].split(
                    ' ')
        else:
            k, v = header_list[i].split(':', 1)
            header_dict[k] = v.strip()
    return header_dict


def send_msg(conn, msg_bytes):
    """
    WebSocket服务端向客户端发送消息
    :param conn: 客户端连接到服务器端的socket对象,即： conn,address = socket.accept()
    :param msg_bytes: 向客户端发送的字节
    :return:
    """
    import struct

    token = b"\x81"
    length = len(msg_bytes)
    if length < 126:
        token += struct.pack("B", length)
    elif length <= 0xFFFF:
        token += struct.pack("!BH", 126, length)
    else:
        token += struct.pack("!BQ", 127, length)

    msg = token + msg_bytes
    conn.send(msg)
    return True


def run():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 9999))
    sock.listen(5)

    conn, address = sock.accept()

    while True:
        data = conn.recv(1024)
        if not data:
            break
        headers = get_headers(data)
        response_tpl = "HTTP/1.1 101 Switching Protocols\r\n" \
                    "Upgrade:websocket\r\n" \
                    "Connection:Upgrade\r\n" \
                    "Sec-WebSocket-Accept:%s\r\n" \
                    "WebSocket-Location:ws://%s%s\r\n\r\n"

        value = headers['Sec-WebSocket-Key'] + '258EAFA5-E914-47DA-95CA-C5AB0DC85B11'
        ac = base64.b64encode(hashlib.sha1(value.encode('utf-8')).digest())
        response_str = response_tpl % (
            ac.decode('utf-8'), headers['Host'], headers['url'])
        conn.send(bytes(response_str, encoding='utf-8'))

        while True:
            for item in get_remote_detail():
                json_data1 = item.json_format()
                send_msg(conn, json_data1.encode('utf-8'))
            time.sleep(5)
    sock.close()


if __name__ == '__main__':
    run()
