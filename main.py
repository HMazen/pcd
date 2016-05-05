import Pyro4

from receiver import Receiver
from sender import Sender


def parse_config():
    ''' parses the configuration file for the main script '''
    config_dict = {}
    infile = None

    # open the configuration file
    try:
        infile = open('file.cfg', 'r')
    except:
        print 'could not open configuration file'
        return

    lines = infile.readlines()

    # handles the case if the file is empty
    if not lines:
        print 'empty configuration file'
        return

    # fills the key/value pairs
    for line in lines:
        l = line.strip().split('=')
        key = l[0].strip()
        value = l[1].strip()
        config_dict[key] = value

    return config_dict


def main():
    # TODO: parse configuration file to retreive
    # sender's and receiver's ip addresses
    config_dict = parse_config()
    if not config_dict:
        print 'no config params'
        return
    sender_name = config_dict['IP'] + '_sender'
    recv_name = config_dict['IP'] + '_receiver'
    print 'sender name: ' + sender_name
    print 'receiver name: ' + recv_name
    s_obj = Sender()
    r_obj = Receiver()
    s_obj.ip_address = config_dict['IP']
    r_obj.ip_address = config_dict['IP']
    s_obj.multicast_address = config_dict['multicast']
    r_obj.multicast_address = config_dict['multicast']
    Pyro4.Daemon.serveSimple(
        {
            s_obj: sender_name,
            r_obj: recv_name
        },
        ns=False,
        port=45000,
        host=config_dict["IP"]
    )


if __name__ == '__main__':
    main()
