import argparse
from yacs.config import CfgNode as CN
import os
from utils.Client import linux_client
from utils.Process import exec_process

# 读取配置文件
def get_config(args):
    file_path=os.sep.join([os.getcwd(),"config",args.name+".yaml"])
    if os.path.exists(file_path):
        with open(file_path,"r",encoding="utf-8") as f:
            cfg=CN.load_cfg(f)
        return cfg
    else:
        raise Exception("Config file is not exist {}".format(file_path))

# 获取参数
def get_args():
    parser=argparse.ArgumentParser()
    parser.add_argument("-n","--name",type=str,help="file name of config file.")
    args=parser.parse_args()
    return args

# 开始部署
def auto_start():
    # 读取参数
    args=get_args()
    if args.name:
        # 读取配置文件
        cfg=get_config(args)
        # 远程电脑对象
        computer=linux_client(hostname=cfg.HOST.IP,port=cfg.HOST.PORT,username=cfg.HOST.USERNAME,password=cfg.HOST.PASSWORD)
        # 连接
        ssh_client,sftp_client=computer.connect()
        # 处理
        exec_process(ssh_client,sftp_client,cfg)
        # 关闭连接
        ssh_client.close()
        sftp_client.close()
    else:
        print("Please set the --name parameter")
    print("end")


if __name__ == '__main__':
    auto_start()