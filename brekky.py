import bs4
import urllib3
import requests
import markovify as mk
import wikipedia as wk
import nltk
from wiki_gen import write_to_file, par_delim
imgur = r'https://imgur.com/search/score?q=breakfast'


wiki = r'https://en.wikipedia.org/'
list_of_bfast_foods = 'wiki/List_of_breakfast_foods'
bfast_general = 'Breakfast'

bfast_search = [['List of breakfast foods', '== Breakfast foods =='],['Index of breakfast-related articles','== B ==']]

class scan_wiki_bfast(object):
    def __init__(self):
        self.current_trailer = None

    def get_breakfast_foods(self, id_tuple):
        trailer, id_to_find = id_tuple
        get_wiki = requests.get(wiki + trailer)
        self.current_trailer = trailer
        page_content = get_wiki.content
        soup = bs4.BeautifulSoup(page_content)
        head = soup.find(id=id_to_find)
        uls = head.find_all_next('ul')
        data = []
        # for ul in uls:
        for a in head.find_all_next('a'):
            if not self.check_link(a):
                data.append(a)
            if a.find_next(id='See_also') is None:
                break


    def check_link(self,tag):
        try:
            href = tag['href']
            link_drop = ['#cite', 'w/index.php?', self.current_trailer]
            ld = any([l in href for l in link_drop])
        except KeyError:
            ld = False

        try:
            class_ = tag['class']
            class_drop = ['image', 'external', 'selflink']
            cl = any([c in class_ for c in class_drop])
        except KeyError:
            cl = False

        try:
            title = tag['title']
            title_drops = ['Wikipedia:Citation needed']
            td = any([t in title for t in title_drops])
            print(a['title'])
        except KeyError:
            td = False
        if any([ld, cl, td]):
            return True


def filter_content(content, beg, end='== See also =='):
    content = content.split('\n')
    content = content[content.index(beg):content.index(end)]
    cache = content[:]
    for entry in cache:
        remove = False
        if '' == entry:
            remove = True
        elif '== ' in entry:
            remove = True
        if remove:
            content.remove(entry)
    return content

def get_breakfast_foods_to_search():
    search_list = ['Breakfast']
    for page, beg in bfast_search:
        wk_page = wk.page(page)
        search_list += filter_content(wk_page.content, beg, '== See also ==')
    return search_list

def search_list_of_topics(search_list):
    data = []
    print(len(search_list))
    searched = []
    for topic in set(search_list):
        wk_page = search_term(topic)
        if wk_page is None:
            topic = refine_search(topic)
            wk_page = search_term(topic)
        if wk_page is None:
            continue
        if wk_page.title in searched:
            continue
        data.append(wk_page.summary)
        searched.append(wk_page.title)
    return data


def search_term(topic):
    try:
        content = wk.page(topic)
        return content
    except (wk.exceptions.PageError, wk.exceptions.DisambiguationError) as fine:
        pass
    except wk.exceptions.WikipediaException as weird:
        print('weird exception::  %s' % weird)

def refine_search(term):
    term = term.split('-')[0]
    term = term.strip()
    return term


def access_breakfast():
    foods = get_breakfast_foods_to_search()
    data= search_list_of_topics(foods)
    text_model = mk.Text(''.join(data))
    output = []
    for i in range(5):
        sent = text_model.make_short_sentence(280)
        if sent is not None:
            # return sent
            output.append(sent)
            print(sent)
    return output


def clean_summaries(data):
    return [row.replace('\n',' -- ') for row in data]


def write_breakfast():
    foods = get_breakfast_foods_to_search()
    data = search_list_of_topics(foods)
    data = clean_summaries(data)
    write_to_file(data, 'corpus\\breakfast\\breakfast.txt')


if __name__ == '__main__':
    access_breakfast()
    # scanner = scan_wiki_bfast()
    # scanner.get_breakfast_foods((list_of_bfast_foods,'Breakfast_foods'))