import email
import xlwt
import optparse
import os

def main(filename,dir):
    # sum计数附加文件个数
    sum = 1
    try:
        # 二进制打开文件
        fp = open(filename, 'rb')
        msg = email.message_from_binary_file(fp)
        
        # 将ip和主题保存到excel
        os.chdir(dir)
        workbook = xlwt.Workbook(encoding = 'ascii')
        worksheet = workbook.add_sheet('My Worksheet')
        worksheet.col(0).width = 5500
        worksheet.write(0, 0, 'IP')
        worksheet.write(0, 1, '主题')
        worksheet.write(1, 0, msg['X-Originating-IP'][1:-1])
        worksheet.write(1, 1, msg['Subject'])
        workbook.save('output.xls')
        
        # 循环信件中的每一个mime的数据块
        for part in msg.walk():
            # print(p.get_content_type())
            if part.get_content_maintype() == 'multipart':
                continue
            Annex_name = part.get_filename()
            # 如果附件存在名字及保存附件
            if Annex_name:
                Annex_name = str(sum) + '.' + Annex_name
                fp = open(Annex_name,'wb')
                fp.write(part.get_payload(decode=True))
                sum += 1
    except:
        print("error")

if __name__=="__main__":
    parser = optparse.OptionParser(usage='Get_Eml_Message.py  -f file -m mkdir ')
    parser.add_option(
        '-f',
        '--file',
        dest='file',
        type="string",
        help="target file ")
    parser.add_option(
        '-m',
        '--mkdir',
        dest='dir',
        default=os.getcwd(),
        type="string",
        help='output dir')
    option, args = parser.parse_args()
    main(option.file, option.dir)