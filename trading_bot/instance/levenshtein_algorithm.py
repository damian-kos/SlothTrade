from thefuzz import fuzz

def fuzz_test(query, db_item):
    similarity = fuzz.token_set_ratio(query, db_item)
    return similarity
