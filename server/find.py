# -*- coding: utf-8 -*-

import os
import re
from sys import modules

IS_KANJI = re.compile(r'[一ー-龥]+')
IS_ZENKAKU = re.compile(r'[ぁ-んァ-ンヴ一ー-龥]+')
IS_COMMENT = re.compile(r'#\s*[a-zA-Z0-9!-/:-@¥[-`{-~a-z0-9ぁ-んァ-ン一ー-龥]+')
IS_VARIABLE = re.compile(r'[ぁ-んァ-ンヴ一ー-龥]+\s*=\s*')
IS_STRING_S = re.compile(r"[']\s*[a-zA-Z0-9!-&(-/:-@¥[-`{-~a-z0-9ぁ-んァ-ン一ー-龥\s]+\s*[']") #single
IS_STRING_D = re.compile(r'["]\s*[a-zA-Z0-9!#-/:-@¥[-`{-~a-z0-9ぁ-んァ-ン一ー-龥\s]+\s*["]')   #double

def find_ZENKAKU_and_IMPORT(i, line, variable, modules):
    diagnostics = []
    # flag = ''

    # コメント文
    if line.startswith('#'):
        return
    
    # # import文
    # if 'import' in line:
    #     tmp = re.sub('from|import', '', line)
    #     tmp = tmp.split(' ')
    #     for item in tmp:
    #         if item != '':
    #             modules.append(item)
    #     return

    # 文字列
    if '"' in line:
        string = re.finditer(IS_STRING_D, line)
        for s in string:
            s = s.group()
            line = line.replace(s, 'a'*len(s))
    if "'" in line:
        string = re.finditer(IS_STRING_S, line)
        for s in string:
            s = s.group()
            line = line.replace(s, 'a'*len(s))
    
    # 文章途中のコメント文
    if '#' in line:
        # if bool(re.finditer(IS_COMMENT, line)):
        comment = IS_COMMENT.finditer(line)
        for c in comment:
            line = line.replace(c.group(), '')
    
    # 全角変数
    if '=' in line:
        var = IS_VARIABLE.finditer(line)
        for v in var:
            v = v.group().split()
            for item in v:
                variable.append(item)

    # Corgiを使用する自然言語部分            
    matches = IS_ZENKAKU.finditer(line)

    for m in matches:
        if  m.group() not in variable: 
            # if 'pandas' in modules:
            #     flag += 'pandas '  
            # if 'matplotlib' in modules:
            #     flag += 'matplot'
            diagnostics.append({
              'source':'corgi-ide',
              'range':{'start':{'line':i, 'character':m.start()}, 'end':{'line':i, 'character':m.end()}},
              'message': 'Corgiが使えるよ',
              'severity': 3,  # 1~4
            #   'code': flag,
              'data': m.group()
            })

    if diagnostics:
      return diagnostics


if __name__ == "__main__":
    doc = '\nimport pandas as pd\n\nprint("Hello", "World", カンマ区切り)\n\nこれ = 6\nあれ = 7\nこれ + あれ\nどれ = これ + あれ # 足し算\nprint(どれ)\n'
    lines = doc.split('\n')
    modules = []
    variable = []
    for i, line in enumerate(lines):
        d = find_ZENKAKU_and_IMPORT(i, line, variable, modules)
        if d:
            print(d)
    if 'pandas' in modules:
        print(modules)
