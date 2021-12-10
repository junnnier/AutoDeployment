from .SSH import ssh
from .SFTP import sftp


class linux_client(object):
    # 通过IP, 用户名，密码，超时时间初始化一个远程Linux主机
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.timeout = 10
        self.try_times = 1

    def connect(self):
        ssh_client=ssh(self.hostname, self.port, self.username, self.password, self.timeout, self.try_times)
        sftp_client=sftp(self.hostname, self.port, self.username, self.password, self.try_times)
        return ssh_client,sftp_client




