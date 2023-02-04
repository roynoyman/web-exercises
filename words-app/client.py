def get_keys(txt):
    words_list = txt.split()
    return words_list, set(words_list)


def get_words_counter(words_list, d):
    for w in words_list:
        d[w] += 1
    return d


def inital_dict(s):
    d = {k: 0 for k in s}
    return d


def validate_text(txt):
    if not type(txt) == str:
        raise TypeError('txt input must be str')


def word_count_text(txt):
    validate_text(txt)
    words_list, keys = get_keys(txt)
    dict = inital_dict(keys)
    counter = get_words_counter(words_list, dict)
    return counter

# if __name__ == '__main__':
#     txt = "bla bla bla a a a c c g bla"
#     ans = word_count_text(txt)
#     ans
