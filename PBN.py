import random
import time
import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
import os
import numpy as np
import json
matplotlib.use('Agg')

class PBN:

    def __init__(self, nodenum, degree, is_thereconst, prob, no):
        self.nodenum = nodenum
        self.node = [self.Node(degree, prob) for _ in range(nodenum)]
        self.degree = degree
        self.is_thereconst = is_thereconst
        self.prob = prob
        self.check = [0 for _ in range(2 ** nodenum)]
        self.count = 1
        self.count2 = 0
        self.graph = nx.DiGraph()
        self.no = no
    
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
                
                if is_thereconst == 0 and self.is_constfunc() == True:
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
    
    def decode10to2_edit_oldstate(self, num10d) -> None:
        n = 0
        div = 2 ** (self.nodenum - 1)

        for n in range(self.nodenum):
            self.node[n].oldstate = num10d // div
            num10d = num10d % div
            div = div // 2
    
    def decode10to2(self, num10d) -> int:
        n = 0
        div = 2 ** (self.nodenum - 1)
        res = 0
        for n in range(self.nodenum):
            res = res * 2
            res += num10d // div
            num10d = num10d % div
            div = div // 2
        return res
    
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
        node_all_pattern_list = [str(self.decode10to2(i)) for i in range(node_all_pattern_num)]
        
        self.graph.add_nodes_from(node_all_pattern_list)

        for node_pattern in range(node_all_pattern_num):
            stateint = node_pattern
            self.decode10to2_edit_oldstate(node_pattern)

            if self.check[node_pattern] != 0:
                continue

            print(f"({self.count}) ", end="")
            while True:
                if self.check[stateint] != 0:
                    break

                self.check[stateint] = self.count
                current_state = node_all_pattern_list[stateint]
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
                next_state = node_all_pattern_list[stateint]

                self.graph.add_edge(current_state, next_state)

            for node in self.node:
                print(node.oldstate, end="")
            print(f"({self.check[stateint]})")

            if self.check[stateint] == self.count:
                self.count2 += 1
            self.count += 1

        print("\nアトラクタ数:", self.count2)
    
    def save_graph_and_attractor(self):
        if not os.path.exists(f"Save/{self.nodenum}node_{self.degree}degree_{self.is_thereconst}const_{self.prob}prob"):
            os.makedirs(f"Save/{self.nodenum}node_{self.degree}degree_{self.is_thereconst}const_{self.prob}prob")
        
        plt.figure(figsize=(12, 12))
        
        # 強連結成分（SCC）を見つける
        sccs = list(nx.strongly_connected_components(self.graph))
        
        # アトラクタを特定（1つ以上のノードを含むSCCで、外部への辺を持たないもの）
        attractors = []
        attractor_data = {
            "total_attractors": 0,
            "size_1_attractors": 0,
            "attractors": []
        }
        
        for scc in sccs:
            is_attractor = True
            for node in scc:
                for successor in self.graph.successors(node):
                    if successor not in scc:
                        is_attractor = False
                        break
                if not is_attractor:
                    break
            
            if is_attractor:
                sorted_scc = sorted(list(scc))
                attractors.append(sorted_scc)
                
                # アトラクタの情報を記録
                attractor_info = {
                    "size": len(sorted_scc),
                    "nodes": [format(int(node), f'0{self.nodenum}b') for node in sorted_scc]
                }
                attractor_data["attractors"].append(attractor_info)
                
                # サイズ1のアトラクタをカウント
                if len(sorted_scc) == 1:
                    attractor_data["size_1_attractors"] += 1
        
        attractor_data["total_attractors"] = len(attractors)
        
        # エッジリストを取得（重複なし）
        edge_list = list(self.graph.edges())
        
        # Force-directed layout with fixed edge lengths
        pos = nx.spring_layout(
            self.graph,
            k=1.5,
            iterations=100,
            weight='weight',
            fixed=None,
            scale=2.0,
            seed=42
        )
        
        # 双方向エッジの検出
        bidirectional_edges = []
        for u, v in edge_list:
            if (v, u) in edge_list and u != v and (v, u) not in bidirectional_edges:
                bidirectional_edges.extend([(u, v), (v, u)])
        
        # 通常の片方向エッジを描画（直線）
        normal_edges = [(u, v) for u, v in edge_list if (u, v) not in bidirectional_edges and u != v]
        nx.draw_networkx_edges(self.graph, pos,
                              edgelist=normal_edges,
                              edge_color='gray',
                              arrows=True,
                              arrowsize=30,
                              width=2,
                              arrowstyle='->',
                              min_source_margin=25,
                              min_target_margin=25)
        
        # 双方向エッジを描画（曲線）
        for u, v in bidirectional_edges:
            if u < v:
                nx.draw_networkx_edges(self.graph, pos,
                                     edgelist=[(u, v)],
                                     edge_color='gray',
                                     arrows=True,
                                     arrowsize=30,
                                     width=2,
                                     arrowstyle='->',
                                     connectionstyle="arc3,rad=0.2",
                                     min_source_margin=25,
                                     min_target_margin=25)
                nx.draw_networkx_edges(self.graph, pos,
                                     edgelist=[(v, u)],
                                     edge_color='gray',
                                     arrows=True,
                                     arrowsize=30,
                                     width=2,
                                     arrowstyle='->',
                                     connectionstyle="arc3,rad=0.2",
                                     min_source_margin=25,
                                     min_target_margin=25)
        
        # 自己ループの描画
        self_loops = [(u, v) for u, v in edge_list if u == v]
        for u, v in self_loops:
            nx.draw_networkx_edges(self.graph, pos,
                                 edgelist=[(u, v)],
                                 edge_color='gray',
                                 arrows=True,
                                 arrowsize=30,
                                 width=2,
                                 connectionstyle="arc3,rad=1.0",
                                 arrowstyle='-|>',
                                 min_source_margin=30,
                                 min_target_margin=30)
        
        # ノードの描画
        nx.draw_networkx_nodes(self.graph, pos,
                              node_color='lightblue',
                              node_size=2000,
                              edgecolors='darkblue',
                              linewidths=2)
        
        # ラベルを二進数に変換
        labels = {node: format(int(node), f'0{self.nodenum}b') for node in self.graph.nodes()}
        
        # ラベルの描画
        nx.draw_networkx_labels(self.graph, pos,
                               labels=labels,
                               font_size=12,
                               font_weight='bold',
                               font_family='sans-serif')
        
        plt.axis('off')
        plt.tight_layout()
        
        plt.savefig(f"Save/{self.nodenum}node_{self.degree}degree_{self.is_thereconst}const_{self.prob}prob/graph{self.no}.png",
                    dpi=300,
                    bbox_inches='tight')
        plt.close()

        # アトラクタ情報をJSONで保存
        json_path = f"Save/{self.nodenum}node_{self.degree}degree_{self.is_thereconst}const_{self.prob}prob/attractor{self.no}.json"
        with open(json_path, 'w') as f:
            json.dump(attractor_data, f, indent=4)

class PBNGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PBNシミュレーター")
        self.create_widgets()

    def create_widgets(self):
        input_frame = ttk.LabelFrame(self.root, text="パラメータ入力", padding=10)
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

        # ノード数（コンボボックス）
        ttk.Label(input_frame, text="ノードの数:").grid(row=0, column=0, sticky="w")
        self.nodenum = ttk.Combobox(input_frame, values=[4, 5, 6, 7], state="readonly")
        self.nodenum.set(4)
        self.nodenum.grid(row=0, column=1, padx=5, pady=2)

        # 次数（コンボボックス）
        ttk.Label(input_frame, text="次数:").grid(row=1, column=0, sticky="w")
        self.degree = ttk.Combobox(input_frame, values=[2, 3, 4], state="readonly")
        self.degree.set(2)
        self.degree.grid(row=1, column=1, padx=5, pady=2)

        # 定数関数（ラジオボタン）
        ttk.Label(input_frame, text="定数関数:").grid(row=2, column=0, sticky="w")
        self.is_thereconst = tk.IntVar(value=0)
        radio_frame = ttk.Frame(input_frame)
        radio_frame.grid(row=2, column=1, sticky="w")
        ttk.Radiobutton(radio_frame, text="なし", variable=self.is_thereconst, value=0).pack(side=tk.LEFT)
        ttk.Radiobutton(radio_frame, text="あり", variable=self.is_thereconst, value=1).pack(side=tk.LEFT)

        # 確率（スライダー）
        ttk.Label(input_frame, text="確率:").grid(row=3, column=0, sticky="w")
        slider_frame = ttk.Frame(input_frame)
        slider_frame.grid(row=3, column=1, sticky="ew")
        self.prob = tk.DoubleVar(value=0.5)
        self.prob_slider = ttk.Scale(
            slider_frame,
            from_=0.0,
            to=1.0,
            orient="horizontal",
            variable=self.prob,
            length=200
        )
        self.prob_slider.pack(side=tk.LEFT, fill="x", expand=True)
        self.prob_label = ttk.Label(slider_frame, textvariable=self.prob)
        self.prob_label.pack(side=tk.LEFT, padx=(5, 0))

        ttk.Label(input_frame, text="シミュレーション回数:").grid(row=4, column=0, sticky="w")
        self.sim_num = tk.IntVar(value=100)
        self.sim_num_entry = ttk.Entry(input_frame, textvariable=self.sim_num)
        self.sim_num_entry.grid(row=4, column=1, padx=5, pady=2)


        # 実行ボタン
        ttk.Button(self.root, text="実行", command=self.run_simulation).grid(row=1, column=0, pady=10)

    def validate_inputs(self):
        try:
            nodenum = int(self.nodenum.get())
            degree = int(self.degree.get())
            is_thereconst = self.is_thereconst.get()
            prob = self.prob.get()
            sim_num = int(self.sim_num.get())
            return nodenum, degree, is_thereconst, prob, sim_num
        except ValueError as e:
            messagebox.showerror("エラー", "入力値が不正です")
            return None

    def run_simulation(self):
        params = self.validate_inputs()
        if params:
            nodenum, degree, is_thereconst, prob, sim_num = params
            # GUIウィンドウを閉じる
            self.root.destroy()
            
            # PBNの実行
            for degree in range(2, 5):
                for is_thereconst in range(0, 2):
                    for i in range(sim_num):

                        pbn = PBN(7, degree, is_thereconst, prob, i)      
                        pbn.decide_func()
                        pbn.print_bool_table()
                        pbn.decide_topology()
                        pbn.print_topology()
                        pbn.run()
                        pbn.save_graph_and_attractor()
        else:
            # エラーダイアログを表示した後、GUIは開いたままにする
            messagebox.showerror("エラー", "入力値を確認してください")

def main():
    random.seed(time.time())
    while True:
        try:
            gui = PBNGUI()
            gui.root.mainloop()
            # GUIが正常に閉じられた場合（有効な入力後）はループを抜ける
            break
        except Exception as e:
            # 予期せぬエラーが発生した場合
            messagebox.showerror("エラー", f"予期せぬエラーが発生しました: {str(e)}")
            continue

if __name__ == "__main__":
    main()