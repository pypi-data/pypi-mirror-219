import sys

from optparse import OptionParser
from selis.client import ChatClient


def return_arguments():
    parser = OptionParser()
    parser.add_option("-v", "--version", dest="version", action="store_true", help="show version and exit")
    parser.add_option("-p", "--port", dest="port", help="connect to sever through this port")
    parser.add_option("-n", "--nickname", dest="nickname", help="choose a nickname")
    (options, arguments) = parser.parse_args()

    if options.version:
        print("selis 1.0.0")

        sys.exit()

    return_error(parser, options)
    return options


def return_error(parser, options):
    if not options.port:
        parser.error("\033[91m[-] Port not found\033[0m")


def main():
    options = return_arguments()

    ip = "0.tcp.ap.ngrok.io"
    port = int(options.port)
    nickname = options.nickname

    if nickname:
        pass
    else:
        nickname = input("\033[1m\033[0m[*] Choose a name: \n>> \033[1m")


    try:
        client = ChatClient(ip=ip, port=port, nickname=nickname)
        client.start()
    except KeyboardInterrupt:
        sys.exit()


if __name__ == "__main__":
    main()
