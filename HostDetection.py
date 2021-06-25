from scapy.all import *
from random import randint
from optparse import OptionParser
from scapy.layers.inet import IP, ICMP


def main():
    parser = OptionParser("Usage:%prog -i <target host> ")

    parser.add_option('-i',type='string',dest='IP',help='specify target host')
    option, args = parser.parse_args()
    print("Scan report for " + option.IP + "\n")
    if '-' in option.IP:
        for i in range(int(option.IP.split('-')[0].split('.')[3]),int(option.IP.split('-')[1])+1):
            # print(i)
            # print(option.IP.split(".")[0]+"."+option.IP.split(".")[1] + "." + option.IP.split(".")[2] + "." + str(i))
            Scan(
                option.IP.split(".")[0]+"."+option.IP.split(".")[1] + "." + option.IP.split(".")[2] + "." + str(i)
            )
            time.sleep(0.2)
    else:
        Scan(option.IP)
    print("\nScan finished!...\n")
def Scan(ip):
    ip_id = randint(1,65535)
    icmp_id = randint(1,65535)
    icmp_seq = randint(1,65535)
    packet = IP(dst=ip,ttl=64,id=ip_id)/ICMP(id=icmp_id,seq=icmp_seq)/b'rootkit'
    result = sr1(packet, timeout=1, verbose=False)

    if result != None:
        # result.display()
        print(ip + '--->' + 'Host is up')
    else:
        print(ip + '--->' + 'host is down')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("interrupted by user, killing all threads...")