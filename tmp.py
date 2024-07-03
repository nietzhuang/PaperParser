import os
import PyPDF2
import pandas as pd
from tqdm import tqdm

pth = r"D:\papers\61 DAC Proceedings\61 DAC Proceedings\Files"
paper_dict = {
    "paper": [],
    "BERT": [],
    "GPT": [],
    "Llama": [],
    "Transformer": [],
}
for fname in tqdm(os.listdir(pth)):
    reader = PyPDF2.PdfReader(os.path.join(pth, fname), strict=False)
    num_BERT = 0
    num_GPT = 0
    num_Llama = 0
    num_tran = 0
    for page in range(len(reader.pages)):
        word_lst = reader.pages[page].extract_text().split()
        num_BERT += sum("Bert" == w or "BERT" == w for w in word_lst)
        num_GPT += sum("GPT" in w or "gpt" in w for w in word_lst)
        num_Llama += sum("Llama" in w or "llama" in w or "LLAMA" in w for w in word_lst)
        num_tran += sum("Transformer" in w or "ViT" in w for w in word_lst)
    if num_BERT > 0 or num_GPT>0 or num_Llama>0 or num_tran>0:
        paper_dict["paper"].append(fname)
        paper_dict["BERT"].append(num_BERT)
        paper_dict["GPT"].append(num_GPT)
        paper_dict["Llama"].append(num_Llama)
        paper_dict["Transformer"].append(num_tran)
    # if num_Llama > 0:
    #     break
df = pd.DataFrame.from_dict(paper_dict)
df.to_csv('out.csv', index=False) 
print(df)