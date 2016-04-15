#!/usr/bin/env python
import re
import nltk
from nltk.corpus import stopwords

import db
import spellcorrector


def run_query():
    pass

def RemoveStopWords(query_list):
    def is_number(n):
        try:
            int(n)
            return True
        except:
            return False

    cachedStopWords = stopwords.words("english")
    query_list = [q for q in query_list if q not in cachedStopWords]    
    # remove all other terms which are not available in our
    # categories, features and brands except numbers which will
    # be used in range queries
    corrected_terms = {}
    for i in xrange(len(query_list)):
        if is_number(query_list[i]):
            continue
        tmp = spellcorrector.correct(query_list[i])
        if tmp != query_list[i]:
            corrected_terms[query_list[i]] = tmp
            query_list[i] = tmp

    copy_query_list = query_list[:]

    with open("ForSpellChecking.txt") as f:
        c = f.read()

    c = c.replace("feature", "")
    query_list = [q for q in query_list if is_number(q) or q in c]
    query_list = remove_wh(query_list)
    removed_terms = [t for t in copy_query_list if t not in query_list]
    print query_list, removed_terms
    return [query_list, removed_terms, corrected_terms]


def remove_wh(query_list):
    t = ['What', 'Why', 'Who', 'Which', 'whose']
    removed = []
    for x in query_list:
        if x not in t:
            removed.append(x)
    return removed


def get_query_type_and_details(query_list, removed_terms):
    out = {}
    # comparison type
    for q in removed_terms:
        if "er" == q[-2:]: # lesser, higher
            out["type"] = "comparison"
            details = {}
            details["comp_term"] = q
            details["feature"] = query_list[0]
            details["products"] = query_list[1:]
            out["details"] = details
            return out
        if "range" in q:
            out["type"] = "range"
            # Ex. "what are all the dslr cameras between the price range 100 to 200"
            details = {}
            details["range"] = query_list[-2:]
            query_list = query_list[:-2]
            details["feature"] = query_list[-1]
            query_list.pop()
            details["category"] = ' '.join(query_list)
            out["details"] = details
            return out
    # query found is "feature type"
    out["type"] = "featurevalue"
    details = {}
    if "features" in removed_terms:
        details["feature"] = "all_features"
        details["product"] = ' '.join(query_list)
    else:
        details["feature"] = query_list[0]
        details["product"] = ' '.join(query_list[1:])
    out["details"] = details
    return out

def print_format_all_features(val, product):
    out = "Following are the features for %s\n" % (product)
    for f in val:
        if f == "_id":
            continue
        out += "%s -> %s\n" % (f, val[f])
    return out

def print_format_feature_value(val, feature, product):
    return "%s of %s is %s" % (feature, product, val)

def print_format_comparison(val, products, feature, com_term):
    pos = ["better", "higher", "larger", "greater"]
    val = [re.findall(r'\d+', v)[0] for v in val]
    l = [i for i in zip(val, products)]    
    if com_term in pos:    
        l = sorted(l, reverse=True)
    else:
        l = sorted(l)
    val = [i[0] for i in l]
    products = [i[1] for i in l]
    out = "%s of %s is %s than %s" % (feature, products[0], com_term, products[1])
    for p in products[2:]:
        out += " in turn %s than %s" % (com_term, p)
    out += " with values as "
    for v in val:
        out += "%s, "%(v)
    out = out[:-2]
    out += " respectively."
    return out

def print_format_range(val, feature, r, category):
    products = [v for v in val]
    print "products are %s" % (products)
    out = "We have the following products in %s to %s:\n" % (r[0], r[1])
    for i, p in enumerate(products):
        out += "%s. " % (i+1)
        for k in p:
            if k == "_id":
                continue
            out += "%s is %s\n" % (k, p[k])
    return out


def execute_query_feature_value(query_details):
    feature, product = query_details["feature"], query_details["product"]
    val = db.findProductFeatureValue(product, feature)
    if feature == "all_features":
        return print_format_all_features(val, product)
    else:
        return print_format_feature_value(val, feature, product)

def execute_query_comparison(query_details):
    feature = query_details["feature"]
    products = query_details["products"]
    products = [' '.join(products[0:2]), ' '.join(products[2: 4])]
    val = []
    for product in products:
        val.append(db.findProductFeatureValue(product, feature))
    return print_format_comparison(val, products, feature, query_details["comp_term"])

def execute_query_range(query_details):
    feature = query_details["feature"]
    category = query_details["category"]
    r = query_details["range"]
    val = db.findProductsInRange(feature, r, category)
    return print_format_range(val, feature, r, category)

def execute_query(query_list, removed_terms, corrected_terms):
    query_info = get_query_type_and_details(query_list, removed_terms)
    tmp, etmp = "", ""
    for k in corrected_terms:
        tmp += "%s "%(corrected_terms[k])
        etmp += "%s "%(k)
    out = ""
    if tmp != etmp:
        out = "(showing results for %s instead of %s)\n" % (tmp, etmp)
    if query_info["type"] == "featurevalue":
        val = execute_query_feature_value(query_info["details"])
    elif query_info["type"] == "comparison":
        val = execute_query_comparison(query_info["details"])
    elif query_info["type"] == "range":
        val = execute_query_range(query_info["details"])
    
    if val:
        return out + val
    else:
        return "Sorry. We couldn't find any relevant information for your question."


def remove_puncs(query):
    puncs = ["?", "!", ",", ":", "'"]
    new_query = ""
    for c in query:
        if c in puncs:
            continue
        new_query += c
    return new_query


def main(query):
    query = query.lower()
    query = remove_puncs(query)
    query_list = nltk.word_tokenize(query)
    query_list, removed_terms, corrected_terms = RemoveStopWords(query_list)
    #print nltk.pos_tag(query_list)
    # print query_list
    output = execute_query(query_list, removed_terms, corrected_terms)
    return output
    return output_in_user_format(output)

if __name__ == "__main__":
    inp = raw_input('Enter a question: ')
    print main(inp)
