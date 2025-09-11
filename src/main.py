import os
import shutil
from textnode import TextNode, TextType

def main():
    test = TextNode("Hello there", TextType.LINK, "https://github.com/nickdellaquilo/")
    print(test)
    transfer()



def transfer(src="static", dst="public"):
    if not os.path.exists(dst):
        os.makedirs(dst)
    shutil.rmtree(dst)
    shutil.copytree(src, dst)
    

if __name__ == "__main__":
    main()