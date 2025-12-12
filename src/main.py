import os

def numberize(str):
    if "$" in str:
        elements = str.split("$")
        num = float(elements[1].replace(",", ""))
        if elements[0] == "-":
            num *= -1
        return num
    elif str == '':
        return str
    else:
        str = float(str.replace(",", ""))
        return 1/str

def get_rtp(ftable):
    sum = 0
    for i in range(1, len(ftable[0])):
        sum += (ftable[0][i] * ftable[-1][i])
        # print(ftable[0][i] * ftable[-1][i], ftable[0][i], ftable[-1][i], i)
    # print("RTP", round(sum / ftable[0][0],  2) * 100, "%")
    return [sum, (sum / ftable[0][0]) * 100]

def get_var(ftable,ev):
    sum = 0
    for i in range(1, len(ftable[0])):
        sum += ((ftable[0][i] - ev) ** 2) * ftable[-1][i]
    return sum

def get_per(ftable, percent):
    # print(percent * 100, "Percent Table")
    mtable = ftable
    pertable = [[ftable[0][0]], [ftable[-1][0]]]
    # print("most likely", round(len(ftable[-1]) * percent), "outcomes")
    for i in range(1, round(len(ftable[-1]) * percent)):
        biggest = [mtable[0][1], mtable[-1][1], 1]
        for j in range(1, len(mtable[-1])):
            if mtable[-1][j] > biggest[1]:
                biggest = [mtable[0][j], mtable[-1][j], j]
        pertable[0].append(biggest[0])
        pertable[1].append(biggest[1])
        # print("X", round(biggest[0]/ftable[0][0], 2), round(biggest[1] * 100, 2), "%")
        index = biggest[2]
        mtable[0].pop(index)
        mtable[-1].pop(index)
    return pertable

def get_stats(filename):
    name = filename.split("../lotteries")
    # print("stats for", name[1][1:])
    table = []
    first = True
    with open(filename, "r") as file:
        go = True
        while(go):
            row = file.readline().strip()
            if(row == ""):
                go = False
            elif(first):
                first = False
                temp = row.split("\t")
                temp.append("")
                table.append(temp)
            else:
                table.append(row.split("\t"))
    ftable = []
    for i in range(len(table[0])):
        entry = []
        for j in range(len(table)):
            entry.append(numberize(table[j][i]))
        # print(entry)
        ftable.append(entry)
    ev = get_rtp(ftable)[0]
    rtp = get_rtp(ftable)[1]
    var = get_var(ftable, ev)
    sd = pow(var, .5)
    sum = 0
    for i in range(1, len(ftable[-1])):
        sum += ftable[-1][i]
    # print("hit freq", round(sum * 100, 2), "%")

    # print("")
    pertable = get_per(ftable, .1)
    ev = get_rtp(pertable)[0]
    prtp = get_rtp(pertable)[1]
    var = get_var(pertable, ev)
    sd = pow(var, .5)
    persum = 0
    for i in range(1, len(pertable[-1])):
        persum += pertable[-1][i]
    # print("hit freq", round(persum * 100, 2), "%")
    return [round(rtp, 2), round(abs(sum - persum) * 100, 2), round(prtp, 2), round(rtp - (100 - prtp), 2)]


if __name__ == '__main__':
    long = True
    directory_path = "../lotteries"
    # rtp, hit freq - per hit freq, prtp, rtp - (100 - prtp)
    best = [0, 100, 0, -100, "name"]
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            check = get_stats(file_path)
            check.append(file_name)
            print(check)
            if long:
                #if check[0] == best[0]:
                #    if check[1] < best[1]:
                #    best = check
                #elif check[0] > best[0]:
                #    best = check
                if(check[3] > best[3]):
                    best = check
            else:
                if check[2] > best[2]:
                    best = check
    print("")
    print(best)
    # atomic cash, boulder blast, clue, cow abduction, miner jack's combo caverns,