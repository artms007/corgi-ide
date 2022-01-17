
import os

def modules_dl():
    DIR_PATH = os.path.dirname(__file__)
    FILE_PATH = DIR_PATH + '/requirements.txt'    
    os.system(f'pip3 install -r {FILE_PATH}')

# def modules_dl():
#     DIR_PATH = os.path.dirname(__file__)
#     FILE_PATH = DIR_PATH + '/requirements.txt'
#     COMMAND = 'pip3 install -r ' + FILE_PATH
#     # print(COMMAND)
#     os.system(COMMAND)

if __name__ == "__main__":
    # print("File: ", os.path.dirname(__file__))
    modules_dl()
