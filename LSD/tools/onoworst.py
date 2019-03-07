
def generate_onoworst(outpath, vertnumber):
    f = open(outpath, "w")
    for i in range(vertnumber-1):
        f.write("{fro} {to}\n".format(fro=i, to=(i + 1)))
        f.write("{fro} {to}\n".format(fro=i, to=vertnumber))
        # for j in range(2):
        #     f.write("{fro} {to}\n".format(fro=i, to=(i+j + 1) % vertnumber))
    f.close()
    
    
def generate_dirctworst(outpath, vertnumber):
    f = open(outpath, "w")
    for i in range(vertnumber):
        f.write("{fro} {to}\n".format(fro=i, to=(i + 1) % vertnumber))
    f.write("{fro} {to}\n".format(fro=0, to=vertnumber))
        # for j in range(2):
        #     f.write("{fro} {to}\n".format(fro=i, to=(i+j + 1) % vertnumber))
    f.close()


if __name__ == "__main__":
    import sys
    path = sys.argv[1]
    size = int(float(sys.argv[2]))
    # generate_onoworst(path, size)
    generate_dirctworst(path, size)
