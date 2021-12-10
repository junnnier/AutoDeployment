import paramiko


class sftp(object):
    def __init__(self, hostname, port, username, password, try_times):
        while True:
            try:
                tran = paramiko.Transport((hostname, int(port)))
                tran.connect(username=username, password=password)
                self.sftp_client = paramiko.SFTPClient.from_transport(tran)
                print("{} sftp connection success".format(hostname))
                break
            except:
                if try_times > 0:
                    print("{} sftp connection fail, try again.".format(hostname))
                    try_times -= 1
                else:
                    raise Exception("{} sftp connection fail.".format(hostname))

    # 上传
    def put(self,local_file,remote_file):
        try:
            print("[uploading] {} -> {}".format(local_file,remote_file))
            self.sftp_client.put(local_file,remote_file,callback=self.show_percent)
            print("[upload success] {}".format(local_file))
        except:
            print("[upload fail] {}".format(local_file))

    # 显示进度
    def show_percent(self,send,total):
        print(f"Transferred percentage: {send/total*100:.2f}%",end="\r")

    def close(self):
        self.sftp_client.close()
