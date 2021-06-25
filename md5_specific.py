import hashlib
import random
import sys
from colorama import init

# 初始化颜色
init(autoreset=True)

# MD5加密
def md5encode(chars):
    return hashlib.md5(chars).hexdigest()

# 获取随机数字
def generate():
    return str(random.randint(1,10000000000000000))

# 主函数循环尝试得到字符串
def specific_char(c):
    start = c
    while True:
        strs = bytes(generate(), encoding="utf8")
        # print(strs)
        # print(md5encode(strs))
        if md5encode(strs).startswith(start):
            print("\033[0;32mThis string is: \033[0m"+str(strs)[2:-1])
            print("\033[0;32mThe md5 value of this string is: \033[0m"+md5encode(strs))
            break
        
if __name__ == '__main__':
    # 参数获取
    if len(sys.argv) == 2:
        specific_md5 = sys.argv[1]
    else:
        print("\033[0;31mExample: %s 6d0bc1\033[0m" % sys.argv[0])
        sys.exit(-1)
    # 执行主函数
    specific_char(specific_md5)
