#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import io

in_keyword = "AnimValue"
trimDir("/Users/project/core_cpp/")

def isIncludeKeyWord(detailinfo, tmp_keyword):
    #正则表达查询性能较差，先用find函数过滤，因为大部分字符串都不需要走正则查询
    if  -1 != detailinfo.find(tmp_keyword):
        #匹配^tmp_keyword$或^tmp_keyword(非字母数字下划线)(任意字符)
        #或(任意字符)(非字母数字下划线)tmp_keyword$或(任意字符)(非字母数字下划线)tmp_keyword(非字母数字下划线)(任意字符)
        pattern_str='(^'+tmp_keyword+'$)|(^'+tmp_keyword+'(\W+).*)|(.*(\W+)'+tmp_keyword+'$)|(.*(\W+)'+tmp_keyword+'(\W+).*)'
        m = re.match(r''+pattern_str+'', detailinfo)
        if m:
            return 1
    return 0


# 处理文件夹
def trimDir(path):
    print(">> " + path)
    for root, dirs, files in os.walk(path):
        print(files)
        for name in files:
            trimFile(os.path.join(root, name))


STATE_BLOCK_INIT = 0
STATE_BLOCK_BEGIN = 1
STATE_LINE_BEGIN = 2


# 处理文件
def trimFile(path):
    if re.match(r".*?\.(cpp|hpp)$", path):
        print(">> Process: " + path)
    else:
        print(">> Ignore: " + path)
        return

    bak_file = path + ".bak"
    try:
        os.rename(path, bak_file)
    except:
        print(">> Exception: " + bak_file)
        return

    fp_src = open(bak_file)
    fp_dst = open(path, 'w')

    state = STATE_BLOCK_INIT
    queue = ''

    for line in fp_src.readlines():
        # print(line)
        if (state == STATE_BLOCK_INIT):
            if (isIncludeKeyWord(line, in_keyword)):
                # 找到关键字开始行
                for char in line:
                    if char == '{':
                        queue = '{'
                        state = STATE_BLOCK_BEGIN
                        break
                    elif char == ';':
                        state = STATE_LINE_BEGIN
                        break
            if state == STATE_LINE_BEGIN:
                state = STATE_BLOCK_INIT
                continue
        elif state == STATE_BLOCK_BEGIN:
            # 查找代码块结尾
            for char in line:
                if char == '{':
                    queue += '{'
                elif char == '}':
                    if queue[len(queue) - 1] == '{':
                        queue = queue[0:len(queue) - 1]
                    else:
                        print(">> ERROR:" + queue)
                        return
            # for
            # 找到代码块的结尾，下一行重新开始
            if (queue == ''):
                state = STATE_BLOCK_INIT
                continue
        # if/elif

        if state == STATE_BLOCK_INIT:
            fp_dst.write(line)

        # print("state=%d"%(state))
        # print("queue=%s"%(queue))
    # for

    fp_src.close()
    os.remove(bak_file)
    fp_dst.close()
