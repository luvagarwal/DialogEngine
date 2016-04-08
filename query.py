#!/usr/bin/env python
import nltk
from nltk.corpus import stopwords
import MySQLdb

cachedStopWords = stopwords.words("english")

def run_query(query):
    db = MySQLdb.connect(user="root", passwd="123123", db="dialogengine")
    cur = db.cursor()
    cur.execute(query)
    data = cur.fetchall()
    db.close()
    return data

def RemoveStopWords(word_list):
    removed = []
    for x in word_list:
        if x not in cachedStopWords:
            removed.append(x)
    return removed

def remove_wh(word_list):
    t = ['What', 'Why', 'Who', 'Which']
    removed = []
    for x in word_list:
        if x not in t:
            removed.append(x)
    return removed

def execute_query(word_list):
    feature = word_list[0]
    product = ' '.join(word_list[1:])
    tables = run_query('SHOW TABLES;')
    for table in tables:
        t = table[0]
        features = run_query('describe `%s`' % (t))
        for f in features:
            if feature == f[0]:
                try:
                    #print 'SELECT %s from `%s` where Brand="%s"' % (feature, t, product)
                    data = run_query('SELECT %s from `%s` where Brand="%s"' % (feature, t, product))
                except:
                    try:
                        data = run_query('SELECT %s from `%s` where `Brand Name`="%s"' % (feature, t, product))
                    except:    
                        data = ()
                if len(data) != 0 and data[0][0] != 'NULL':
                    return [[feature], [product], [d[0] for d in data]]


def output_in_user_format(output):
    if not output:
        return "Sorry. We couldn't find any relevant information for your question."
    return "The %s of the %s is %s" % (output[0][0], output[1][0], output[2][0])

def main(query):
    word_list = nltk.word_tokenize(query)
    # print word_list
    word_list = RemoveStopWords(word_list)
    #print nltk.pos_tag(word_list)
    # print word_list
    word_list = remove_wh(word_list)
    output = execute_query(word_list)
    return output_in_user_format(output)

if __name__ == "__main__":
    inp = raw_input('Enter a question: ')
    print main(inp)
