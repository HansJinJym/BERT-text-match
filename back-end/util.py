import heapq
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

def get_excel(path):
    excel_reader = pd.ExcelFile(path)
    sheet_names = excel_reader.sheet_names
    question =  excel_reader.parse(sheet_name=sheet_names[0])
    keyword = excel_reader.parse(sheet_name=sheet_names[1])
    return question['问题'].tolist(), keyword['关键词'].tolist()

def tokenize(query):
    path = '../Q&A_intern.xlsx'
    questions, keywords = get_excel(path)
    for k in keywords:
        jieba.add_word(str(k))
    tokens = jieba.cut_for_search(query)
    tokens = ' '.join(tokens).split()
    return tokens, questions

def tokenize_key(query):
    path = '../Q&A_intern.xlsx'
    questions, keywords = get_excel(path)
    for k in keywords:
        jieba.add_word(str(k))
    tags = jieba.analyse.extract_tags(query, topK=20, withWeight=True)
    tokens = [tags[i][0] for i in range(len(tags))]
    weights = [tags[i][1] for i in range(len(tags))]
    # tokens = jieba.cut_for_search(query)
    # tokens = ' '.join(tokens).split()
    return tokens, questions

def search_by_token(query, topk=10):
    tokens, questions = tokenize_key(query)
    print(tokens)
    query = BERT_MODEL.encode(tokens)
    with open('../question_seg_features.json', 'r') as f:
        corpus = json.load(f)
    similarities = []
    for i in range(len(corpus)):
        # seg = jieba.lcut(corpus[i])
        # seg_embeddings = BERT_MODEL.encode(seg)
        seg_embeddings = np.array(corpus[i], dtype=np.float32)
        score = util.semantic_search(query, seg_embeddings, top_k=1)
        # print(score)
        total = 0.0
        for s in score:
            total += s[0]['score']
        # score = score[0][0]['score']
        similarities.append(total / len(tokens))
        # print(i)
    top_k = heapq.nlargest(topk, range(len(similarities)), similarities.__getitem__)
    res = []
    for i in range(topk):
        d = {}
        d['number'] = i + 1
        d['match'] = questions[top_k[i]]
        d['similarity'] = similarities[top_k[i]]
        res.append(d)
    return res