import jieba

text1 = '今天哪里都没去，在中信证券总部工作了一天'
jieba.add_word('中信证券总部')
text2 = 'future'
seg_list = jieba.lcut(text1)
print(seg_list)

