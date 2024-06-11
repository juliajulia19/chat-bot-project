import requests as rq
from bs4 import BeautifulSoup
import pandas as pd
import re
import spacy
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, wordpunct_tokenize
#spacy.cli.download('ru_core_news_sm')

stop_words = stopwords.words('russian')


#парсинг новостей общей тематики
url = "https://www.mk.ru/news/2024/6/9/"
page = rq.get(url)
soup = BeautifulSoup(page.text, features="html.parser")

news_title = soup.find_all('h3', {'class' : 'news-listing__item-title'})
text_title = [i.text for i in news_title]


links = []
for i in soup.find_all('a', {'class' : 'news-listing__item-link'}):
      links.append(i.get('href'))


def GetNewsBody(url):
  page = rq.get(url)
  soup = BeautifulSoup(page.text, features="html.parser")
  body_text = []
  for item in soup.find_all('div', {'class': 'article__body'}):
        for i in item.find_all('p'):
            body_text.append(i.text.strip())

  return ' '.join(body_text)

news_body = []
for link in links:
    new = GetNewsBody(link)
    news_body.append(new)


for i in news_body:
    i = i.replace('\xa0', ' ')


# print(news_body)
#
news_df = pd.DataFrame({'link': links, 'title': text_title, 'text': news_body})
# news_df.to_csv('newsMK_df.csv')
# print(news_df)

nlp_rus = spacy.load("ru_core_news_sm")
#сделаем отдельный столбец с очищенным и лемматизированным текстом
def preprocess(text):
    tokenized = word_tokenize(text) 
    text_clean = []
    for word in tokenized:
        if word[0].isalnum() and word not in stop_words:
            text_clean.append(word)
    doc = nlp_rus(' '.join(text_clean)) #передаем в spacy и лемматизируем
    lemmas = []
    for token in doc:
        lemmas.append(token.lemma_)
    return ' '.join(lemmas)

news_df['text_lemmas'] = news_df['text'].apply(preprocess)

#выделение именнованных сущностей для каждой статьи

ents = [] #список списков для всех NER по статьям
for i in news_df['text_lemmas']:
    doc = nlp_rus(i)
    article_ents = [] #список для NER одной статьи
    for ent in doc.ents:
        article_ents.append((ent.text, ent.label_))
    ents.append(article_ents)

#можно позже слепить именованную сущность и лейбл

news_df['NER'] = ents #добавляем колонку с NER в датафрейм
news_df.to_csv('newsMK_df.csv')








# #парсинг новостей экономика за неделю, не получилось - спарсились и другие новости со страницы
# all_pages = ['https://www.mk.ru/economics/2024/6/3/', 'https://www.mk.ru/economics/2024/6/4/', 'https://www.mk.ru/economics/2024/6/5/', 'https://www.mk.ru/economics/2024/6/6/', 'https://www.mk.ru/economics/2024/6/7/', 'https://www.mk.ru/economics/2024/6/8/', 'https://www.mk.ru/economics/2024/6/9/']
#
# def GetNews(url):
#   page = rq.get(url)
#   soup = BeautifulSoup(page.text, features="html.parser")
#   title_econ = []
#   for art in soup.find_all('article', {'class': 'article-preview'}):
#         for a in art.find_all('a', {'class': 'article-preview__content'}):
#             for i in a.find_all('h3', {'class': 'article-preview__title'}):
#                 title_econ.append(i.text)
#             preview_econ = []
#             for i in a.find_all('p', {'class': 'article-preview__desc'}):
#                 preview_econ.append(i.text)
#             links_econ = []
#             for i in a.find_all('a', {'class': 'article-preview__content'}):
#                  links.append(i.get('href'))
#
#       return title_econ, preview_econ, links_econ
#
# news_econ = [] # список с новостями по экономике
# for link in all_pages:
#         new = GetNews(link)
#         news_econ.append(new)
#
# print(news_econ)
