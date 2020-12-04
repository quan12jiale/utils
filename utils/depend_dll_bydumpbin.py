import os
import os.path as osp
import shutil

chdir_path = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin'
command_prefix =  '.\dumpbin /dependents '
dllpath_prefix = 'F:/GTJ/build/bin/Win32/RelWithDebInfo/'

def get_dll_depend_dll_set(dllname : str, find_dll_set : set, depend_dll_set : set):
    dllpath = dllpath_prefix +  dllname
    if (not osp.exists(dllpath)):
        return
    
    if dllname in find_dll_set:
        return
    find_dll_set.add(dllname)
    
    command = command_prefix + '"' + dllpath + '"'
    output = os.popen(command)
    info = output.readlines()
    cnt = 1
    for line in info: 
        line = line.strip()
        if line:
            if line.endswith('.dll'):
                if dllname.lower().endswith('.dll') and cnt == 1:
                    cnt = 2
                    continue
                depend_dll_set.add(line)
                get_dll_depend_dll_set(line, find_dll_set, depend_dll_set)

g_dll_srcpath = r"F:\GTJ\build\bin\Win32\RelWithDebInfo"
g_dll_dstpath = r"F:\GTJ\tools\GBCQ\build\bin\Win32\RelWithDebInfo"
def copy_dll(depend_dll_set : set):    
    depend_dll_set = sorted(depend_dll_set)
    for dllname in depend_dll_set:
        dll_srcpath = osp.join(g_dll_srcpath, dllname)
        if (not osp.exists(dll_srcpath)):
            print(dllname)
            continue
        
        dll_dstpath = osp.join(g_dll_dstpath, dllname)
        if (osp.exists(dll_dstpath)):
            continue
        
        shutil.copyfile(dll_srcpath, dll_dstpath)

if __name__ == "__main__":
    # 查看当前工作目录
    getcwd = os.getcwd()
    print ("当前工作目录为 %s" % getcwd)
    # 修改当前工作目录
    os.chdir(chdir_path)
    print ("修改工作目录为 %s" % os.getcwd())
    
    find_dll_set = set()
    depend_dll_set5 = set()
    get_dll_depend_dll_set('GBCQCalcService.exe', find_dll_set, depend_dll_set5)
    
    # copy_dll(depend_dll_set)
    
    # find_dll_set.clear()
    # depend_dll_set.clear()
    # get_dll_depend_dll_set('GCLCollect.dll', find_dll_set, depend_dll_set)
    
    # copy_dll(depend_dll_set)
    
    # 修改为之前工作目录
    os.chdir(getcwd)
    print ("还原工作目录为 %s" % os.getcwd())
