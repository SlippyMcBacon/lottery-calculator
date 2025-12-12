from main import numberize

def clean(filename):
    table = []
    with open(filename, "r") as file:
        go = True
        while go:
            row = file.readline().strip()
            if row == "":
                go = False
            else:
                table.append(row)
    cleaned = []
    sum = 0
    for i in range(len(table)):
        if table[i] == "Deposit":
            num = numberize(table[i+2]) * -1
            sum += num
            cleaned.append(num)
        elif table[i] == "CashOut Request":
            num = numberize(table[i+2]) * -1
            sum += num
            cleaned.append(num)
    print(sum)
    return cleaned

if __name__ == '__main__':
    # cleaned = clean("../files/spent_test.tsv")
    cleaned = clean("../files/spent.tsv")
    for i in range(len(cleaned)):
        print(cleaned[i])
