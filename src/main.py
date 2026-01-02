import os
import copy

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

def get_perlim(table, percent):
    # print(percent * 100, "Percent Table")
    mtable = table
    pertable = [[table[0][0]], [table[-1][0]]]
    # print("most likely", round(len(ftable[-1]) * percent), "outcomes")
    check = True
    while check:
        biggest = [mtable[0][1], mtable[-1][1], 1]
        for j in range(1, len(mtable[-1])):
            if mtable[-1][j] > biggest[1]:
                biggest = [mtable[0][j], mtable[-1][j], j]
        if biggest[1] < percent:
            check = False
        else:
            pertable[0].append(biggest[0])
            pertable[1].append(biggest[1])
            # print("X", round(biggest[0]/ftable[0][0], 2), round(biggest[1] * 100, 2), "%")
            index = biggest[2]
            mtable[0].pop(index)
            mtable[-1].pop(index)
    return pertable

def get_mlr(ftable):
    ret = [-1, 0]
    for i in range(1, len(ftable[0])):
        look = [ftable[-1][i], ftable[0][i]/ftable[0][0]]
        if look[0] == ret[0]:
            if look[1] > ret[1]:
                ret = look
        elif look[0] > ret[0]:
            ret = look
    return ret[0] * ret[1]

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
    # print("hit freq", round(persum * 100, 2), "%")

    perlimtable = ftable
    perlimtable = get_perlim(copy.deepcopy(perlimtable), .01)
    ev = get_rtp(perlimtable)[0]
    plrtp = get_rtp(perlimtable)[1]
    var = get_var(perlimtable, ev)
    sd = pow(var, .5)
    perlimsum = 0
    for i in range(1, len(perlimtable[-1])):
        perlimsum += perlimtable[-1][i]
    # print("hit freq", round(persum * 100, 2), "%")

    return [round(rtp, 2), round(sum * 100, 2), round(plrtp, 2), round((get_mlr(copy.deepcopy(ftable)) * 100), 2), round(((ftable[0][-1]/ftable[0][0]) * ftable[-1][-1]) * 100, 2), ftable[0][0]]


if __name__ == '__main__':
    weighted = True
    directory_path = "../lotteries"
    # rtp//hit freq//percent limit rtp//most likely return//jackpot rtp//min bet
    best = [0, 0, 0, 0, 0, 100, "name"]
    for root, _, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            check = get_stats(file_path)
            check.append(file_name.split(".tsv")[0])
            if weighted:
                rtpW = .3 #.3
                oowW = .1 #.1
                plrtpW = .5 #.5
                mlrW = .7 #.7
                checkW = (check[0] * rtpW) + (check[1] * oowW) + (check[2] * plrtpW) + (check[3] * mlrW)
                bestW = (best[0] * rtpW) + (best[1] * oowW) + (best[2] * plrtpW) + (best[3] * mlrW)
                if checkW > bestW:
                    best = check
                if check[5] <= 50 and checkW > 70:
                    print(check, checkW)
            else:
                if check[4] > 1.8:
                    print(check)
                if check[4] > best[4]:
                    best = check
    print("")
    print(" RTP%  Win%  LimRTP% MLR%")
    print(best)
    # atomic cash, boulder blast, clue, cow abduction, miner jack's combo caverns, pinata blast, prospectors gold rush, The mystery of jekyll and hyde, treasure tomb, wobblyblobs, zombie jive
    # what game has best odds of getting money back