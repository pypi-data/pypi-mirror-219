import openpyxl
import pandas as pd 
from tqdm import tqdm 
from tqdm import tqdm 
import sys 
import os 



def remove_first_line(file_path,sheet_name): 
    wb = openpyxl.load_workbook(file_path)
    sheet = wb[sheet_name]
    status = sheet.cell(sheet.min_row, 1).value
    sheet.delete_rows(sheet.min_row, 1)
    wb.save(file_path)


def merge_files(dir_path):
    final_list = [] 
    for _file in tqdm(os.scandir(dir_path)):
        df = pd.read_excel(_file.path)
        final_list.append(df)

    master_df = pd.concat(final_list, ignore_index=True)
    print("Starting Write...")
    master_df.to_csv("./master.csv",index=False)



def main(): 
    print("starting the process...")
    
    source_dir = sys.argv[1].lstrip("\"'").rstrip("\"'")
  
    source_dir = os.path.abspath(source_dir) 
    if not  os.path.exists(source_dir): 
        print("The Specified Directory {} does not exist aborting!!".format(source_dir))
        exit(0)
    files = list(os.scandir(source_dir))
    print("found {}(s) files begining to process".format(len(files)))
    print("begining process of removing first line ....")
    for _file in tqdm(list(files)): 
        remove_first_line(_file.path,"sheet1")


    print("done removing first lines")

    print("starting to merge..")
    merge_files(source_dir)
    print("done writing files")

