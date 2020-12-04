import os.path as osp

import copy_dll_lib

g_sln_path = r"F:\GTJ\build\Sln\win32\Dev";

def get_lib_depend_lib_set(path : str, find_lib_set : set, depend_lib_set : set):
    strpath = osp.join(g_sln_path, path)
    strfile = osp.join(strpath, path + ".vcxproj")
    if (not osp.exists(strfile)):
        return
    
    if path in find_lib_set:
        return
    find_lib_set.add(path)
    
    with open(strfile, encoding = "utf-8") as file:
        while True:  
            line = file.readline()  
            if not line:  
                return
            elif "<AdditionalDependencies>" in line and "</AdditionalDependencies>" in line:
                line = line.strip()
                line = line.replace("<AdditionalDependencies>", "")
                line = line.replace("</AdditionalDependencies>", "")
                strlist = line.split(";")
                for string in strlist:
                    if string and string.endswith(".lib"):
                        idx = string.rfind("\\")
                        if idx == -1: # ==-1应该是系统的lib库
                            depend_lib_set.add(string)
                        else:
                            strlib = string[idx+1:]
                            depend_lib_set.add(strlib)
                            get_lib_depend_lib_set(strlib[:-4], find_lib_set, depend_lib_set)
                return

if __name__ == "__main__":
    
    find_lib_set = set()
    depend_lib_set = set()
    get_lib_depend_lib_set("GTJCalcQuantityNoFrm", find_lib_set, depend_lib_set)

    copy_dll_lib.copy_lib(depend_lib_set)
    
    depend_dll_set = set()
    for lib in depend_lib_set:
        dll = lib.replace('.lib', '.dll')
        depend_dll_set.add(dll)
    copy_dll_lib.copy_dll(depend_dll_set)
        