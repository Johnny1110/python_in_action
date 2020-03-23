import sys

import jieba

delim = ','

def play():
    sentence = '獨立音樂需要大家一起來推廣，歡迎加入我們的行列！'
    words = jieba.cut(sentence, cut_all=False)
    output = []
    for word in words:
        output.append(word)
    print(delim.join(output))

if __name__ == '__main__':
    play()