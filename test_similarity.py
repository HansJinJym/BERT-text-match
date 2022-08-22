import jieba                  # jieba分词
import difflib                # 方法一：Python自带标准库计算相似度的方法，可直接用
from fuzzywuzzy import fuzz   # 方法二：Python自带标准库计算相似度的方法，可直接用
import numpy as np
from collections import Counter

# 方法三：编辑距离，又称Levenshtein距离
def edit_similar(str1, str2):   # str1，str2是分词后的标签列表
    len_str1 = len(str1)
    len_str2 = len(str2)
    taglist = np.zeros((len_str1+1, len_str2+1))
    for a in range(len_str1):
        taglist[a][0] = a
    for a in range(len_str2):
        taglist[0][a] = a
    for i in range(1, len_str1+1):
        for j in range(1, len_str2+1):
            if(str1[i - 1] == str2[j - 1]):
                temp = 0
            else:
                temp = 1
            taglist[i][j] = min(taglist[i - 1][j - 1] + temp, taglist[i][j - 1] + 1, taglist[i - 1][j] + 1)
    return 1-taglist[len_str1][len_str2] / max(len_str1, len_str2)

# 方法四：余弦相似度
def cos_sim(str1, str2):        # str1，str2是分词后的标签列表
    co_str1 = (Counter(str1))
    co_str2 = (Counter(str2))
    p_str1 = []
    p_str2 = []
    for temp in set(str1 + str2):
        p_str1.append(co_str1[temp])
        p_str2.append(co_str2[temp])
    p_str1 = np.array(p_str1)
    p_str2 = np.array(p_str2)
    return p_str1.dot(p_str2) / (np.sqrt(p_str1.dot(p_str1)) * np.sqrt(p_str2.dot(p_str2)))
 
# 举例说明
str1 = "餐饮"
str2 = "宴请”"
str11 = jieba.lcut(str1)
str22 = jieba.lcut(str2)
print('str1=' + str1)     # jieba分词后
print('str2=' + str2)     # jieba分词后
diff_result = difflib.SequenceMatcher(None, str1, str2).ratio()
print('方法一：Python标准库difflib的计算分值：' + str(diff_result))
print('方法二：Python标准库fuzz的计算分值：' + str(fuzz.ratio(str1, str2)/100))
print('方法三：编辑距离的计算分值：' + str(edit_similar(str11, str22)))
print('方法四：余弦相似度的计算分值：' + str(cos_sim(str11, str22)))
