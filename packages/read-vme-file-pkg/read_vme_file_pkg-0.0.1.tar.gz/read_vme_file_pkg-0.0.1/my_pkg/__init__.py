
from .read_vme import read_vme_file

def read_and_print():
    #Give the file path
    file_path = 'C:/Users/ssy/Desktop/hiwi-test/code/TEST215.24'
    ret_dict = read_vme_file(file_path)
    print(ret_dict)