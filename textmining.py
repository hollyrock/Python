# -*- coding: utf-8 -*-
import MeCab

fi = open("textmining/original.txt",'r').read()
fo = open("textmining/analyzed.txt",'w')

m = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
keyword = m.parse(fi)

words = []
for row in keyword.split("\n"):
    word = row.split("\t")[0]
    if word == "EOS":
        break
    else:
        pos = row.split("\t")[1].split(",")[0]
    if pos == "名詞":
        words.append(word)
    else:
        pos = row.split("\t")[1].split(",")[0]
    if pos == "形容詞":
        words.append(word)
    else:
        pos = row.split("\t")[1].split(",")[0]
    if pos == "動詞":
        words.append(word)

w =','. join(words)
keywords = w.replace(',',' ')
print(keywords)