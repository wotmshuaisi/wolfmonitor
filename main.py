from lib.net import get_remote_ip

if __name__ == "__main__":
    for x in get_remote_ip():
        print(x)
