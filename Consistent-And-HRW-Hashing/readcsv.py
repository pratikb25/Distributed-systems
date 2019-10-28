import csv

def main():
    with open('causes-of-death.csv', mode='r') as csv_file:
        start = False
        csv_reader = csv.reader(csv_file)
        for line in csv_reader:
            if(start is False):
                start = True
                continue
            key = line[0]+line[2]+line[3]
            print(key)
            #print("Key: (%s:%s:%s)" % (line[0],line[2],line[3]))


if __name__ == '__main__':
    main()
