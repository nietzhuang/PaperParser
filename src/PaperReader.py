import os
import sys
import re
import pdb

import PyPDF2
from tqdm import tqdm
from main import ask, log


class PaperReader:
    def __init__(self, dir_paper, dir_path):
        self.dir_paper = dir_paper
        self.dir_path = dir_path
        self.workpath = os.getcwd()
        # os.chdir(dir_path)

    def ask_keywords(self):
        keyword_string = input('Enter your keywords to parse papers (e.g. DNN, hardware, accelerator): ') 
        # keyword_string = 'DNN, hardware' 
        keywords = re.sub(' ', '', keyword_string).split(',')
        return keywords

    def printhits(self, paper_hits):
        log('The following list your keywords that appear among the papers:', color='white')

        for item in range(len(paper_hits)):
            log(paper_hits[item][0], 'green')

            for kw, hits in paper_hits[item][1].items():
                log(kw + ': ' + str(hits), 'blue')
        print()


    def start(self):
        keywords = self.ask_keywords()
        # keyword_dict = dict(zip(keywords, kw_hits))

        # # os.chdir(dir_path)
        kw_hits = [0] * len(keywords)
        paper_hits = []
        for fname in tqdm(os.listdir(self.dir_path)):
            reader = PyPDF2.PdfReader(os.path.join(self.dir_path, fname), strict=False)
            for page in range(len(reader.pages)):
                word_list = reader.pages[page].extract_text().split()
                for hit_idx in range(len(kw_hits)):
                    kw_hits[hit_idx] += sum(keywords[hit_idx].lower() == w.lower() 
                                            or keywords[hit_idx].lower() == w.lower() for w in word_list)
            
            paper_hits.append([fname, dict(zip(keywords, kw_hits))])
        
        self.printhits(paper_hits)




