from bs4 import BeautifulSoup

def parse_articles(html):
    soup = BeautifulSoup(html, 'html.parser')
    articles = []
    article_blocks = soup.find_all('article', class_='tm-article-snippet')
    
    if not article_blocks:
        article_blocks = soup.find_all('div', class_='tm-article-snippet')
    
    if not article_blocks:
        title_elements = soup.find_all('h2', class_='tm-title')
        for title_elem in title_elements[:5]:
            title_link = title_elem.find('a')
            if title_link:
                title_text = title_link.get_text(strip=True)
                articles.append({
                    'title': title_text,
                    'index': len(articles) + 1
                })
    else:
        for idx, article in enumerate(article_blocks[:5], 1):
            title_elem = article.find('h2', class_='tm-title')
            if not title_elem:
                title_elem = article.find('h2') or article.find('h1')
            
            if title_elem:
                link = title_elem.find('a')
                if link:
                    title_text = link.get_text(strip=True)
                else:
                    title_text = title_elem.get_text(strip=True)
            else:
                link = article.find('a', class_='tm-article-snippet__title-link')
                if link:
                    title_text = link.get_text(strip=True)
                else:
                    title_text = "Заголовок не найден"
            
            articles.append({
                'title': title_text,
                'index': idx
            })
    return articles[:5]
