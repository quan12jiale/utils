import os
import os.path as osp
import shutil

g_dll_srcpath = r"F:\GTJ\build\bin\Win32\RelWithDebInfo"
g_dll_dstpath = r"F:\GTJ\tools\GBCQ\build\bin\Win32\RelWithDebInfo"

def copy_all_file():
    if (not osp.exists(g_dll_srcpath)):
        return
    if (not osp.exists(g_dll_dstpath)):
        return
    for path, dirs, files in os.walk(g_dll_dstpath):
        for d in dirs[:]:
            # 不进入子目录
            dirs.remove(d)
        for f in files:
            src_filename = osp.join(g_dll_srcpath, f)
            if (not osp.exists(src_filename)):
                # 如果GTJ不存在该文件，则continue
                continue
            
            basename = osp.basename(src_filename)
            dst_filename = osp.join(g_dll_dstpath, basename)
            shutil.copyfile(src_filename, dst_filename)
        
def copy_all_libfile():
    g_lib_srcpath = r"F:\GTJ\build\lib\Win32\RelWithDebInfo"
    g_lib_dstpath = r"F:\GTJ\tools\GBCQ\build\lib\Win32\RelWithDebInfo" 
    if (not osp.exists(g_lib_srcpath)):
        return
    if (not osp.exists(g_lib_dstpath)):
        return
    for path, dirs, files in os.walk(g_lib_dstpath):
        for d in dirs[:]:
            # 不进入子目录
            dirs.remove(d)
        for f in files:
            src_filename = osp.join(g_lib_srcpath, f)
            if (not osp.exists(src_filename)):
                # 如果GTJ不存在该文件，则continue
                continue
            
            basename = osp.basename(src_filename)
            dst_filename = osp.join(g_lib_dstpath, basename)
            shutil.copyfile(src_filename, dst_filename)
        
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

def copy_lib(depend_lib_set : set):
    g_lib_srcpath = r"F:\GTJ\build\lib\Win32\RelWithDebInfo"
    g_lib_dstpath = r"F:\GTJ\tools\GBCQ\build\lib\Win32\RelWithDebInfo" 

    depend_lib_set = sorted(depend_lib_set)
    for libname in depend_lib_set:
        lib_srcpath = osp.join(g_lib_srcpath, libname)
        if (not osp.exists(lib_srcpath)):
            #print(libname)
            continue
        
        lib_dstpath = osp.join(g_lib_dstpath, libname)
        if (osp.exists(lib_dstpath)):
            continue
        
        print(lib_srcpath)
        shutil.copyfile(lib_srcpath, lib_dstpath)
        
def copy_GTJCalcExe_depend_dll():
    # 先windeployqt GTJCalcExe.exe 
    dll_list = ['GLDRibbonStyle.dll', 'libeay32.dll', 'ssleay32.dll', 'GP.dll', 
                'FreeImage.dll', 'libfbxsdk.dll', 'assimp-vc140-mt.dll',
                'lib3ds-2_0.dll', 'GCCSCloudService_Zip32.dll',
                'GTTchEntity_19.7src_14.tx', 'ConvertTangentModule.dll',
                'ISM_19.7src_14.tx', 'TD_Alloc_19.7src_14.dll', 'GSolver.dll',
                'TD_Db_19.7src_14.dll', 'TD_DbCore_19.7src_14.dll',
                'TD_DbEntities_19.7src_14.tx', 'TD_DbRoot_19.7src_14.dll',
                'RenderSystemGL.dll', 'RenderSystemAngle.dll', 'TD_Ge_19.7src_14.dll',
                'TD_Gi_19.7src_14.dll', 'TD_Gs_19.7src_14.dll', 'TD_Root_19.7src_14.dll',
                'TD_SpatialIndex_19.7src_14.dll', 'glewctx.dll', 'glew32.dll',
                'GCCSCloudService_Lzma32.dll', 'GCCSCloudService_Common32.dll',
                'FileManagerCache.exe', 'GSPEngine.dll', 'GTJCalcExe.ini',
                'GCPPCalculator.dll', 'GCLCollect.dll', 'libexpat.dll', 
                'libapriconv-1.dll', 'GTJProjectManageService.dll', 'GCLReport.dll', 
                'GGJReport.dll', 'GTJReport.dll', 'GTJCADCmdState.dll', 
                'GTJCloudCheck.dll', 'GMPExtractSDK.dll', 'GTJCADIdentifier.dll', 
                'GMPFeatures.dll', 'GTJCADBeamIdentifier.dll']
    for dllname in dll_list:
        dll_srcpath = osp.join(g_dll_srcpath, dllname)
        if (not osp.exists(dll_srcpath)):
            print(dllname)
            continue
        
        dll_dstpath = osp.join(g_dll_dstpath, dllname)
        if (osp.exists(dll_dstpath)):
            continue
        
        shutil.copyfile(dll_srcpath, dll_dstpath)
    # 然后拷贝所有GDB以及GSP文件
        
if __name__ == "__main__":
    #copy_GTJCalcExe_depend_dll()
    copy_all_libfile()
    