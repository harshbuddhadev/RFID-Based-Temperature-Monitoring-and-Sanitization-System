import os

def vali(tagid):
    id=""
    if(tagid=="75005339405F"):
        id=["Rachit","Sharma","70331019040"]
    # elif(tagid=="2400352DD4E8"):
    #     id=["Harsh","Buddhadev","70331019003"]
    elif(tagid=="5800CA1337B6"):
        id=["Shinty","Sharma","01234"]
    elif(tagid=="5800CA1AE76F"):
        id=["Bunty","LifeBuoy","9876"]
    elif(tagid=="5800CA0D6EF1"):
        id=["Peter","Daruwala","6543"]
    elif(tagid=="5800CA138D0C"):
        id=["Titu","Mama","4567"]
    elif(tagid=="5800C9EFFE80"):
        id=["Jai","J.","1987"]
    elif(tagid=="5800C85C74B8"):
        id=["Bhaalu","Sharma","123987"]
    elif(tagid=="5800C9A6B582"):
        id=["Karan","Gandi","70331019040"]
    elif(tagid=="5800CA1636B2"):
        id=["Abhishek","Garg","70331019007"]
    else:
        id=[]
        

    return id


# while(True):
#     test=str(os.popen("sudo head -c 12 /dev/ttyUSB0").read())
#     print(validate(test))

#     break