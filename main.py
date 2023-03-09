import requests
from bs4 import BeautifulSoup, Tag
import copy

def get_html(url):
    r = requests.get(url)
    return r.text


def get_data(html, urlDest, i = 0, path =""):
    soup = BeautifulSoup(html, 'lxml')
    paragrahps = soup.find('div', id='mw-content-text').find_all('p')
    refs_in_paragrahs = []
    for paragraph in paragrahps:
        # print(paragraph.text)
        paragrath_with_a = ""
        for content in paragraph.contents:
            if isinstance(content, Tag):
                if content.name == 'a':
                    paragrath_with_a += content.text + "(ссылка)"
                else:
                    paragrath_with_a += content.text
            else:
                paragrath_with_a += content
        paragrath_with_a.split('.')
        list_of_sentences = list(filter(lambda element: "(ссылка)" in element, paragrath_with_a.split('.')))
        list_of_sentences_with_a = []
        for sentence in list_of_sentences:
            for k in range(sentence.count("(ссылка)")):
                list_of_sentences_with_a.append(sentence)
        if paragraph.find_all('a') and list_of_sentences_with_a:
            refs_in_paragrahs.append((paragraph.find_all('a'), list_of_sentences_with_a))
    refs = []
    for refs_in_one_paragraph, sentences in refs_in_paragrahs:
        for ref, sentence in zip(refs_in_one_paragraph, sentences):
            url = ref.get('href')
            if url is not None and '#' not in url:
                refs.append((url, sentence))
    urls = []
    for ref, text in refs:
        if '/wiki' in ref:
            if 'https' not in ref:
                url = 'https://ru.wikipedia.org' + ref
            else:
                url = ref
            if url not in urls:
                urls.append((url, text))
    if 'https://ru.wikipedia.org/wiki/Nintendo_3DS' in urls:
        print('НАШЛОСЬ')
    for url, text in urls:
        if url == urlDest:
            path += text + "\n"  + url + "\n"
            print(path)
            return
        if i != 2:
            get_data(get_html(url), urlDest, i + 1, (path + '.')[:-1] + text + "\n"  + url + "\n")

urlInp = input("Введите начальный url: ")
urlDest = input("Введите конечный url: ")
url = 'https://ru.wikipedia.org/wiki/Xbox_360_S'
url2 = 'https://ru.wikipedia.org/wiki/Nintendo_3DS'
get_data(get_html(urlInp), urlDest)
print()


