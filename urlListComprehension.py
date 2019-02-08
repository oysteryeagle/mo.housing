with open('urls.txt','r') as f:
    urls = [line.rstrip() for line in f]
    print(len(urls))
