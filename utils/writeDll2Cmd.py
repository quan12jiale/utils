import re
import os
import os.path as osp
import copy

chdir_path = r'C:\Program Files (x86)\Microsoft Visual Studio 14.0\VC\bin'
command_prefix =  '.\dumpbin /dependents '

gtj_dir = osp.dirname(osp.dirname(osp.dirname(osp.dirname(osp.dirname(__file__)))))
external_dir = osp.join(gtj_dir, "external")
relWithDebInfo_dir = osp.join(gtj_dir, r"build\bin\Win32\RelWithDebInfo")

dllpath_prefix = relWithDebInfo_dir.replace('\\','/') + '/'
cmd_path = osp.join(osp.dirname(__file__), "CopyAllReleaseDebug32_GBCQCalcService.cmd")
#cmd_path = r"F:\VisualStudio\NewCalcRuleTool\source\GBCQCopy\CopyAllReleaseDebug32.cmd"

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
                

def writeSingleGMPDll2Cmd(dll : str, dll_set_copy : set, cmd_file):
    dst_dll = osp.join(relWithDebInfo_dir, dll)
    if not osp.exists(dst_dll):
        return
    for path, dirs, files in os.walk(external_dir):
        for f in files:
            if f.lower() == dll.lower():
                src_dll = osp.join(path, dll)
                if (osp.getmtime(src_dll) == osp.getmtime(dst_dll)) and (osp.getsize(src_dll) == osp.getsize(dst_dll)) and ("qt5" not in dll.lower()):
                    path = path[len(external_dir)+1:]
                    write_str = 'Copy /Y "%GMPPath%\{}\{}" "%DestPath%\\"\n'.format(path, dll)
                    cmd_file.write(write_str)
                    print(write_str)
                    dll_set_copy.remove(dll)
                    return
            
def writeSingleGTJDll2Cmd(dll : str, dll_set_copy2 : set, cmd_file):
    for path, dirs, files in os.walk(relWithDebInfo_dir):
        for d in dirs[:]:
            # 不进入子目录
            dirs.remove(d)
        for f in files:
            if f.lower() == dll.lower():
                if "qt5" not in dll.lower():
                    write_str = 'Copy /Y "%GTJPath%\{}" "%DestPath%\\"\n'.format(dll)
                    cmd_file.write(write_str)
                    print(write_str)
                    dll_set_copy2.remove(dll)
                    return

def writeSingleQTDll2Cmd(dll : str, cmd_file):
    if "qt5" in dll.lower():
        write_str = 'Copy /Y "%QtPath%\{}" "%DestPath%\\"\n'.format(dll)
        cmd_file.write(write_str)
        print(write_str)
        return

def getAlreadyExistDllSet(cmdfile_path : str):
    existDllSet = set()
    with open(cmdfile_path, mode='r') as cmd_file:
        line = cmd_file.readline()
        while line:
            matchObj = re.search(r'[^\\]+(\.dll)', line)
            if matchObj and matchObj.group():
                existDllSet.add(matchObj.group())
            line = cmd_file.readline()
        return existDllSet

def writeDll2Cmd(depend_dll_set : set):
    existDllSet = getAlreadyExistDllSet(cmd_path)
    depend_dll_set = depend_dll_set.difference(existDllSet)
    with open(cmd_path, mode='a+') as cmd_file:
        cmd_file.write("\n")
        
        dll_set_copy = copy.deepcopy(depend_dll_set)
        cmd_file.write('echo "--------------------GMP Copy--------------------"\n')
        for dll in depend_dll_set:
            writeSingleGMPDll2Cmd(dll, dll_set_copy, cmd_file)
        cmd_file.write("\n")
        
        dll_set_copy2 = copy.deepcopy(dll_set_copy)
        cmd_file.write('echo "--------------------GTJ Copy--------------------"\n')
        for dll in dll_set_copy:
            writeSingleGTJDll2Cmd(dll, dll_set_copy2, cmd_file)
        cmd_file.write("\n")
        
        cmd_file.write('echo "--------------------Qt Copy--------------------"\n')
        for dll in dll_set_copy2:
            writeSingleQTDll2Cmd(dll, cmd_file)
        cmd_file.write("\n")
        
def copyGGDBExplorer(depend_dll_set : set):
    cmd_path = r"F:\GTJ\tools\GBCQ\source\GBCQCopy\CopyGGDBExplorerDll.bat"
    with open(cmd_path, mode='w') as cmd_file:
        cmd_file.write('@echo off\n')
        cmd_file.write('\n')
        cmd_file.write(r'set QtPath=F:\GTJ\external\qt563\msvc2015')
        cmd_file.write('\n')
        cmd_file.write(r'set GTJPath=F:\GTJ\build\bin\Win32\RelWithDebInfo')
        cmd_file.write('\n')
        cmd_file.write('set DestPath=D:\Glodon\GGDBExplorer\n')
        cmd_file.write('\n')
        cmd_file.write('md "%DestPath%\platforms"\n')
        cmd_file.write('\n')
        for dll in depend_dll_set:
            dst_dll = osp.join(relWithDebInfo_dir, dll)
            if not osp.exists(dst_dll):
                print(dst_dll)
                continue
            write_str = 'Copy /Y "%GTJPath%\{}" "%DestPath%\\"\n'.format(dll)
            cmd_file.write(write_str)
        cmd_file.write('Copy /Y "%GTJPath%\GGDBExplorer2019.exe" "%DestPath%\\"\n')
        cmd_file.write('Copy /Y "%GTJPath%\FileManagerCache.exe" "%DestPath%\\"\n')
        cmd_file.write('Copy /Y "%QtPath%\plugins\platforms\qminimal.dll" "%DestPath%\platforms\\"\n')
        cmd_file.write('Copy /Y "%QtPath%\plugins\platforms\qoffscreen.dll" "%DestPath%\platforms\\"\n')
        cmd_file.write('Copy /Y "%QtPath%\plugins\platforms\qwindows.dll" "%DestPath%\platforms\\"\n')
        cmd_file.write('\n')
        cmd_file.write('pause\n')


if __name__ == "__main__":
    getcwd = os.getcwd()
    print ("当前工作目录为 %s" % getcwd)
    os.chdir(chdir_path)
    print ("修改工作目录为 %s" % os.getcwd())
    
    dll_list = ['GGDBExplorer2019.exe']
    dll_set = set()
    for dllname in dll_list:
        find_dll_set = set()
        depend_dll_set = set()
        get_dll_depend_dll_set(dllname, find_dll_set, depend_dll_set)
        
        dll_set = dll_set.union(depend_dll_set)
        
    os.chdir(getcwd)
    print ("还原工作目录为 %s" % os.getcwd())
    copyGGDBExplorer(dll_set)
    
    #writeDll2Cmd(dll_set)
    