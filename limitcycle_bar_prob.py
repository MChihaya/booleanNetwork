import json
import matplotlib.pyplot as plt
import os
import numpy as np

def main():
    result = {}
    if not os.path.exists("limitcycle_prob.json"):
        

        simu_num = 100
        for degree in range(2, 5):
            for const in range(0, 2):
                for prob in [0.1, 0.3, 0.5, 0.7, 0.9]:
                    result[f"{degree}degree_{const}const_{prob}prob"] = []
                    for sim_no in range(simu_num):
                        with open(f"Save/4node_{degree}degree_{const}const_{prob}prob/attractor{sim_no}.json", "r") as f:
                            data = json.load(f)
                            for attractor in data["attractors"]:
                                result[f"{degree}degree_{const}const_{prob}prob"].append(attractor["size"])

        with open("limitcycle_prob.json", "w") as f:
            json.dump(result, f)
    with open("limitcycle_prob.json", "r") as f:
        result = json.load(f)
    
    result_average = {}
    
    for degree in range(2, 5):
        for const in range(0, 2):
            for prob in [0.1, 0.3, 0.5, 0.7, 0.9]:
                result_average[f"{degree}degree_{const}const_{prob}prob"] = float(sum(result[f"{degree}degree_{const}const_{prob}prob"])) / len(result[f"{degree}degree_{const}const_{prob}prob"])
    
    
    # Create a single figure
    plt.figure(figsize=(15, 6))
    plt.rcParams['font.size'] = 18
    
    combinations = [f"d{d},c{c}" for d in range(2, 5) for c in range(0, 2)]
    group_width = len(combinations)
    
    bar_width = 0.15  # バーの幅を設定
    
    for i, prob in enumerate([0.1, 0.3, 0.5, 0.7, 0.9]):
        means = []
        errors = []
        for degree in range(2, 5):
            for const in range(0, 2):
                key = f"{degree}degree_{const}const_{prob}prob"
                means.append(np.mean(result[key]))
                errors.append(np.std(result[key]) / np.sqrt(len(result[key])))  # 標準誤差を計算
        
        # バーの位置を計算
        positions = [j + (i * bar_width) for j in range(len(combinations))]
        # エラーバー付きの棒グラフをプロット
        plt.bar(positions, means, bar_width, 
               label=f'probability={prob}',
               color=f'C{i}',
               alpha=0.9)
        plt.errorbar(positions, means, yerr=errors, 
                    fmt='none', 
                    color='black', 
                    capsize=3)
    
    plt.xlabel("Degree, Const combinations", fontsize=16)
    plt.ylabel("Average Attractor Size", fontsize=16)
    
    # x軸のラベルを設定
    plt.xticks(np.arange(len(combinations)) + bar_width * 2, 
               combinations, 
               rotation=45, 
               fontsize=14)
    plt.yticks(fontsize=14)
    
    plt.legend(fontsize=14, loc = "lower left")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
