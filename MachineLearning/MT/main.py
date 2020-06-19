import io
import re
import unicodedata

import tensorflow as tf

# 處理 Unicode String，保證相同字串在底層編碼也相同。

def unicode_to_ascii(s):
  return ''.join(c for c in unicodedata.normalize('NFD', s)
      if unicodedata.category(c) != 'Mn')


def preprocess_sentence(w):
  w = unicode_to_ascii(w.lower().strip())

  # 切詞
  # eg: "he is a boy." => "he is a boy ."
  w = re.sub(r"([?.!,¿])", r" \1 ", w)
  w = re.sub(r'[" "]+', " ", w)

  # 除了 (a-z, A-Z, ".", "?", "!", ",") 以外，其他全部變空白
  w = re.sub(r"[^a-zA-Z?.!,¿]+", " ", w)

  w = w.strip()

  # 加入開始與節數標記
  w = '<start> ' + w + ' <end>'
  return w


# 1. Remove the accents
# 2. Clean the sentences
# 3. Return word pairs in the format: [ENGLISH, SPANISH]
def create_dataset(path, num_examples):
  lines = io.open(path, encoding='UTF-8').read().strip().split('\n')

  word_pairs = [[preprocess_sentence(w) for w in l.split('\t')]  for l in lines[:num_examples]]
  # eg: [['<start> go . <end>', '<start> ve . <end>'], ['<start> go . <end>', '<start> vete . <end>']]

  return zip(*word_pairs)

def tokenize(lang):
  lang_tokenizer = tf.keras.preprocessing.text.Tokenizer(
      filters='')
  lang_tokenizer.fit_on_texts(lang)

  tensor = lang_tokenizer.texts_to_sequences(lang)

  tensor = tf.keras.preprocessing.sequence.pad_sequences(tensor,
                                                         padding='post')

  return tensor, lang_tokenizer

if __name__ == '__main__':
    filePath = "D:\\Mike_workshop\\2020\\6月\mtData\\spa.txt"
    en, sp = create_dataset(filePath, None)
    print(en[0], en[-1])
    print(sp[0], sp[-1])
    input_tensor, input_token = tokenize(en)
    print(input_tensor)

