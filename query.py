#!/usr/bin/env python
import nltk
from nltk.corpus import stopwords

import db
import spellcorrector


# def run_query(query):
#     db = MySQLdb.connect(user="root", passwd="123123", db="dialogengine")
#     cur = db.cursor()
#     cur.execute(query)
#     data = cur.fetchall()
#     db.close()
#     return data

def run_query():
    pass

def RemoveStopWords(query_list):
    cachedStopWords = stopwords.words("english")
    query_list = [q for q in query_list if q not in cachedStopWords]    
    # remove all other terms which are not available in our
    # categories, features and brands except numbers which will
    # be used in range queries
    def is_number(n):
        try:
            int(n)
            return True
        except:
            return False
    copy_query_list = query_list[:]
    with open("ForSpellChecking.txt") as f:
        c = f.read()
    query_list = [q for q in query_list if is_number(q) or q in c]
    query_list = remove_wh(query_list)
    removed = [t for t in copy_query_list if t not in query_list]
    print query_list, removed
    return [query_list, removed]

def remove_wh(query_list):
    t = ['What', 'Why', 'Who', 'Which', 'whose']
    removed = []
    for x in query_list:
        if x not in t:
            removed.append(x)
    return removed

# def execute_query(query_list):
#     feature = query_list[0]
#     print feature
#     product = ' '.join(query_list[1:])
#     tables = run_query('SHOW TABLES;')
#     for table in tables:
#         t = table[0]
#         features = run_query('describe `%s`' % (t))
#         for f in features:
#             if feature == f[0]:
#                 try:
#                     #print 'SELECT %s from `%s` where Brand="%s"' % (feature, t, product)
#                     data = run_query('SELECT %s from `%s` where Brand="%s"' % (feature, t, product))
#                 except:
#                     try:
#                         data = run_query('SELECT %s from `%s` where `Brand Name`="%s"' % (feature, t, product))
#                     except:    
#                         data = ()
#                 if len(data) != 0 and data[0][0] != 'NULL':
#                     return [[feature], [product], [d[0] for d in data]]

def get_query_type_and_details(query_list, removed_terms):
    out = {}

    # comparison type
    for q in removed_terms:
        if "er" == q[-2:]: # lesser, higher
            print query_list
            out["type"] = "comparison"
            details = {}
            details["comp_term"] = q
            details["feature"] = query_list[0]
            details["products"] = query_list[1:]
            out["details"] = details
            return out

        if "range" == q:
            print query_list

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


def execute_query(query_list, removed_terms):
    return get_query_type_and_details(query_list, removed_terms)
    e_query_list = query_list[:]
    for i in xrange(len(query_list)):
        query_list[i] = spellcorrector.correct(query_list[i])
    feature = query_list[0]
    product = ' '.join(query_list[1:])
    efeature, eproduct = e_query_list[0], ' '.join(e_query_list[1:])
    # feature = spellcorrector.correct(feature, "features")
    # product = spellcorrector.correct(product, "brands")
    val = db.findProductFeatureValue(product, feature)
    if val:
        return {"feature": feature, "product": product, "val": val, "spellcorrected": {efeature: feature, eproduct: product}}

def output_in_user_format(output):
    if not output:
        return "Sorry. We couldn't find any relevant information for your question."
    s = ""
    for key, value in output['spellcorrected'].iteritems():
        if key != value:
            s += "(showing results for %s instead of %s\n)" % (value, key)
    s += "%s of %s is %s" % (output["feature"], output["product"], output["val"])
    return s

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
    query_list, removed_terms = RemoveStopWords(query_list)
    #print nltk.pos_tag(query_list)
    # print query_list
    output = execute_query(query_list, removed_terms)
    return output
    return output_in_user_format(output)

if __name__ == "__main__":
    inp = raw_input('Enter a question: ')
    print main(inp)
