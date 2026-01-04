def word_search(doc_list, keyword):
    
    tempList = []
    for i, doc in enumerate(doc_list):
        tokens = doc.split()
        normalized = [token.rstrip(',.').lower() for token in tokens]
        if keyword.lower() in normalized:
            tempList.append(i)
    return tempList

def multi_word_search(doc_list, keywords):
    
    ans = {} # 1. 改为字典
    for s in keywords:
        # 2. 将 word_search 的结果存入字典，对应的键是 s
        ans[s] = word_search(doc_list, s)
    return ans