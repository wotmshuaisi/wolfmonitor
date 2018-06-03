import geoip2
from vendor.netstat import netstat_tcp4, netstat_udp4


def get_remote_ip():
    """
    get rmote connection info
    """
    resultList = []
    netList = netstat_tcp4()
    for item in netList:
        if item[4] == "ESTABLISHED" and not item[3].startswith("127.0.0.1"):
            resultList.append(item)
    return resultList
