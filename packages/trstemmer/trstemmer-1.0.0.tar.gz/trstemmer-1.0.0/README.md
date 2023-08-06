trstemmer is a simple Turkish word stemmer which is still in development (for now, it can only stem verbs and may not be accurate.). You should download Turkish NLP model (`pip install https://huggingface.co/turkish-nlp-suite/tr_core_news_lg/resolve/main/tr_core_news_lg-any-py3-none-any.whl`) before using the library. You can use the library as following:
```
from trstemmer import turkish
stemmer = turkish.stemmer()
result = stemmer.stem("seviyorum, yapmışım, koşarlar, yemişsin")
print(f"Result: {result}")
>>> Result: sev yap koş ye
```
