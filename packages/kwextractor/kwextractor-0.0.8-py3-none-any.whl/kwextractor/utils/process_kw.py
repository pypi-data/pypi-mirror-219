import re

def sort_keywords(keywords):
    keywords.sort(key=len, reverse=True)
    return keywords


def flatten(A):
    """
    Flatten a list of lists.

    :param A: list of lists (multi-dimensional list, e.g. [[1, 2], [3, 4]])
    :return: list (e.g. [1, 2, 3, 4])
    """
    rt = []
    for i in A:
        if isinstance(i, list):
            rt.extend(flatten(i))
        else:
            rt.append(i.lower().replace(' ', '_'))
    return rt


def merge_type_keywords(keywords):
    """
    Merge keywords from different types to one list.

    :param keywords: a dictionary of keywords
    (e.g. {'person': ['Donald Trump', 'Barack Obama'], 'location': ['Hanoi', 'Ha Noi']})
    :return: a list of keywords (e.g. ['Donald Trump', 'Barack Obama', 'Hanoi', 'Ha Noi'])
    """
    all_val = list(keywords.values())
    flat= flatten(all_val)
    return flat


def clean_text(text):
    """
    Clean text by removing special characters, numbers, stop words, etc.

    :type text: string
    :param text: text to be cleaned
    :return: cleaned text
    """
    text = re.sub(r'[;!@#$%^&*()_+\-=\[\]{}\'\\"|<>/]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r"\s\s+", " ", text)
    return text


def remove_duplicate_keywords(keywords):
    """
    Remove duplicate keywords.

    Example: ['Donal Trump', 'Donald' , 'Trump'] -> ['Donald Trump']

    :param keywords: list of keywords
    :return: list of filtered keywords
    """
    filtered_keywords = []
    for kw in keywords:
        subkw = False
        for anotherkw in keywords:
            if kw != anotherkw and kw in anotherkw:
                subkw = True
                break
        if not subkw:
            filtered_keywords.append(kw)
    return filtered_keywords


def is_subset(arr1, arr2):
    """
    Check if arr1 is a subset of arr2

    :param arr1: a list of words
    :param arr2: a list of words
    :return: boolean
    """

    # Create a Frequency Table using STL
    frequency = {}
    m = len(arr1)
    n = len(arr2)
    # Increase the frequency of each element
    # in the frequency table.
    for i in range(0, m):
        if arr1[i].lower() in frequency:
            frequency[arr1[i].lower()] = frequency[arr1[i].lower()] + 1
        else:
            frequency[arr1[i].lower()] = 1

    # Decrease the frequency if the
    # element was found in the frequency
    # table with the frequency more than 0.
    # else return 0 and if loop is
    # completed return 1.
    for i in range(0, n):
        if arr2[i].lower() in frequency:
            if frequency[arr2[i].lower()] > 0:
                frequency[arr2[i].lower()] -= 1
            else:
                return False
        else:
            return False

    return True


def is_overlap(str1, str2):
    """
    Check if two strings are overlapped.

    :param str1: string 1
    :param str2: string 2
    :return: True if two strings are overlapped, False otherwise
    """
    arr_str1 = str1.split(' ')
    arr_str2 = str2.split(' ')

    merged = ''
    if arr_str1[-1].lower() == arr_str2[0].lower():
        merged = ' '.join(arr_str1[:-1] + arr_str2)
    elif arr_str1[0].lower() == arr_str2[-1].lower():
        merged = ' '.join(arr_str2[:-1] + arr_str1)
    elif is_subset(arr_str1, arr_str2):
        merged = str1
    elif is_subset(arr_str2, arr_str1):
        merged = str2
    return merged
