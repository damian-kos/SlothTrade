import numpy as np
from thefuzz import fuzz


def fuzz_test(query, db_item):
    similarity = fuzz.token_set_ratio(query, db_item)
    return similarity


# def levenshtein_similarity(search_phrase, db_item):
#     size_a = len(search_phrase) + 1
#     size_b = len(db_item) + 1

#     matrix = np.zeros((size_a, size_b))

#     for i in range(size_a):
#         matrix[i, 0] = i

#     for j in range(size_b):
#         matrix[0, j] = j

#     for i in range(1, size_a):
#         for j in range(1, size_b):
#             if search_phrase[i - 1].lower() == db_item[j - 1].lower():
#                 matrix[i, j] = min(
#                     matrix[i - 1, j - 1],
#                     matrix[i - 1, j] + 1,
#                     matrix[i, j - 1] + 1,
#                 )
#             else:
#                 matrix[i, j] = min(
#                     matrix[i - 1, j] + 1,
#                     matrix[i - 1, j - 1] + 1,
#                     matrix[i, j - 1] + 1,
#                 )
#     return int(matrix[-1, -1])
