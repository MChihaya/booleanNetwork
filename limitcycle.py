import json
import matplotlib.pyplot as plt
import os
import numpy as np

def main():
    result = {}
    if not os.path.exists("limitcycle.json"):
        

        simu_num = 100
        for node_num in range(4, 8):
            for degree in range(2, 5):
                for const in range(0, 2):
                    result[f"{node_num}node_{degree}degree_{const}const"] = []
                    for sim_no in range(simu_num):
                        with open(f"Save/{node_num}node_{degree}degree_{const}const_0.5prob/attractor{sim_no}.json", "r") as f:
                            data = json.load(f)
                            for attractor in data["attractors"]:
                                result[f"{node_num}node_{degree}degree_{const}const"].append(attractor["size"])

        with open("limitcycle.json", "w") as f:
            json.dump(result, f)
    with open("limitcycle.json", "r") as f:
        result = json.load(f)
    
    result_average = {}
    for node_num in range(4, 8):
        for degree in range(2, 5):
            for const in range(0, 2):
                result_average[f"{node_num}node_{degree}degree_{const}const"] = float(sum(result[f"{node_num}node_{degree}degree_{const}const"])) / len(result[f"{node_num}node_{degree}degree_{const}const"])
    
    
    # Create a single figure
    plt.figure(figsize=(15, 6))
    plt.rcParams['font.size'] = 18  # 基本のフォントサイズを設定
    
    # Create labels for degree and const combinations
    combinations = [f"d{d},c{c}" for d in range(2, 5) for c in range(0, 2)]
    group_width = len(combinations)
    
    for i, node_num in enumerate(range(4, 8)):
        box_data = []
        for degree in range(2, 5):
            for const in range(0, 2):
                key = f"{node_num}node_{degree}degree_{const}const"
                box_data.append(result[key])
        
        # 箱ひげ図の位置を計算
        positions = [j + (i * (group_width + 2)) for j in range(len(combinations))]
        # 箱ひげ図をプロット
        bp = plt.boxplot(box_data, positions=positions, widths=0.8, 
                        patch_artist=True,  # 箱の中を塗りつぶす
                        medianprops=dict(color="black"),  # 中央値の線の色
                        flierprops=dict(marker='o', markerfacecolor='gray', markersize=4))  # 外れ値のマーカー設定
        
        # 箱の色を設定
        for box in bp['boxes']:
            box.set(facecolor=f'C{i}')  # 各ノード数で異なる色を使用
    
    plt.xlabel("Degree, Const combinations", fontsize=16)
    plt.ylabel("Attractor Size", fontsize=16)
    
    # x軸のラベルを設定
    all_x = [j + (i * (group_width + 2)) for i in range(4) for j in range(len(combinations))]
    plt.xticks(all_x, combinations * 4, rotation=45, fontsize=14)
    plt.yticks(fontsize=14)
    
    # 凡例を追加
    legend_elements = [plt.Rectangle((0,0),1,1, facecolor=f'C{i}', 
                      label=f'{n} Nodes') for i, n in enumerate(range(4,8))]
    plt.legend(handles=legend_elements, fontsize=14)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
