import wikipedia as wk
import markovify as mk
import time
exclude_flag = ['List ','National Register of Historic']
exclude_flag += [str(i) for i in range(1000,2018)]
par_delim = ' -- '


def get_wikipedia_summary(num_articles=10):
    data = []
    for i in range(int(num_articles / 10)):
        page_titles = wk.random(10)
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


def read_corpus(fp):
    with open(fp, 'rb') as docs:
        data = docs.readlines()
        decoded = [line.decode('utf8').replace(par_delim, '').replace('=','') for line in data]
        decoded = list(set(decoded))
    return decoded


def load_model(fp):
    decoded = read_corpus(fp)
    text_model = mk.NewlineText('\n'.join(decoded))
    print('_'*100)
    for i in range(20):
        message = text_model.make_short_sentence(280)
        if message is not None:
            print(message)


def get_tweet(fp, live=False, size=280):
    if live:
        decoded = get_wikipedia_summary(200)
    else:
        decoded = read_corpus(fp)
    text_model = mk.NewlineText('\n'.join(decoded))
    print('_'*100)
    for i in range(20):
        message= text_model.make_short_sentence(size)
        if message is not None:
            return message

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