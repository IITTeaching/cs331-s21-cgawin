import urllib.request
import requests


def book_to_words(book_url='http://www.gutenberg.org/files/84/84-0.txt'):
    booktxt = urllib.request.urlopen(book_url).read().decode()
    bookascii = booktxt.encode('ascii', 'replace')
    return bookascii.split()


def count_sort(words_lst, char_idx):
    buckets = [0 for _ in range(128)]  # keep track of amount of each ASCII character
    sorted_lst = [None for _ in range(len(words_lst))]  # resulting (sorted) list of words

    """ Store amount of occurrences of each character """
    for word in words_lst:
        buckets[word[char_idx]] += 1

    """ Accumulate prior buckets """
    for bucket_idx in range(len(buckets) - 1):
        buckets[bucket_idx + 1] += buckets[bucket_idx]

    """ Place words at correct position in sorted list """
    for word in reversed(words_lst):
        sorted_lst[buckets[word[char_idx]] - 1] = word
        buckets[word[char_idx]] -= 1

    return sorted_lst


def radix_a_book(book_url='https://www.gutenberg.org/files/84/84-0.txt'):
    words_lst = book_to_words(book_url)
    max_len = len(max(words_lst, key=len))

    """ Pad each word so all are same length """
    for i in range(len(words_lst)):
        words_lst[i] = words_lst[i].ljust(max_len)

    """ Iterate through each character and perform count sort """
    for char_idx in reversed(range(max_len)):  # iterate through each character
        words_lst = count_sort(words_lst, char_idx) # perform count sort

    """ Remove padding """
    words_lst = [i.replace(b' ', b'') for i in words_lst]

    return words_lst


def test():
    words = book_to_words()
    radixed_lst = radix_a_book()
    sorted_lst = sorted(words)
    for i in range(len(words)):
        assert str(radixed_lst[i]) == str(sorted_lst[i])


def main():
    test()


if __name__ == '__main__':
    main()
