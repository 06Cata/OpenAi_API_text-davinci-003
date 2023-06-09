import json
import openai
import os
import re

# PS momo,pc有四個地方要換, 用text-davinci-003才能跑
# 讀取 json 文件
with open('momo2.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 設置 api_key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 輸入prompt, 給範例
prompt = "是一個電商的行銷po文內容的json檔案, 格式為{'momo': ['po文內容','po文內容','po文內容'...]} , 請你一個一個po文內容讀取, 預測電商平台可能會有的產品類別, '3c'、'家電'、'運動'、'日用品'、'生活'、'聊天'、'書籍'、'美妝'、'保養'、'時尚精品'、'旅遊度假'、'美食'、'活動合作'、'無法分類'..., 只告訴我產品類別和各類產品的'總數', 格式為[{'產品類別1':總數},{'產品類別2':總數}],產品類別不要重複, '3c'和'3C'視為一樣, 顯示'3C'就好, po文判斷就好不要顯示"

# 儲存在json
results = {}

# 找到預測的產品類別
for post in data["momo"]:
    # 使用 text-davinci-003 模型生成文本
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt + f"{post}",
        max_tokens=100
    )

    # 提取產品類別
    generated_text = response.choices[0].text.strip()
    generated_category = re.search(r"'([^']*)'", generated_text)
    if generated_category:
        generated_category = generated_category.group(1)
    else:
        generated_category = "其他"

    # 加到字典, 如果產品類別存在就+1
    if generated_category in results:
        results[generated_category] += 1
    else:
        results[generated_category] = 1

# 印出 json 結果 
formatted_results = [{category: count} for category, count in results.items()]
print(json.dumps(formatted_results, ensure_ascii=False, indent=4))

# 寫入json 文件
with open('momo_result.json', 'w', encoding='utf-8') as outfile:
    json.dump(formatted_results, outfile, ensure_ascii=False, indent=4)