# encoding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def data2csv(filename, data, mid=False):
    f = open(filename + '.csv', 'a+')
    id_index = 0
    for line in f:
        id_index += 1
    for d in data:
        if mid == False:
            f.write(','.join(d) + '\n')
        else:
            f.write(str(id_index) + ',' + ','.join(d) + '\n')
            id_index += 1
    f.close()


def header2csv(filename, headers):
    f = open(filename + '.csv', 'a+')
    header = ','.join(headers)
    f.write(header + "\n")
    f.close()

