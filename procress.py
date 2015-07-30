#-*- coding: UTF-8 -*-
import string
from BeautifulSoup import BeautifulSoup
import urllib, re, sqlite3, os
import chardet
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import AffinityPropagation
from nltk.stem import SnowballStemmer
from sklearn.cluster import KMeans
import numpy
import FileUtil
from xml.dom.minidom import Document
from sklearn.feature_extraction.text import TfidfVectorizer
reload(sys)
sys.setdefaultencoding('utf-8')
METADATA_DIR = 'F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/metadata'
WEPPAGES_DIR = 'F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/web_pages'
EXTRECT_DIR = 'F:/Data/homework/clustering/me/des'
dis = []
def des_extrect():
    filename_list = []
    file_stopwords = file('stopwords.txt', "r")
    stopwords = [line.strip() for line in file_stopwords.readlines()]  
    for file_name in os.listdir(DESCRIPTION_DIR):
        filename_list.append(file_name) 
    for filename in filename_list:
        path =  os.path.join(DESCRIPTION_DIR, filename)
        fr = file(path, 'r')
        fw = file(filename+'.des', 'w')
        soup = BeautifulSoup(fr.read())
        docs = soup.findAll('doc')
        for doc in docs:
            content = str(doc['title'] + doc.snippet.text)
            content =  re.sub("[\.\@\,\:\;\!\?\(\)]".decode("utf8"), "".decode("utf8"),content)
            stemmer = SnowballStemmer('english')
            content = content.split()
            pro_content = ''
            for w in content: 
                w = stemmer.stem(w)
                #去停用词
                if w not in stopwords:
                    pro_content += w + ' '
            fw.write(doc['rank'] + ' ' +pro_content+'\n')
        fw.close()
        fr.close()
    

def procress_together():
    dir = r"F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/web_pages"
    file_stopwords = file('stopwords.txt', "r")
    stopwords = [line.strip() for line in file_stopwords.readlines()]
    scan=FileUtil.ScanFile(dir,postfix='.f')
    files = scan.scan_files() 
    corpus = []
    for f in files:
        fr = file(f, 'r')
        corpus_file_path = str(f)[:-1] + 'token'
        fw = file(corpus_file_path, 'w')
        soup = BeautifulSoup(fr.read())
        title = str(soup.title.string).strip()
        snippet = str(soup.snippet.string).strip()
        content = title + ' ' + snippet 
        content =  re.sub("[\.\@\,\:\;\!\?\(\)]", " ",content)
        content = content.split()
        stemmer = SnowballStemmer('english')
        pro_content = ''
        for w in content: 
            #w = stemmer.stem(w)
                    #去停用词
            if w not in stopwords:
                pro_content +=  ' ' + w + ' '
        fw.write(pro_content) 
        fw.close()
        fr.close()
    return
def procress_nem_together():
    dir = r"F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/web_pages"
    file_stopwords = file('stopwords.txt', "r")
    stopwords = [line.strip() for line in file_stopwords.readlines()]
    scan=FileUtil.ScanFile(dir,postfix='.nem')
    files = scan.scan_files() 
    corpus = []
    for f in files:
        fr = file(f, 'r')
        corpus_file_path = str(f)[:-3] + 'token'
        fw = file(corpus_file_path, 'a')
        content = str(fr.read()).strip()
        if len(content) == 0:
            continue
        encoding = chardet.detect(content)['encoding']
        content = content.decode(encoding).encode('utf-8')
        content =  re.sub("[\.\@\,\:\;\!\?\(\)]", " ",content)
        content = content.split()
        stemmer = SnowballStemmer('english')
        pro_content = ''
        for w in content: 
            #w = stemmer.stem(w)
                    #去停用词
            if w not in stopwords:
                pro_content += ' ' + w + ' '
        fw.write(pro_content) 
        fw.close()
        fr.close()
    return
METADATA_DIR = 'F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/metadata'
WEPPAGES_DIR = 'F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/web_pages'
def getTitle_Url_Snippet():
    filename_list = []
    for file_name in os.listdir(METADATA_DIR):
        filename_list.append(file_name) 
    for filename in filename_list:
        path =  os.path.join(METADATA_DIR, filename)
        fr = file(path, 'r')
        soup = BeautifulSoup(fr.read())
        docs = soup.findAll('doc')
        for doc in docs:
            rank = doc['rank']
            title = doc['title']
            url = doc['url']
            snip = doc.snippet
            content = '<title>\n' + str(title) + '\n</title>\n' +  '<url>\n' + str(url) + '\n</url>\n' + '<snippet>\n' + str(snip)[9:-10]+'\n</snippet>\n'
            #content =  re.sub("[\.\@\,\:\;\!\?\(\)]".decode("utf8"), "".decode("utf8"),content)
            write_file_path = WEPPAGES_DIR + '/' + filename[:-4] + '/' + str(rank).zfill(3) + '.nem'
            fw = file(write_file_path, 'w')
            fw.write("")
        fw.close()
        fr.close()
    return
def getMetadata():
    dir = r"F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/web_pages"
    scan=FileUtil.ScanFile(dir,postfix='.html')
    files = scan.scan_files() 
    for f in files:
        fr = file(f ,'r')
        file_append_path = str(f)[:-4] + 'nem'
        fw = open(file_append_path,'a')
        soup = BeautifulSoup(fr.read())
        metas = soup.findAll('meta')
        #metadata = '\n<metadata>\n'
        metadata = ''
        if metas is not None:
            try:
                for m in metas:
                    for attr in  m.attrs:
                        for i in attr:
                            if str(i).lower() == 'name':
                                if str(m['name']).lower() == 'description':
                                    metadata += m['content']
                                if str(m['name']).lower() == 'keywords':
                                    metadata += m['content']
                                                   
            except:
                print '-------------except------------------'
        fw.write(metadata)
        fw.close()
        fr.close()                
    return
def getNameEntity():
    dir = r"F:/Data/homework/clustering/test_data/ae_gold_standard/AE"
    scan=FileUtil.ScanFile(dir,postfix='.txt')
    files = scan.scan_files() 
    for f in files:
        fr = file(f, 'r') 
        ne_list = ['' for i in range(151)]
        for line in fr:
            line_list = line.split() 
            for i in line_list[2:]:
                ne_list[int(line_list[0])] += str(i) + ' '
        for i, ne in enumerate(ne_list):
            if len(ne) is 0:
                print '----------'
                continue
            file_name = '/'+ str(i).zfill(3) +'.nem'
            name_pos =  str(f).rfind('\\')
            folder_name = str(f)[name_pos+1:-4]
            file_append_path = "F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/web_pages/" + folder_name + file_name
            fw = open(file_append_path,'w')
            #metadata = '\n<name_entity>\n'
            metadata = ne
            #metadata += '\n</name_entity>'
            metadata = fw.write(metadata) 
            fw.close()
        fr.close()
def tfidf_vector(folder,d):
    dir = "F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/web_pages/" + folder
    scan=FileUtil.ScanFile(dir,postfix='.token')
    files = scan.scan_files() 
    clusting_result_path = "F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/results/"+folder+'.xml'
    isExists = os.path.exists(clusting_result_path)
    if isExists:
        print 'exist'
        return
    corpus = []
    dis_list = []
    clust_list = []
    for i in d:
        dis_list.append(int(i))
    for f in files:
        #去掉discard
        name_pos =  str(f).rfind('\\')+1
        dn = int(f[name_pos:-6])
        #print type(dn)
        if dn in dis_list: 
            continue
        clust_list.append(dn)    
        fr = file(f, 'r')
        content = str(fr.read()).strip()
        encoding = chardet.detect(content)['encoding']
        content = content.decode(encoding).encode('utf-8')
        #content = content.split()
        corpus.append(content)
        fr.close()
    #vectorizer = CountVectorizer(stop_words='english')    
    tfv = TfidfVectorizer(min_df=3,  max_features=None, 
        strip_accents='unicode', analyzer='word',token_pattern=r'\w{1,}',
        ngram_range=(1, 2), use_idf=1,smooth_idf=1,sublinear_tf=1,
        stop_words = 'english') 
    tfv.fit(corpus)
    tfidf_all = tfv.transform(corpus) 
    cluster_num = 19
    kmeans = KMeans(n_clusters=cluster_num)
    kmeans.fit(tfv)
    labels = kmeans.labels_
    s = 0
    result = [[] for i in range(cluster_num)]
    dis_len = len(dis_list)
    for i in range(150-dis_len):
        result[labels[i]].append(clust_list[i])
    fw = file(clusting_result_path, 'w')
    doc = Document()
    root = doc.createElement('clustering')
    doc.appendChild(root)
    for i, e in enumerate(result):
        entity = doc.createElement('entity')
        entity.setAttribute('id',str(i))
        for r in e:
            rank = doc.createElement('doc')
            rank.setAttribute('rank',str(r))
            entity.appendChild(rank)
        root.appendChild(entity)
    fw.write(doc.toprettyxml(indent = '  ', encoding='UTF-8'))     
    print 'writing success'
    fr.close() 
    fw.close()
def ap(folder, d):
    dir = "F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/web_pages/" + folder
    scan=FileUtil.ScanFile(dir,postfix='.token')
    files = scan.scan_files() 
    clusting_result_path = "F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/results/"+folder+'.xml'
    isExists = os.path.exists(clusting_result_path)
    if isExists:
        print 'exist'
        return
    corpus = []
    dis_list = []
    for i in d:
        dis_list.append(int(i))
    clust_list = []   
    for f in files:
        #去掉discard
        name_pos =  str(f).rfind('\\')+1
        dn = int(f[name_pos:-6])
        #print type(dn)
        if dn in dis_list: 
            continue
        clust_list.append(dn) 
        fr = file(f, 'r')
        content = str(fr.read()).strip()
        encoding = chardet.detect(content)['encoding']
        content = content.decode(encoding).encode('utf-8')
        #content = content.split()
        corpus.append(content)
        fr.close()
    vectorizer = CountVectorizer(stop_words='english')    
    transformer = TfidfTransformer()
    tf_idf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    word = vectorizer.get_feature_names()
    weight = tf_idf.toarray()
    '''
    for i in range(len(weight)):
        for j in range(len(word)):  
            print str(word[j]).encode("utf-8"), str(weight[i][j]).encode("utf-8")  
        return
        '''
    agg = AffinityPropagation()
    agg.fit(tf_idf)
    labels = agg.labels_
    s = 0
    result = [[] for i in range(labels.size)]
    dis_len = len(dis_list)
    for i in range(150-dis_len):
        result[labels[i]].append(clust_list[i])
    fw = file(clusting_result_path, 'w')
    doc = Document()
    root = doc.createElement('clustering')
    doc.appendChild(root)
    for i, e in enumerate(result):
        entity = doc.createElement('entity')
        entity.setAttribute('id',str(i))
        for r in e:
            rank = doc.createElement('doc')
            rank.setAttribute('rank',str(r))
            entity.appendChild(rank)
        root.appendChild(entity)
    fw.write(doc.toprettyxml(indent = '  ', encoding='UTF-8'))     
    print 'writing success'
    fr.close() 
    fw.close()
def traverse_folder():
    filename_list = []
    folders = []
    for file_name in os.listdir(METADATA_DIR):
        filename_list.append(file_name) 
    for i, f in enumerate(filename_list):
        #
        dis_f = dis[i]
        #ap(str(f)[:-4],dis_f)
        tfidf_vector(str(f)[:-4],dis_f)
        #folders.append(str(f)[:-4])
def discard():
    dir = "F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/gold_standard"
    scan=FileUtil.ScanFile(dir,postfix='.xml')
    files = scan.scan_files() 
    dis = [[] for i in range(30)]
    for n, f in enumerate(files):
        fr = file(f ,'r')
        soup = BeautifulSoup(fr.read())
        dis_doc = soup.discarded.contents
        for i,doc in enumerate(dis_doc):
            if i == 0:
                continue
            dis[n].append(doc['rank'])
    return dis            
def delete_file():
    dir = "F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/web_pages"
    scan=FileUtil.ScanFile(dir,postfix='.netoken')
    files = scan.scan_files() 
    for f in files:
        os.remove(f)
if __name__ == '__main__':
    #getTitle_Url_Snippet() #从html中获取title，url，snippet并写入*.f
    #getMetadata() #从html获取metadata
    #getNameEntity() #获取name entity存入*.nem
    #procress_together() #将title，snippet写入*.token
    #procress_nem_together() #将ne和metadata写入*.token
    dis = discard()
    traverse_folder()  #遍历每个名字文件夹，并分类 
   # tfidf('AMANDA_LENTZ', dis[0])
    
