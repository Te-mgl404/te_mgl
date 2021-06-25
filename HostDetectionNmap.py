import nmap
import optparse

def NmapScan(targetIP):
    nm = nmap.PortScanner()
    try:
        result = nm.scan(hosts=targetIP,arguments='-sn -PE')
        state = result['scan'][targetIP]['status']['statr']
        print("[{}] is [{}]".format(targetIP, state))
    except Exception as e:
        pass
if __name__ == "__main__":
    parser = optparse.OptionParser("Usage: python %prog -i ip \n\n""Example : python %prog -i 192.168.1.1[192.168.1.1-100]\n")
    parser.add_option('-i','--ip',dest='targetIP',default="192.168.1.1",type="string",help="target ip address")
    option, args=parser.parse_args()
    if "-" in option.targetIP:
        for i in range(int(option.targetIP.split('-')[2]),int(option.targetIP.split('-')[1])+1):
            NmapScan(option.targetIP.split('.')[0]+'.'+option.targetIP.split(".")[1]+"."+option.targetIP.split(".")[2]+"."+str(i))
    else:NmapScan(option.targetIP)
