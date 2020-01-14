# This file houses functions to create a corpus of wikipedia summaries
import wikipedia as wk
import time

exclude_flag = ['List ','National Register of Historic']
exclude_flag += [str(i) for i in range(1000,2018)]
par_delim = ' -- '


def get_wikipedia_summary(num_articles=10):
    data = []
    for i in range(int(num_articles / 10)):
        try:
            page_titles = wk.random(10)
        except ConnectionError:
            time.sleep(60)
        for title in page_titles:
            summary = get_summary_from_search_term(title,exclude_flag)
            if summary is not None:
                data.append(summary)
    return data


def get_summary_from_search_term(title, excludes_flag):
    if any([flag in title for flag in exclude_flag]):
        return
    try:
        page = wk.page(title)
        summary = page.summary
        summary = summary.replace('\n', par_delim)
        return summary
    except (wk.exceptions.DisambiguationError, wk.exceptions.PageError):
        pass
    except Exception as huh:
        print(huh)


def write_to_file(data,fp):
    with open(fp,'ab') as stash:
        stash.write('\n'.join(data).encode())




############ MAIN #############

def scan_write_corpus():
    run = 0
    while True:
        print('Run #%s' %run)
        data = get_wikipedia_summary(100)
        write_to_file(data,'corpus\\corpus.txt')
        time.sleep(60)
        run +=1


if __name__ == '__main__':
    scan_write_corpus()
    # load_model('corpus\\corpus.txt')