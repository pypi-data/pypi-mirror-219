import sys

def check():
    a = sys.version
    b = a[0]
    c = a[2:4]
    try:
        int(c)
    except ValueError:
        c = a[2:3]
        int(c)
    int(b)
    if (b==2 and c<6) or (b==3 and c<3) or (b==3 and c>12):
        raise OSError("Please use Python 2.6, 2.7, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10, 3.11, 3.12")
