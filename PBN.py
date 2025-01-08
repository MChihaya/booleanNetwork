import random
import time
def is_constfunc(a, n) -> bool:
    x = a[0]
    for i in range(n):
        if a[i] != x:
            return False
    return True

def encode2to10(state, node) -> int:
    res = 0
    for i in range(node):
        res = res * 2
    return res

def decode10to2(state, num10d, node) -> None:
    n = 0
    div = 2 ** (node - 1)

    for n in range(node):
        state[n] = num10d / div
        num10d = num10d % div
        div = div / 2

def main():
    random.seed(time.time())
    nodenum = None
    degree = None
    is_thereconst = None
    prob = None
    while True:
        nodenum = int(input("ノードの数を入力してください(4～7)"))
        if nodenum >= 4 and nodenum <= 7:
            break

    while True:
        degree = int(input("次数を入力してください(2～4)"))
        if degree >= 2 and degree <= 4:
            break

    while True:
        is_thereconst = bool(input("定数関数がある場合は1、ない場合は0を入力してください"))
        if is_thereconst == 0 or is_thereconst == 1:
            break
    
    while True:
        prob = float(input("確率を入力してください(0.0～1.0)"))
        if prob >= 0.0 and prob <= 1.0:
            break

    print("ブール関数をランダムに決定します。")
    n = n ** degree
    func = [[None for _ in range(n)] for _ in range(nodenum)]
    for i in range(nodenum):
        for j in range(n):
            if (random.random() < prob):
                func[i][j] = 1
            else:
                func[i][j] = 0
        
        if is_thereconst == 0 and is_constfunc(func[i], n):
            i -= 1
    
    print(*[i + 1 for i in range(degree)], "|", *[chr(ord('A') + i) for i in range(nodenum)])

    for i in range(n):
        if degree >= 4:
            print(i//8, (i%8) // 4, (i%4) // 2, i%2, "|", end="")
        elif degree == 3:
            print(i//4, (i%4) // 2, i%2, "|", end="")
        elif degree == 2:
            print(i//2, i%2, "|", end="")
    
        for j in range(nodenum):
            print(" " + str(func[j][i]), end="")


    
    
    


if __name__ == "__main__":
    main()