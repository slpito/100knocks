from Morpheme import Morpheme

def main():
    file_name = 'materials/neko.txt.mecab'
    morph = Morpheme(mecab_file_name=file_name)
    result = morph.read_mecab_file()  # 辞書のリスト

    for d in result:
        if d['pos'] == '動詞':
            print(d['base'])


if __name__ == '__main__':
    main()