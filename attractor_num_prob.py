import json
import matplotlib.pyplot as plt
import os
import numpy as np

def main():
    result = {}
    if not os.path.exists("attractor_num_prob.json"):
        

        simu_num = 100
        for degree in range(2, 5):
            for const in range(0, 2):
                for prob in [0.1, 0.3, 0.5, 0.7, 0.9]:
                    result[f"{degree}degree_{const}const_{prob}prob"] = []
                    for sim_no in range(simu_num):
                        with open(f"Save/4node_{degree}degree_{const}const_{prob}prob/attractor{sim_no}.json", "r") as f:
                            data = json.load(f)
                            result[f"{degree}degree_{const}const_{prob}prob"].append(len(data["attractors"]))

        with open("attractor_num_prob.json", "w") as f:
            json.dump(result, f)
    with open("attractor_num_prob.json", "r") as f:
        result = json.load(f)
    
    result_average = {}
    for degree in range(2, 5):
        for const in range(0, 2):
            for prob in [0.1, 0.3, 0.5, 0.7, 0.9]:
                result_average[f"{degree}degree_{const}const_{prob}prob"] = float(sum(result[f"{degree}degree_{const}const_{prob}prob"])) / len(result[f"{degree}degree_{const}const_{prob}prob"])
    
    plt.figure(figsize=(15, 6))
    plt.rcParams['font.size'] = 18
    
    # degree-constの組み合わせをx軸に設定
    combinations = [f"d{d},c{c}" for d in range(2, 5) for c in range(0, 2)]
    probs = [0.1, 0.3, 0.5, 0.7, 0.9]
    bar_width = 0.15
    
    for i, prob in enumerate(probs):
        averages = []
        stds = []
        for degree in range(2, 5):
            for const in range(0, 2):
                key = f"{degree}degree_{const}const_{prob}prob"
                values = result[key]
                averages.append(np.mean(values))
                stds.append(np.std(values, ddof=1) / np.sqrt(len(values)))
        
        # 各probabilityのバーの位置を計算
        x = np.arange(len(combinations)) + i * bar_width
        plt.bar(x, averages, width=bar_width, label=f'prob={prob}')
        plt.errorbar(x, averages, yerr=stds, fmt='none', color='black', capsize=5)

    plt.xlabel("Degree, Const combinations", fontsize=16)
    plt.ylabel("Number of Attractors", fontsize=16)
    
    # x軸のラベルを設定
    plt.xticks(np.arange(len(combinations)) + (bar_width * 2), combinations, fontsize=14)
    plt.yticks(fontsize=14)
    
    plt.legend(fontsize=14)
    plt.tight_layout()
    plt.show()

# ... rest of the code ...

if __name__ == "__main__":
    main()
