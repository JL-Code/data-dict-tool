import os

# https://blog.csdn.net/Cryhelyxx/article/details/45534041
if __name__ == '__main__':
    print(os.environ['HOME'])
    print(os.path.expandvars('$HOME'))
    print(os.path.expanduser('~'))

    """python路径拼接os.path.join()函数完全教程
    https://blog.csdn.net/weixin_37895339/article/details/79185119
    """
    print("1:", os.path.join('aaaa', '/bbbb', 'ccccc.txt'))
    print("2:", os.path.join('/aaaa', '/bbbb', '/ccccc.txt'))
    print("3:", os.path.join('aaaa', './bbb', 'ccccc.txt'))
    print("3:", os.path.join(os.path.expanduser('~'), 'Library/logs', 'app.log'))
