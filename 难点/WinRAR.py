
import os
import platform

def copy_tree(from_path, to_path, include_extensions=tuple(), exclude_extensions=tuple(), replace=False, exclude_names=tuple()):
    '''
    shutil的copytree不支持merge两个文件夹，只能自己写个了
    :param from_path:
    :param to_path:
    :param include_extensions: 指定了之后就只复制对应后缀名的文件
    :param exclude_extensions: 指定了之后将跳过对应后缀名的文件
    :param replace: 是否全部覆盖
    :param exclude_names: 忽略的文件名（带后缀）
    :return:
    '''
    if not os.path.isdir(from_path):
        return

    # windows下尝试使用robocopy
    sysstr = platform.system()
    if sysstr == "Windows":
        from scripts.base.utils import common_utils
        log.info("[Robocopy] start to copy from: %s, to: %s" % (from_path, to_path))

        ignore_folders = [n for n in exclude_names]
        ignore_exts = ['*' + n for n in exclude_extensions]
        ignore_exts += exclude_names
        include_exts = ['*' + n for n in include_extensions]

        extra_args = ''
        for i in ignore_folders:
            extra_args += ' /XD ' + i
        for i in ignore_exts:
            extra_args += ' /XF ' + i
        for i in include_exts:
            extra_args += " /IF " + i

        # 完全同步
        if replace:
            extra_args += " /purge"

        cmd = 'robocopy %s %s /S /Z /MT:32 /v /np %s' % (from_path, to_path, extra_args)
        return common_utils.call_cmd(cmd)

    # 覆盖
    if replace and os.path.exists(to_path):
        if os.path.islink(to_path):
            os.remove(to_path)
        else:
            remove_tree(to_path)

    if not os.path.exists(to_path):
        os.makedirs(to_path)

    # 后缀不区分大小写
    lower_include_exts = _convert_to_lowercase_list(include_extensions)
    lower_exclude_exts = _convert_to_lowercase_list(exclude_extensions)

    names = os.listdir(from_path)

    # 特殊处理目标文件夹不存在的情况
    if not os.path.exists(to_path):
        os.makedirs(to_path)

    for n in names:
        if n in exclude_names:
            continue

        fullname_from = os.path.join(from_path, n)
        fullname_to = os.path.join(to_path, n)
        if os.path.isfile(fullname_from):
            if _check_file_extension(n, lower_include_exts, lower_exclude_exts):
                make_file_writable(fullname_to)
                shutil.copy2(fullname_from, fullname_to)
        else:
            if not os.path.exists(fullname_to):
                os.makedirs(fullname_to)
            # 递归处理子文件夹
            copy_tree(fullname_from, fullname_to,
                      lower_include_exts, lower_exclude_exts)