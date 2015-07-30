#-*- coding: UTF-8 -*-
import string
from BeautifulSoup import BeautifulSoup
import urllib, re, sqlite3, os
from chardet import detect
import sys
import numpy
from nltk.tag.stanford import NERTagger
import codecs
reload(sys)
sys.setdefaultencoding('utf-8')

java_path = "E:/java/jdk1.8/bin" # replace this
os.environ['JAVAHOME'] = java_path

#reference https://github.com/idear1203/html2text
class ScanFile(object):
    def __init__(self,directory,prefix=None,postfix=None):
        self.directory=directory
        self.prefix=prefix
        self.postfix=postfix
    
    def scan_files(self):
        files_list=[]
        
        for dirpath,dirnames,filenames in os.walk(self.directory):
            '''
                dirpath is a string, the path to the directory.
                dirnames is a list of the names of the subdirectories in dirpath (excluding '.' and '..').
                filenames is a list of the names of the non-directory files in dirpath.
            '''  
            for special_file in filenames:
                if self.postfix:
                  if special_file.endswith(self.postfix):
                    files_list.append(os.path.join(dirpath,special_file))
                elif self.prefix:
                  if special_file.startswith(self.prefix):
                    files_list.append(os.path.join(dirpath,special_file))
                else:
                  files_list.append(os.path.join(dirpath,special_file))
    
        return files_list

    def scan_subdir(self):
        subdir_list=[]
        for dirpath,dirnames,files in os.walk(self.directory):
            subdir_list.append(dirpath)
        return subdir_list

def mkdir(path):
    import os
    path=path.strip()
    path=path.rstrip("\\")
    isExists = os.path.isdir(path)
    if not isExists:
        print 'make dir ing'
        os.makedirs(path)
        return True
    else:
        return False
if __name__ == '__main__':
    dir = r"F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/plain_text/BERTRAM_BROOKER"
    scan=ScanFile(dir,postfix='.txt')
    f_except = file('F:/Data/homework/clustering/test_data/WePS2_test_data/data/test/plain_text/except.txt', 'w')
    files=scan.scan_files()
    st = NERTagger('F:/Data/homework/clustering/stanford-ner-2015-04-20/classifiers/english.all.3class.distsim.crf.ser.gz','F:/Data/homework/clustering/stanford-ner-2015-04-20/stanford-ner.jar')
    for f in files:
        print f
        f_encoding = file(f,'r')
        data_encoding = f_encoding.read()
        encoding = detect(data_encoding)['encoding']
        f_encoding.close()
        fr = codecs.open(str(f), 'r', encoding)
        write_file_path = str(f)+'.ne'
        if os.path.exists(write_file_path):
            print 'existing, skip'
            continue
        fw = file(write_file_path, 'w')
        extrect_list = [[] for i in range(3)]
        try:
            for line in fr:
                line = str(line).decode(encoding, errors='ignore')
                tag = st.tag(str(line).split())
                for i in tag:
                    for j in i:
                        if j[1] == 'PERSON':
                            extrect_list[0].append(j[0])
                        if j[1] == 'LOCATION':
                            extrect_list[1].append(j[0])
                        if j[1] == 'ORGANIZATION':
                            extrect_list[2].append(j[0])
            print 'start to write'
            for i in extrect_list:
                fw.write('---------------')
                for j in i:
                    fw.write(j+' ') 
                fw.write('\n')                    
        except:
            f_except.write(str(f) + '') 
            continue
        f_except.close 
        fr.close()            
        fw.close()

