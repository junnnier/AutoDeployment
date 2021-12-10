import zipfile
import os
from datetime import datetime


def exec_process(ssh_client,sftp_client,cfg):
    remote_path=cfg.REMOTE_PATH
    local_path=cfg.LOCAL_PATH
    update=cfg.UPDATE
    # 在原项目上更新指定文件或文件夹
    if update:
        for item in update:
            loc_position,rem_position,backup=item.split(";")
            # 文件
            if os.path.isfile(loc_position):
                # 检查本地是否存在
                if os.path.exists(loc_position):
                    # 是否备份原文件
                    if ssh_client.is_exist(rem_position) and int(backup):
                        print("[backup] {}".format(rem_position))
                        pre_name=os.path.dirname(rem_position)
                        temp,suffix=rem_position[len(pre_name):].split(".")
                        temp=temp+datetime.now().strftime("_backup_%Y%m%d_%H%M%S")
                        ssh_client.rename(rem_position,pre_name+temp+"."+suffix)
                    # 上传
                    sftp_client.put(loc_position,rem_position)
                else:
                    raise Exception("file is not exists {}".format(loc_position))
            # 目录
            else:
                # 检查本地是否存在
                if os.path.exists(loc_position):
                    zip_name=zip_file(loc_position)
                    sftp_client.put(zip_name,rem_position+"/"+zip_name)
                    unzip_dir=rem_position+"/"+zip_name.split(".")[0]  # 解压后的目录名
                    # 是否备份原目录
                    if ssh_client.is_exist(unzip_dir) and int(backup):
                        print("[backup] {}".format(unzip_dir))
                        date=datetime.now().strftime("_backup_%Y%m%d_%H%M%S")
                        ssh_client.rename(unzip_dir, unzip_dir+date)
                    # 解压
                    ssh_client.unzip_file(rem_position+"/"+zip_name,rem_position)
                    ssh_client.rm(rem_position+"/"+zip_name)
                    os.remove(zip_name)
                    print("[delete local temporary] {}".format(zip_name))
                else:
                    raise Exception("directory is not exists {}".format(loc_position))

    # 更新整个项目
    else:
        # 本地打包
        zip_name=zip_file(local_path)
        # 上传
        sftp_client.put(zip_name,remote_path+"/"+zip_name)
        # 远端存在项目原文件则备份
        if ssh_client.is_exist(remote_path+"/"+zip_name.split(".")[0]):
            date=datetime.now().strftime("_backup_%Y%m%d_%H%M%S")
            src=remote_path+"/"+zip_name.split(".")[0]
            ssh_client.rename(src,src+date)
        # 远端解压
        ssh_client.unzip_file(remote_path+"/"+zip_name,remote_path)
        # 删除压缩文件
        ssh_client.rm(remote_path+"/"+zip_name)
        # 删除本地打包文件
        os.remove(zip_name)
        print("[delete local temporary] {}".format(zip_name))


# 本地打包
def zip_file(local_path):
    zip_name = local_path.split(os.sep)[-1] + ".zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as f:
        index_len = len(os.path.dirname(local_path))
        for dirpath, dirnames, filenames in os.walk(local_path):
            for filename in filenames:
                pathfile = os.path.join(dirpath, filename)
                arcname = pathfile[index_len:].strip(os.sep)
                f.write(pathfile, arcname)
    return zip_name