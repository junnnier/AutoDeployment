import paramiko
import os


class ssh(object):
    def __init__(self,hostname, port, username, password, timeout, try_times):
        while True:
            try:
                self.ssh_client = paramiko.SSHClient()
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 接受不再本地know_hosts文件中记录的主机
                self.ssh_client.connect(hostname=hostname, port=port, username=username, password=password, timeout=timeout)
                print("{} ssh connection success".format(hostname))
                break
            except:
                if try_times > 0:
                    print("{} ssh connection fail, try again.".format(hostname))
                    try_times -= 1
                else:
                    raise Exception("{} ssh connection fail.".format(hostname))

    # 是否存在
    def is_exist(self,path):
        pre=os.path.dirname(path)
        name=path.split("/")[-1]
        stdin,stdout,stderr=self.ssh_client.exec_command(f"find {pre} -name {name}")
        if str(stdout.read(),encoding="utf-8"):
            return True
        else:
            return False

    # 重命名
    def rename(self,src,dest):
        stdin,stdout,stderr=self.ssh_client.exec_command(f"mv {src} {dest}")
        err_info=str(stderr.read(), encoding="utf-8")
        if err_info:
            raise Exception("rename fail {} \n{}".format(dest,err_info))
        else:
            print("[rename success] {}".format(dest))

    # 解压
    def unzip_file(self,path,dest_path):
        stdin,stdout,stderr=self.ssh_client.exec_command(f"unzip -o {path} -d {dest_path}")
        err_info=str(stderr.read(), encoding="utf-8")
        if err_info:
            raise Exception("unzip fail {} \n{}".format(path,err_info))
        else:
            print("[unzip success] {}".format(path))

    # 删除
    def rm(self,path):
        if os.path.isfile(path):
            stdin,stdout,stderr=self.ssh_client.exec_command(f"rm -f {path}")
        else:
            stdin,stdout,stderr=self.ssh_client.exec_command(f"rm -rf {path}")
        err_info=str(stderr.read(), encoding="utf-8")
        if err_info:
            raise Exception("delete fail {} \n{}".format(path,err_info))
        else:
            print("[delete success] {}".format(path))

    # 关闭
    def close(self):
        self.ssh_client.close()