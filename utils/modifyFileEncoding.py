import os.path as osp
import os

def fun(directory : str, sOldEncode : str, sNewEncode : str):
    if not osp.exists(directory):
        return
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = osp.join(root, file)
            a, ext = osp.splitext(path)
            if (ext == '.h' or ext == '.cpp'):
                try:
                    with open(path, mode='r', encoding=sOldEncode) as f:
                        data = f.read()
                    with open(path, mode='w', encoding=sNewEncode) as f:
                        f.write(data)
                except:
                    print(path)

if __name__ == '__main__':
    directory = r"F:\cmake-examples\02-sub-projects\musicplayer"
    
    # 将文件编码从utf-8改为utf-8 with BOM
    fun(directory, 'utf-8', 'utf-8-sig')
    
    # 将文件编码从gbk改为utf-8
    #fun(directory, 'gbk', 'utf-8')