
import MeCab

tagger = MeCab.Tagger("-Ochasen")
result = tagger.parse("私は東京に住んでいます。")
print(result)
