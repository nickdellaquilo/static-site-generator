from textnode import TextNode, TextType

def main():
    test = TextNode("Hello there", TextType.LINK, "https://github.com/nickdellaquilo/")
    print(test)




if __name__ == "__main__":
    main()