import os.path

def get_datafile():
    datafile = "dataset.bag"
    if os.path.exists("./data/" + datafile):
        datasetsDir = "./data/"
    elif os.path.exists("../data/" + datafile):
        datasetsDir = "../data/"
    else:
        datasetsDir = "/media/aitor/Data1/"
    return datasetsDir + datafile