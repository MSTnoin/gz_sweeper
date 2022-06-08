import os
import sys
import winreg
import re


# stellaris游戏工坊
# D:\Program Files (x86)\Steam\steamapps\workshop\content\281990
# 鸽组汉化的id
gz_dir = "2131014154"

if __name__ == '__main__':
    try:
        # 获取steam根目录
        hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\WOW6432Node\Valve\Steam")
        steam_path = winreg.QueryValueEx(hkey, "InstallPath")
    except:
        print('无法找到Steam目录')
        input("请按回车键退出。")
        sys.exit(0)
        
    # 打开libraryfolders.vdf以寻找玩家steam库
    lib_folders = open(os.path.join(steam_path[0], 'steamapps/libraryfolders.vdf'))

    try:
        # 看某个库里是否有游戏281990
        game_id = '-1'
        for line in lib_folders:
            path_search = re.match('		"path"		"(.*)"', line)
            if path_search:
                lib_path = path_search.group(1)

            game_search = re.match('			"(\d+)"', line)
            if game_search:
                game_id = game_search.group(1)

            if game_id == '281990':
                ste_path = os.path.join(lib_path, 'steamapps/workshop/content/281990')

    except:
        print('无法找到群星创意工坊目录')
        input("请按回车键退出。")
        sys.exit(0)

    os.chdir(ste_path)

    stellaris = r'.'
    mod_names = os.listdir(stellaris)
    if gz_dir in mod_names:
        mod_names.remove(gz_dir)
    else:
        print('本目录下找不到鸽组汉化的2131014154文件夹。')
        input("请按回车键退出。")
        sys.exit(0)
    mod_names = [i for i in mod_names if os.path.isdir(os.path.join(stellaris, i))]

    gz_files = set()
    # 读入鸽组文件
    gz_full_path = os.path.join(stellaris, gz_dir)
    print("鸽组内部的同名文件：")
    for root, dirs, files in os.walk(gz_full_path):
        for file_name in files:
            if not file_name.endswith('l_simp_chinese.yml'):
                continue
            mod_loc_file = (os.path.join(root, file_name))
            if file_name not in gz_files:
                gz_files.add(file_name)
            else:
                print(mod_loc_file)
    print()

    same_name_files = []
    for mod_name in mod_names:
        print("检测" + mod_name + "与鸽组汉化同名的文件：")
        mod_loc_dir = os.path.join(stellaris, mod_name, "localisation")
        if not os.path.exists(mod_loc_dir):
            continue
        for root, dirs, files in os.walk(mod_loc_dir):
            for file in files:
                if file in gz_files:
                    p = (os.path.join(root, file))
                    print(p)
                    same_name_files.append(p)

    if len(same_name_files) > 0:
        confirm = input("是否删除与鸽组汉化同名的其他汉化文件(y/n)？")
        if confirm == 'y':
            for f in same_name_files:
                os.remove(f)
    else:
        print("无同名文件。")
    input("请按回车键退出。")
