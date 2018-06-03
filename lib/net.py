import json
import geoip2
from functools import reduce
from config import config
from lib.geoip import GeoIPClient
from vendor.netstat import netstat_tcp4, netstat_udp4

"""
{
    'countrycode': 'China',
    'country': 'CN',
    'longitude': 120.1614,
    'latitude': 30.2936
    'city': 'Hangzhou',
    'dport': '80',
    'zerg': 'rush',
    'countrycode2': 'Singapore',
    'country2': 'SG',
    'city2': 'Singapore',
    'longitude2': 103.8565,
    'latitude2': 1.2854999999999999,
    'md5': '223.5.5.5',
    'type': 'ipviking.honey',
}
"""


class Location:
    country = ""
    countrycode = ""
    city = ""
    longitude = 0.0
    latitude = 0.0
    country2 = ""
    countrycode2 = ""
    city2 = ""
    dport = ""
    longitude2 = 0.0
    latitude2 = 0.0
    md5 = ""
    t = "ipviking.honey"
    zerg = "rush"

    def __init__(self, *args, **kwargs):
        self.country = kwargs["country"]
        self.countrycode = kwargs["countrycode"]
        self.city = kwargs["city"]
        self.longitude = kwargs["longitude"]
        self.latitude = kwargs["latitude"]
        self.country2 = kwargs["country2"]
        self.countrycode2 = kwargs["countrycode2"]
        self.city2 = kwargs["city2"]
        self.longitude2 = kwargs["longitude2"]
        self.latitude2 = kwargs["latitude2"]
        self.dport = kwargs["dport"]
        self.md5 = kwargs["ip"]

    def json_format(self):
        temp_dict = {
            "country": self.country,
            "countrycode": self.country2,
            "city": self.city,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "country2": self.country2,
            "countrycode2": self.countrycode2,
            "city2": self.city2,
            "longitude2": self.longitude2,
            "latitude2": self.latitude2,
            "md5": self.md5,
            "dport": self.dport,
            "type": self.t,
            "zerg": self.zerg
        }
        return json.dumps(temp_dict)


def ip_into_int(ip):
    # 先把 192.168.1.13 变成16进制的 c0.a8.01.0d ，再去了“.”后转成10进制的 3232235789 即可。
    # (((((192 * 256) + 168) * 256) + 1) * 256) + 13
    return reduce(lambda x, y: (x << 8) + y, map(int, ip.split('.')))


def is_internal_ip(ip):
    ip = ip_into_int(ip)
    net_a = ip_into_int('10.255.255.255') >> 24
    net_b = ip_into_int('172.31.255.255') >> 20
    net_c = ip_into_int('192.168.255.255') >> 16
    return ip >> 24 == net_a or ip >> 20 == net_b or ip >> 16 == net_c


def get_remote_detail():
    """
    get rmote connection info
    """
    resultList = []
    netList = netstat_tcp4()
    for item in netList:
        if item[4] != "ESTABLISHED" and item[3].startswith("127.0.0.1"):
            continue
        temp_ip = item[3].split(":")[0]
        if is_internal_ip(temp_ip):
            continue
        temp_port = item[2].split(":")[1]
        temp_dict = {
            "country": None,
            "countrycode": None,
            "city": None,
            "longitude": None,
            "latitude": None,
            "country2": None,
            "countrycode2": None,
            "city2": None,
            "longitude2": None,
            "latitude2": None,
            "ip": temp_ip,
            "dport": temp_port
        }
        geohandler = GeoIPClient()
        # target
        geohandler.ip_addr = temp_ip
        try:
            temp_dict["country2"] = geohandler.get_country()
            temp_dict["countrycode2"] = geohandler.get_country_code()
            temp_dict["city2"] = geohandler.get_city_name()
            l1, l2 = geohandler.get_location()
            temp_dict["latitude2"] = l1
            temp_dict["longitude2"] = l2
            # source
            geohandler.ip_addr = config.SERVER_IP
            temp_dict["country"] = geohandler.get_country()
            temp_dict["countrycode"] = geohandler.get_country_code()
            temp_dict["city"] = geohandler.get_city_name()
            l1, l2 = geohandler.get_location()
            temp_dict["latitude"] = l1
            temp_dict["longitude"] = l2
            # location object
            l_obj = Location(**temp_dict)
            resultList.append(l_obj)
        except geoip2.errors.AddressNotFoundError:
            continue
    return resultList
