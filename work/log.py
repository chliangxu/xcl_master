import datetime
import os
import sys
import shutil

CACHE_SIZE = 1024
FILE_PATH_SUFFIX = 'log.txt'
g_file_handle = None
g_log_cache = ''
g_is_local = False  # 为False则只print而不保存文件

log_builder = 'none_builder'
log_node = 'none_node'

# arg1 arg2...
g_position_args = []
# -option1 [param1, param2, ...] -option2 [param1, param2, ...] ...
g_optional_args = {}


def _pack_str(args):
    if not args:
        return
    stringfieds = [str(a) for a in args]

    if g_is_local:
        return '[%s] %s \n' % (str(datetime.datetime.now()), ' '.join(stringfieds))
    else:
        return '%s \n' % (' '.join(stringfieds))

def info(*args):
    log_str = _pack_str(args)
    log_str = '[{0}-{1}]{2}'.format(log_builder, log_node, log_str)  # 加一个空格为了与ERROR对齐
    _print_log(log_str)


def _print_log(log_str):
    # test
    # blocks = ('Source/', 'Source\\', 'Apex')
    # for b in blocks:
    #     if 'lua' not in log_str and b in log_str:
    #         return
    # test

    import chardet

    convert_str = None
    if type(log_str) == str:
        convert_str = log_str
    else:
        encoding = chardet.detect(log_str)['encoding']
        try:
            convert_str = log_str.decode(encoding)
        except Exception as e:
            convert_str = _try_print_simple(log_str)

    try:
        print(convert_str)
    except Exception as e:
        print('cannot decode by gbk..')
    sys.stdout.flush()

    global g_log_cache
    size = len(g_log_cache) + len(convert_str)
    if size > CACHE_SIZE:
        _dump_log_and_clean_cache()

    g_log_cache += convert_str
    if len(g_log_cache) > CACHE_SIZE:
        _dump_log_and_clean_cache()


def _try_print_simple(log_str):
    try:
        return _remove_non_alphabet_chars(log_str)
    except Exception as e:
        return "removal doesn't work :("

def _dump_log_and_clean_cache():

    global g_log_cache

    file_handle = _open_file()
    if not file_handle:
        return

    file_handle.write(g_log_cache)
    file_handle.flush()

    g_log_cache = ''


def _remove_non_alphabet_chars(text):
    ret = ''
    for c in text:
        ascii_code = ord(c)
        if 0 <= ascii_code <= 255:
            ret += c
        else:
            ret += '?'

    return ret


def _open_file():
    global g_file_handle
    if g_file_handle:
        return g_file_handle

    folder = os.path.join(__file__, "..", "..", "logs")
    folder = os.path.abspath(folder)
    running_node = parse_arg("-run") or ""

    print("日志目录： ", os.path.abspath(folder))

    if not os.path.exists(folder):
        os.makedirs(folder)

    # 文件过多时保留10个，其余删除
    try:
        remove_log_file(folder)
    except Exception as exc:
        print("[ERROR:] open log is failed. error message: %s" % exc)

    file_path = os.path.join(folder, running_node + '-' + FILE_PATH_SUFFIX)

    # 当执行clear_context时，将目录下的文件备份一下
    if running_node == "clear_context":
        back_folder_name = str(datetime.datetime.now()) + "_backup"
        back_folder_name = back_folder_name.replace(':', '-')
        backup_folder = os.path.join(folder, back_folder_name)
        os.makedirs(backup_folder, exist_ok=True)
        for name in os.listdir(folder):
            temp_path = os.path.join(folder, name)
            if os.path.isfile(temp_path):
                shutil.move(temp_path, os.path.join(backup_folder, name))

    g_file_handle = open(file_path, 'a+', encoding='utf-8')
    return g_file_handle

def parse_arg(name_or_position):
    if type(name_or_position) == int:
        return _get_position_arg(name_or_position)
    elif type(name_or_position) == str:
        arg = g_optional_args.get(name_or_position)
        if arg is None:
            return None
        elif len(arg) == 0:
            return True
        elif len(arg) == 1:
            return arg[0]
        elif len(arg) > 1:
            return arg
        else:
            return None
    else:
        return None

def _get_position_arg(position):
    if position < 0 or position >= len(g_position_args):
        return None
    else:
        return g_position_args[position]

def remove_log_file(path):
    tim = []
    if os.path.isdir(path):
        for im in os.listdir(path):
            new_path = os.path.join(path, im)

            if os.path.exists(new_path) and os.path.isdir(new_path):
                # 加入列表并排序
                tim = time_arr(tim, new_path)

    if len(tim) > 10:
        # 删除是个之外的，小日期在前，所以从前面开始
        for rm_path in tim[:len(tim) - 10]:

            if os.path.exists(rm_path):
                remove_tree(rm_path)
                print("remove file:%s is successful" % rm_path)

def time_arr(arr, path):
    """对严格日期格式的目录或文件名排序"""
    if not arr:
        arr.append(path)
        return arr

    tag = 0
    path_time_int = get_str_time(path)

    for i in arr:
        time_int = get_str_time(i)
        if time_int >= path_time_int:
            arr.insert(tag, path)
            break
        elif path_time_int > time_int and tag + 1 < len(arr):
            tag += 1
            continue
        else:
            arr.append(path)
            break

    return arr

def remove_tree(path):
    if not os.path.exists(path) or not os.path.isdir(path):
        print('try to remove invalid folder: %s' % path)
        return

    # def del_rw(action, name, exc):
    #     os.chmod(name, os.stat.S_IWRITE)
    #     os.remove(name)
    #
    # shutil.rmtree(path, onerror=del_rw)
    import stat

    def on_rm_error(func, path, exc_info):
        # path contains the path of the file that couldn't be removed
        # let's just assume that it's read-only and unlink it.
        os.chmod(path, stat.S_IWRITE)
        os.unlink(path)
        print("remove error path : %s" % path)

    shutil.rmtree(path, onerror=on_rm_error, ignore_errors=True)
    print('removed folder %s' % path)

def get_str_time(path):
    """将文件名或目录名的时间转变为int返回"""
    import re
    res = r"\d+"
    dir_name = os.path.split(path)[-1]
    time_str = dir_name.split(".")[0]
    result_list = re.findall(res, time_str)
    time_str = ""
    for m in result_list:
        time_str += m
    return int(time_str)
