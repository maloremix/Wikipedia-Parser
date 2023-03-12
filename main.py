from bs4 import BeautifulSoup, Tag
import asyncio
import aiohttp

async def async_get_refs(session, url):
        list_of_sentences_with_a = []
        response = await session.get(url=url)
        soup = BeautifulSoup(await response.text(), "lxml")
        paragrahps = soup.find('div', id='mw-content-text').find_all('p')
        refs = []
        for paragraph in paragrahps:
            paragrath_with_a = ""
            for content in paragraph.contents:
                if isinstance(content, Tag):
                    if content.name == 'a':
                        ref = content.get("href")
                        if ref is not None:
                            standart_ref = ref if 'https' in ref else 'https://ru.wikipedia.org' + ref
                            refs.append(standart_ref)
                            paragrath_with_a += content.text + "(ссылка)"
                    else:
                        paragrath_with_a += content.text
                else:
                    paragrath_with_a += content
            paragrath_with_a.split('.')
            list_of_sentences = list(filter(lambda element: "(ссылка)" in element, paragrath_with_a.split('.')))
            for sentence in list_of_sentences:
                for k in range(sentence.count("(ссылка)")):
                    list_of_sentences_with_a.append(sentence.replace("(ссылка)", ""))
        return refs, list_of_sentences_with_a

async def get_data(session, ref1, sentence1, url_dest):
    if ref1 == url_dest:
        print("1------------------------" + "\n" + ref1 + sentence1 + "\n\n\n")
    refs2, sentences2 = await async_get_refs(session, ref1)
    for ref2, sentence2 in zip(refs2, sentences2):
        if ref2 == url_dest:
            print("1------------------------" + "\n" + sentence1 + "\n" + ref1 + "\n" + "2------------------------" + "\n" + sentence2 + "\n" +  ref2 + "\n\n\n")
        refs3, sentences3 = await async_get_refs(session, ref2)
        for ref3, sentence3 in zip(refs3, sentences3):
            if ref3 == url_dest:
                print("1------------------------" + "\n" + sentence1 + "\n" + ref1 + "\n" + "2------------------------" + "\n" + sentence2 + "\n" +  ref2 + "\n" + "3------------------------" + "\n" + sentence3 + "\n" + ref3 + "\n\n\n")

async def gather_async(url_inp, url_dest):
    async with aiohttp.ClientSession() as session:
        refs, sentences = await async_get_refs(session, url_inp)
        tasks = []
        for ref, sentence in zip(refs, sentences):
            task = asyncio.create_task(get_data(session, ref, sentence, url_dest))
            tasks.append(task)
        await asyncio.gather(*tasks)

url_inp = input("Введите начальный url: ")
url_dest = input("Введите конечный url: ")
# url1 = 'https://ru.wikipedia.org/wiki/Xbox_360_S'
# url2 = "https://ru.wikipedia.org/wiki/Nintendo_3DS"
asyncio.run(gather_async(url_inp, url_dest))