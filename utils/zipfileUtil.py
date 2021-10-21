import zipfile, os

def zipDir(dirpath, zipfilename):
    zip = zipfile.ZipFile(zipfilename, "w", zipfile.ZIP_DEFLATED)
    for path, dirnames, filenames in os.walk(dirpath):

        # 去掉根路径，只对文件进行压缩
        fpath = path.replace(dirpath,"")
        for filename in filenames:
            zip.write(os.path.join(path, filename), os.path.join(fpath, filename))
        zip.close()
        print("压缩成功")

if __name__ == '__main__':
    zipDir(r"C:\Users\zhang.sun\APItest\utils\excelUtil.py",r"C:\Users\zhang.sun\APItest\utils\excelUtil.zip")