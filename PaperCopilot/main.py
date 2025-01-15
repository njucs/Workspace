import requests
from bs4 import BeautifulSoup
import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from googlesearch import search
from transformers import pipeline

# 1. 网页爬取
def crawl_paper_list(url):
    response = requests.get(url)
    response.raise_for_status()  # 抛出异常如果请求失败
    soup = BeautifulSoup(response.content, "html.parser")

    # 这里需要根据目标网页的结构进行修改
    paper_elements = soup.find_all("li", class_="paper-item")  # 例如，假设每篇论文在 <li> 标签中，且有 class="paper-item"
    papers = []
    for element in paper_elements:
        title = element.find("h3").text.strip() if element.find("h3") else "Title Not Found"  # 例如，假设标题在 <h3> 标签中
        authors = element.find("span", class_="authors").text.strip() if element.find("span", class_="authors") else "Authors Not Found" # 例如，假设作者在 <span> 标签中，且有 class="authors"
        papers.append({"title": title, "authors": authors})
    return papers

# 2. 文本预处理
def preprocess_text(text):
    text = re.sub(r"[^\w\s]", "", text)  # 去除标点符号
    text = text.lower()
    return text

# 3. 语义相似度计算
def semantic_similarity(query, papers, embedding_model):
    query_embedding = embedding_model.encode(preprocess_text(query))
    filtered_papers = []
    for paper in papers:
        title = paper["title"]
        title_embedding = embedding_model.encode(preprocess_text(title))
        similarity = cosine_similarity(query_embedding.reshape(1, -1), title_embedding.reshape(1, -1))[0][0]
        if similarity > 0.5:  # 相似度阈值，可以根据需要调整
            filtered_papers.append({"title": paper["title"], "authors": paper["authors"], "similarity": similarity})
    return filtered_papers


# 4. 论文内容搜索
def search_paper_content(title):
    search_results = search(title, num_results=3)
    for url in search_results:
      try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        text_content = ' '.join([p.text for p in soup.find_all('p')])
        if text_content:
            return text_content
      except requests.exceptions.RequestException as e:
         print(f"Failed to fetch {url}: {e}")
    return None

# 5. 论文观点归纳
def summarize_paper_content(text, summarizer):
    try:
        summary = summarizer(text, max_length=200, min_length=50)[0]['summary_text'] # 可以调整长度
        return summary
    except:
      return "Summary Failed"


if __name__ == "__main__":
    # 替换成你想要爬取的网页链接
    url = "https://example.com/accepted-papers"
    papers = crawl_paper_list(url)
    print(f"Found {len(papers)} papers.")

    query = "自然语言处理中的语义理解"
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # 使用 Sentence-BERT 模型
    filtered_papers = semantic_similarity(query, papers, embedding_model)
    print(f"Found {len(filtered_papers)} relevant papers.")

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn") # 使用 BART 模型进行摘要

    for paper in filtered_papers:
        print(f"Title: {paper['title']}")
        print(f"Authors: {paper['authors']}")
        paper_content = search_paper_content(paper['title'])
        if paper_content:
            summary = summarize_paper_content(paper_content, summarizer)
            print(f"Summary: {summary}")
        else:
           print("Paper Content Not Found")
        print("-" * 40)