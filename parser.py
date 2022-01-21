import requests, json, string, os
from bs4 import BeautifulSoup

num_pages = int(input())
articles_type = input()
for i in range(1, num_pages + 1):
    url = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020' + '&page' + str(i)
    os.mkdir('Page_' + str(i))
    path = 'Page_' + str(i)
    content = requests.get(url).content
    code = requests.get(url).status_code
    if code != 200:
        print(f'The URL returned {code}!')
        exit()
    else:
        soup = BeautifulSoup(content, 'html.parser')
        news_article_links = soup.find_all('span', {'class': 'c-meta__type'}, text=articles_type)
        for news_article in news_article_links:
            anchor = news_article.find_parent('article').find('a', {'data-track-action': 'view article'})
            url_article = anchor.get('href')
            heading = anchor.get_text()
            content_url = 'https://www.nature.com' + url_article
            retrieve_content = requests.get(content_url).content
            inner_soup = BeautifulSoup(retrieve_content, 'html.parser')
            title = inner_soup.find('title')
            title_text = title.text  # TITLE
            description = inner_soup.find("meta",  {"name":"description"})
            desc_text = description['content']  #DESCRIPTION
            all_div = inner_soup.find('div', class_="c-article-body")
            all_text = all_div.text
            punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
            for ele in title_text:
                if ele in punc:
                    title_text = title_text.replace(ele, "")
            file_name = title_text.replace(" ", "_")
            article_file = open(path + '\\' + file_name + '.txt', 'wb')
            article_file.write(bytes(str(all_text), encoding='utf-8'))
            article_file.close()
        print('Saved all articles.')
