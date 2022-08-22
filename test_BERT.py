from sentence_transformers import SentenceTransformer, util
from scipy.spatial.distance import cosine
import numpy as np
import pandas as pd
import jieba
import jieba.analyse
import heapq
import time
import json

# BERT_MODEL = SentenceTransformer('distiluse-base-multilingual-cased')
# BERT_MODEL = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
BERT_MODEL = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')

def softmax(v):
    l1 = list(map(lambda x: np.exp(x), v))
    return list(map(lambda x: x / sum(l1), l1))

def easy_similarity(text1, text2, model=BERT_MODEL):
    vec1 = model.encode(text1)
    vec2 = model.encode(text2)
    # distance = cosine(vec1, vec2)     # 余弦距离
    # similarity = 1 - distance
    similarity2 = util.cos_sim(vec1, vec2)
    return similarity2.tolist()[0][0]

def get_excel(path):
    excel_reader = pd.ExcelFile(path)
    sheet_names = excel_reader.sheet_names
    question =  excel_reader.parse(sheet_name=sheet_names[0])
    keyword = excel_reader.parse(sheet_name=sheet_names[1])
    return question['问题'].tolist(), keyword['关键词'].tolist()


# q1, q2 = '请假', '病假'
# print(easy_similarity(q1, q2))

# 句子匹配
# cur = time.time()
# path = './Q&A_intern.xlsx'
# query = ['餐饮可以报销吗']
# question, _ = get_excel(path)
# query_embedding = BERT_MODEL.encode(query)
# corpus_embeddings = np.load('./question_features.npy')
# hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=10)[0]
# for hit in hits:
#     print(question[hit['corpus_id']], hit['score'])
# print('total time: ', time.time() - cur)

# 单词匹配
# cur = time.time()
# path = './Q&A_intern.xlsx'
# text = ['请假']
# query = BERT_MODEL.encode(text)
# question, keywords = get_excel(path)
# with open('./question_seg_features.json', 'r') as f:
#     corpus = json.load(f)
# # for k in keywords:
# #     jieba.add_word(str(k))
# similarities = []
# for i in range(len(corpus)):
#     # seg = jieba.lcut(corpus[i])
#     # seg_embeddings = BERT_MODEL.encode(seg)
#     seg_embeddings = np.array(corpus[i], dtype=np.float32)
#     score = util.semantic_search(query, seg_embeddings, top_k=1)
#     # print(score)
#     total = 0.0
#     for s in score:
#         total += s[0]['score']
#     # score = score[0][0]['score']
#     similarities.append(total / len(text))
#     # print(i)
# top_k = heapq.nlargest(10, range(len(similarities)), similarities.__getitem__)
# for i in range(10):
#     print(question[top_k[i]], similarities[top_k[i]])
# print('total time: ', time.time() - cur)

# text = '新员工'
# ques = '公司新版考勤制度，请事假的要求有哪些？'
# _, keywords = get_excel('./Q&A_intern.xlsx')
# for k in keywords:
#     jieba.add_word(str(k))
# text = jieba.cut_for_search(text)
# text = ' '.join(text).split()
# query = BERT_MODEL.encode(text)
# seg = jieba.cut_for_search(ques)
# seg = ' '.join(seg).split()
# seg_embeddings = BERT_MODEL.encode(seg)
# print(text)
# print(seg)
# for i in range(len(query)):
#     for j in range(len(seg_embeddings)):
#         print(text[i], seg[j], 1 - cosine(query[i], seg_embeddings[j]))

# content = '公司新版考勤制度，请事假的要求有哪些？'
# tags = jieba.analyse.extract_tags(content, topK=10, withWeight=True)
# print(tags)
# for tag in tags:
#     print("tag: %s\t\t weight: %f" % (tag[0],tag[1]))

cur = time.time()
path = './Q&A_intern.xlsx'
text = '请假'
tag = jieba.analyse.extract_tags(text, topK=20, withWeight=True)
query = BERT_MODEL.encode([tag[i][0] for i in range(len(tag))])
qweight = [tag[i][1] for i in range(len(tag))]
question, keywords = get_excel(path)
with open('./question_key_features.json', 'r') as f:
    corpus = json.load(f)
# for k in keywords:
#     jieba.add_word(str(k))
similarities = []
for i in range(len(corpus)):
    seg_embeddings, seg_weight = corpus[i][0], corpus[i][1]
    score = []
    for q in query:
        qscore = []
        for i in range(len(seg_embeddings)):
            q_seg_score = util.cos_sim(q, seg_embeddings[i]).tolist()[0][0] * seg_weight[i]
            qscore.append(q_seg_score)
        score.append(sum(qscore) / len(qscore))
    similarities.append(sum(score) / len(score))
    # print(i)
top_k = heapq.nlargest(10, range(len(similarities)), similarities.__getitem__)
for i in range(10):
    print(question[top_k[i]], similarities[top_k[i]])
print('total time: ', time.time() - cur)



# path = './Q&A_intern.xlsx'
# corpus, keywords = get_excel(path)
# question_embedding = BERT_MODEL.encode(corpus)
# print(question_embedding.shape)
# np.save('./question_features.npy', question_embedding)

# path = './Q&A_intern.xlsx'
# corpus, keywords = get_excel(path)
# question_seg_features = []
# for i in range(len(corpus)):
#     seg = jieba.cut_for_search(corpus[i])
#     seg = ' '.join(seg).split()
#     seg_embeddings = BERT_MODEL.encode(seg)
#     question_seg_features.append(seg_embeddings.tolist())
# print(len(question_seg_features))
# with open('./question_seg_features.json', 'w') as f:
#     json.dump(question_seg_features, f)


# path = './Q&A_intern.xlsx'
# corpus, keywords = get_excel(path)
# question_key_features = []
# for i in range(len(corpus)):
#     tag = jieba.analyse.extract_tags(corpus[i], topK=20, withWeight=True)
#     seg = [tag[i][0] for i in range(len(tag))]
#     weight = softmax([tag[i][1] for i in range(len(tag))])
#     seg_embeddings = BERT_MODEL.encode(seg)
#     question_key_features.append((seg_embeddings.tolist(), weight))
#     print(seg, weight)
# print(len(question_key_features))
# with open('./question_key_features.json', 'w') as f:
#     json.dump(question_key_features, f)