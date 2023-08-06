
from .read_tydex import read_tydex_file

def read_and_print():
    #Give the file path
    file_path = 'C:/Users/ssy/Desktop/hiwi-test/code/TEST1.tdx'
    tydex_struct = read_tydex_file(file_path)
    print(tydex_struct)