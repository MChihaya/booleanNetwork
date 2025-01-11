import json
import matplotlib.pyplot as plt
import os
import numpy as np

def main():
    result = {}
    if not os.path.exists("point_attractor_num.json"):
        

        simu_num = 100
        for node_num in range(4, 8):
            for degree in range(2, 5):
                for const in range(0, 2):
                    result[f"{node_num}node_{degree}degree_{const}const"] = []
                    for sim_no in range(simu_num):
                        with open(f"Save/{node_num}node_{degree}degree_{const}const_0.5prob/attractor{sim_no}.json", "r") as f:
                            data = json.load(f)
                            
                            result[f"{node_num}node_{degree}degree_{const}const"].append(data["size_1_attractors"])

        with open("point_attractor_num.json", "w") as f:
            json.dump(result, f)
    with open("point_attractor_num.json", "r") as f:
        result = json.load(f)
    
    result_average = {}
    for node_num in range(4, 8):
        for degree in range(2, 5):
            for const in range(0, 2):
                result_average[f"{node_num}node_{degree}degree_{const}const"] = float(sum(result[f"{node_num}node_{degree}degree_{const}const"])) / len(result[f"{node_num}node_{degree}degree_{const}const"])
    
    plt.figure(figsize=(15, 6))
    plt.rcParams['font.size'] = 18  # 基本のフォントサイズを設定
    
    combinations = [f"d{d},c{c}" for d in range(2, 5) for c in range(0, 2)]
    bar_width = 0.8
    group_width = len(combinations)
    
    for i, node_num in enumerate(range(4, 8)):
        averages = []
        stds = []  # 標準偏差を格納するリスト
        for degree in range(2, 5):
            for const in range(0, 2):
                key = f"{node_num}node_{degree}degree_{const}const"
                values = result[key]
                averages.append(np.mean(values))
                stds.append(np.std(values, ddof=1) / np.sqrt(len(values)))  # 標準偏差を計算
        
        # バーの位置を計算
        x = [j + (i * (group_width + 2)) for j in range(len(combinations))]
        plt.bar(x, averages, width=bar_width, label=f"{node_num} Nodes", color=f'C{i}')
        # エラーバーとして標準偏差を追加
        plt.errorbar(x, averages, yerr=stds, fmt='none', color='black', capsize=5)

    plt.xlabel("Degree, Const combinations", fontsize=16)
    plt.ylabel("Number of Point Attractors", fontsize=16)
    
    # x軸のラベルを設定
    all_x = [j + (i * (group_width + 2)) for i in range(4) for j in range(len(combinations))]
    plt.xticks(all_x, combinations * 4, rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    
    plt.legend(fontsize=14, loc="upper right")
    plt.tight_layout()
    plt.show()

# ... rest of the code ...

if __name__ == "__main__":
    main()
