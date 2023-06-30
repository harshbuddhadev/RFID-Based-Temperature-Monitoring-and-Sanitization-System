import os

def vali(tagid):
    id=""
    if(tagid=="75005339405F"):
        id=["Rachit","S","001"]
    elif(tagid=="2400352DD4E8"):
        id=["Harsh","B","002"]
    elif(tagid=="5800CA1337B6"):
        id=["Namr","S","003"]
    elif(tagid=="5800CA1AE76F"):
        id=["Bunty","L","004"]
    elif(tagid=="5800CA0D6EF1"):
        id=["Peter","D","005"]
    elif(tagid=="5800CA138D0C"):
        id=["Karan","M","006"]
    elif(tagid=="5800C9EFFE80"):
        id=["Jai","J","007"]
    elif(tagid=="5800C9A6B582"):
        id=["Karan","G","008"]
    elif(tagid=="5800CA1636B2"):
        id=["Abhishek","G","009"]
    else:
        id=[]
        

    return id

if __name__ == "__main__":
    test=str(os.popen("sudo head -c 12 /dev/ttyUSB0").read())
    print(vali(test))