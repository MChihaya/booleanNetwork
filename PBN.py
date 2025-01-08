import random
import time

class PBN:

    def __init__(self, nodenum, degree, is_thereconst, prob):
        self.nodenum = nodenum
        self.node = [self.Node(degree, prob) for _ in range(nodenum)]
        self.degree = degree
        self.is_thereconst = is_thereconst
        self.prob = prob
        self.check = [0 for _ in range(2 ** nodenum)]
        self.count = 1
        self.count2 = 0
    
    class Node:
        def __init__(self, degree, prob):
            self.degree = degree
            self.func = [None for _ in range(2 ** degree)]
            self.topology = []
            self.prob = prob
            self.state = None
            self.oldstate = None
        def set_func(self, is_thereconst) -> None:
            num2d = 2 ** self.degree
            for i in range(num2d):
                if (random.random() < self.prob):
                    self.func[i] = 1
                else:
                    self.func[i] = 0
                
                if is_thereconst == 0 and self.is_constfunc(self.func, num2d) == True:
                    i -= 1
        def get_nextstate(self, input) -> int:
            return self.func[input]
        
        def is_constfunc(self) -> bool:
            x = self.func[0]
            for i in range(2 ** self.degree):
                if self.func[i] != x:
                    return False
            return True
        def set_topology(self, nodenum) -> None:
            while len(self.topology) < self.degree:
                tmp = random.randint(0, nodenum - 1)
                is_overlap = False
                for topology in self.topology:
                    if topology == tmp:
                        is_overlap = True
                        break
                if is_overlap == False:
                    self.topology.append(tmp)
    def encode2to10(self) -> int:
        res = 0
        for node in self.node:
            res = res * 2
            res += node.state
        return res
    
    def decode10to2(self, num10d) -> None:
        n = 0
        div = 2 ** (self.nodenum - 1)

        for n in range(self.nodenum):
            self.node[n].oldstate = num10d // div
            num10d = num10d % div
            div = div // 2
    
    def decide_func(self) -> None:
        n = 2 ** self.degree
        for i in range(self.nodenum):
            self.node[i].set_func(self.is_thereconst)
    
    def print_bool_table(self) -> None:
        print(*[i + 1 for i in range(self.degree)], "|", *[chr(ord('A') + i) for i in range(self.nodenum)])
        for num2d in range(2 ** self.degree):
            if self.degree >= 4:
                print(num2d//8, (num2d%8) // 4, (num2d%4) // 2, num2d%2, "|", end="")
            elif self.degree == 3:
                print(num2d//4, (num2d%4) // 2, num2d%2, "|", end="")
            elif self.degree == 2:
                print(num2d//2, num2d%2, "|", end="")
        
            for node in self.node:
                print(" " + str(node.func[num2d]), end="")
            print("")
    
    def decide_topology(self) -> None:
        for i in range(self.nodenum):
            self.node[i].set_topology(self.nodenum)
    
    def print_topology(self) -> None:
        print("  |", end="")
        for i in range(self.degree):
            print(" " + str(i+1), end="")
        print("")
        for i in range(self.nodenum):
            print(chr(ord('A') + i) + " |", end="")
            for j in range(self.degree):
                print(" " + chr(ord('A') + self.node[i].topology[j]), end="")
            print("")
    
    def run(self) -> None:
        node_all_pattern_num = 2 ** self.nodenum

        for node_pattern in range(node_all_pattern_num):
            stateint = node_pattern
            self.decode10to2(node_pattern)

            if self.check[node_pattern] != 0:
                continue

            print(f"({self.count}) ", end="")
            while True:
                if self.check[stateint] != 0:
                    break

                self.check[stateint] = self.count
                for j in range(self.nodenum):
                    print(self.node[j].oldstate, end="")
                print("->", end="")

                for node in self.node:
                    funcnum = 0
                    for k in range(self.degree):
                        funcnum = funcnum * 2 + self.node[node.topology[k]].oldstate
                    node.state = node.get_nextstate(funcnum)

                for node in self.node:
                    node.oldstate = node.state

                stateint = self.encode2to10()

            for node in self.node:
                print(node.oldstate, end="")
            print(f"({self.check[stateint]})")

            if self.check[stateint] == self.count:
                self.count2 += 1
            self.count += 1

        print("\nアトラクタ数:", self.count2)

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

    pbn = PBN(nodenum, degree, is_thereconst, prob)
    print("ブール関数をランダムに決定します。")
    pbn.decide_func()
    
    pbn.print_bool_table()

    print("それぞれのノードの入力がどのノードから来るのかを表示(トポロジーの決定)")
    pbn.decide_topology()
    pbn.print_topology()
    
    print("ネットワークを動作させます\n")
    pbn.run()


if __name__ == "__main__":
    main()