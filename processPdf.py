import re
import dill
from datetime import datetime
import textract
from pathlib import Path

fname = '200309-sustainable-finance-teg-final-report-taxonomy-annexes_en.pdf'
workdir = '/home/jovyan/work/nlpexp/QA-DL-liveproject/QAwithDL'
tempdir = f'{workdir}/working'

class ProcessPdf:

    def __init__(self):
        self.text = ''
        self.paras = []
        Path(tempdir).mkdir(parents=True, exist_ok=True)

    def getText(self):
        time1 = datetime.now()

        self.text = '' 
        filepath = Path(tempdir)/f"{fname}.txt"

        if filepath.is_file():
            # print(filepath.name + " exists")
            with filepath.open(mode='r') as text_file:
                self.text = text_file.read()
                text_file.close()
        else:
            self.text = textract.process(f"{workdir}/{fname}")
            with filepath.open(mode='wb') as text_file:
                print(self.text, file=text_file)
                text_file.close()
                
        time2 = datetime.now()   
        print("Fetched text of length {} in {}".format(len(self.text), time2-time1))

    def toParagraphs(self):
        time1 = datetime.now()

        self.paras = []
        filepath = Path(tempdir)/f"{fname}.paras.d"

        if filepath.is_file():
            with filepath.open(mode='rb') as paras_file:
                self.paras = dill.load(paras_file)
                paras_file.close()
        else:
            self.paras = re.split(r'\s*\n+\s*', self.text.decode('utf-8'))
            with filepath.open(mode='wb') as paras_file:
                dill.dump(self.paras, paras_file)
                paras_file.close()

        time2 = datetime.now()  
        print("Extracted paragraphs {} in {}".format(len(self.paras), time2-time1))

    def main(self):
        self.getText()
        self.toParagraphs()

if __name__ == "__main__":
    p = ProcessPdf()
    p.main()
