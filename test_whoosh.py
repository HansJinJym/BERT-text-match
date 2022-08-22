import os
import shutil

from whoosh.fields import *
from whoosh.index import create_in
from whoosh.qparser import QueryParser
from jieba.analyse import ChineseAnalyzer


analyzer = ChineseAnalyzer()

schema = Schema(title=TEXT(stored=True),
                path=ID(stored=True),
                content=TEXT(stored=True,
                             analyzer=analyzer))
if not os.path.exists("test"):
    os.mkdir("test")
else:
    # 递归删除目录
    shutil.rmtree("test")
    os.mkdir("test")

idx = create_in("test", schema)
writer = idx.writer()

writer.add_document(
    title=u"document1",
    path="/tmp1",
    content=u"麦迪是一位著名的篮球运动员，他飘逸的打法深深吸引着我")
writer.add_document(
    title=u"document2",
    path="/tmp2",
    content=u"科比是一位著名的篮球运动员，他坚韧的精神深深的感染着我")
writer.add_document(
    title=u"document3",
    path="/tmp3",
    content=u"詹姆斯是我不喜欢的运动员")

writer.commit()
searcher = idx.searcher()
parser = QueryParser("content", schema=idx.schema)

for keyword in ("篮球", "麦迪"):
    print("searched keyword ",keyword)
    query= parser.parse(keyword)
    results = searcher.search(query)
    for hit in results:
        print(hit.highlights("content"))
    print("="*50)