"""
40. 係り受け解析結果の読み込み（形態素）


neko.txt.cabocha の説明

1行目

    *
    文節番号
    係り先の文節番号(係り先なし:-1)
    主辞の形態素番号/機能語の形態素番号
    係り関係のスコア(大きい方が係りやすい)

2行目

    表層形 （Tab区切り）
    品詞
    品詞細分類1
    品詞細分類2
    品詞細分類3
    活用形
    活用型
    原形
    読み
    発音

"""

import CaboCha
import re
from my_package.Chunk import Chunk
from my_package.Morph import Morph
from my_package.Syntax import Syntax


def exce_cabocha(input_file_name, output_file_name, dict_pass=None):
    """
    入力ファイル(文章ファイル)をCaboChaにかけて出力ファイルに結果を出力
    :param input_file_name: 入力テキストファイル
    :param output_file_name: CaboChaの出力先ファイル
    :param dict_pass: CaboChaの辞書のパス
    :return: なし
    """
    if dict_pass is None:  # 辞書指定なし
        c = CaboCha.Parser()
    else:  # 辞書指定あり
        c = CaboCha.Parser('-d ' + dict_pass)

    with open(input_file_name, mode='r', encoding='utf-8') as input_file, \
            open(output_file_name, mode='w', encoding='utf-8') as output_file:
        for line in input_file:
            parsered = c.parse(line.rstrip())
            output_file.write(parsered.toString(CaboCha.FORMAT_LATTICE))


def read_cabocha_file(cabocha_file_name):
    """
    CaboChaのファイルを読み込む
    :param cabocha_file_name: CaboChaのファイル
    :return: 読み込んだ結果(文のオブジェクト(sytaxクラス)のリスト)
    """
    with open(cabocha_file_name, mode='r', encoding='utf-8') as caboacha_file:
        morph_flag = False  # Chunkオブジェクトを生成するか否か(初回の文節表現のときのケア)
        syntax_structure = []  # 文の集まり(syntaxのリスト)
        chunks = []  # 文節の集まり
        for line in caboacha_file:
            line = line.rstrip()
            if line[0] == '*':  # 1文字目が'*'なら文節表現の行
                if morph_flag is True:  # 文節(Chunk)オブジェクトを生成
                    chunk = Chunk(morphs=morphs, chunk_index=chunk_index,
                                  dst=dst)  # 文節オブジェクト作成
                    chunks.append(chunk)  # 文節の集合に追加
                # 文節(Chunk)オブジェクトのパラメータを更新
                chunk_data = re.split(r' ', line)  # スペースで区切る
                chunk_index = chunk_data[1]  # 文節番号
                dst = chunk_data[2].replace('D', '')  # 係り先の文節番号
                morphs = []  # 形態素のリストを準備 + 空にして仕切り直し
                morph_flag = False
            elif line == 'EOS':  # 1つの文(syntax)が終わる
                # 1文が1文節のみの場合のケア
                if morph_flag is True:  # 文節(Chunk)オブジェクトを生成
                    chunk = Chunk(morphs=morphs, chunk_index=chunk_index,
                                  dst=dst)  # 文節オブジェクト作成
                    chunks.append(chunk)  # 文節の集合に追加

                syntax = Syntax(chunks)  # 1つの文(Syntax)のオブジェクトを生成
                syntax_structure.append(syntax)  # 文の集合に追加
                chunks = []  # 文節の集合を空にして仕切り直し
                morph_flag = False
            else:  # 形態素表現の行
                morph_data = re.split(r'[,\t]', line)  # カンマ、タブで区切る
                s = morph_data[0]  # 0: 表層形(surface)
                b = morph_data[7]  # 6: 基本形
                p = morph_data[1]  # 1: 品詞
                p1 = morph_data[2]  # 2: 品詞細分類1
                morph = Morph(surface=s, base=b, pos=p, pos1=p1)  # 形態素オブジェクト作成
                morphs.append(morph)  # 形態素のリストに追加
                morph_flag = True
    return syntax_structure


def main():
    cabocha_dict_pass = '/var/lib/mecab/dic/ipadic-utf8'  # ipa辞書選択
    input_file_name = 'materials/neko.txt'
    output_file_name = 'materials/neko.txt.cabocha'
    # exce_cabocha(input_file_name, output_file_name, cabocha_dict_pass)
    syntax_structure = read_cabocha_file(output_file_name)
    print(syntax_structure[2].surface(), end='\n'+'-----'+'\n'*2)
    for chunk in syntax_structure[2].chunks:
        for morph in chunk.morphs:
            morph.output()


if __name__ == '__main__':
    main()
