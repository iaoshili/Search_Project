#/usr/bin/python 

__UPLOADS = "uploads"

class A():
    def __init__(self):
        self.test()

    def test(self):
        global __UPLOADS
        print __UPLOADS

def main():
    a = A()

if __name__ == "__main__":
    main()