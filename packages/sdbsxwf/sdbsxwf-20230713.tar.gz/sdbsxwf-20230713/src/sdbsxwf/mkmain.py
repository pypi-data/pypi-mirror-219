import mkgjx
#print(mkgjx.__file__)
#print(mkgjx.cc())




def bb():
    a=input("我是主模块:")
    print(a)
    b=mkgjx.cc()
    print(b)
    input("end")

def aa():
    print("我是主函数")
if __name__ == "__main__":
    bb()

