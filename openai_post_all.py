import json
import openai
import os
import re

# PS momo,pc有四個地方要換, 用text-davinci-003才能跑
# 讀取 json 文件
with open('pchome_try.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

# 設置 api_key
openai.api_key = os.getenv("OPENAI_API_KEY")

# 輸入prompt, 給範例
prompt = "是一個電商的行銷po文內容的json檔案, 格式為{'PChome': ['po文內容','po文內容','po文內容'...]} , 請你一個一個po文內容讀取, 預測電商平台可能會有的產品類別, '3C'、'家電'、'運動健身'、'日用品'、'書店'、'時尚美妝'、'美食'、'活動合作'、'無法分類'..., 產品類別不要重複, '3c'和'3C'視為一樣, 顯示'3C'就好。格式為{'產品類別':'po文內容','產品類別':'po文內容'...}, 範例為{'美妝':' 5小時  · 分享對象：所有人最新推出的Beauty Box美妝盒要來啦 #一樓有驚喜本期由頭皮養護專業的「艾瑪絲」推出$499超值禮盒從頭到腳一組搞定，深入調理頭皮徹底清潔更… 顯示更多點擊可查看商品所有心情：476 476459443讚留言分享'}"

# 儲存在json
results = []

# 找到預測的產品類別
for post in data["PChome"]:
    # 使用 text-davinci-003 模型 
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt + f"{post}",
        max_tokens=100
    )

    # 提取生成的文本
    generated_text = response.choices[0].text.strip()

    # 從文本中提取產品類別
    categories = re.findall(r"'([^']*)'", generated_text)

    # 創一個空字典
    result = {}

    # {產品類別:Po文}
    result[categories[0]] = post

    # append到 results = []
    results.append(result)

# 將結果列表轉換為JSON格式
json_results = json.dumps(results, ensure_ascii=False, indent=4)

# 印出 json 結果
print(json_results)

# 寫入json 文件
with open('pc_post_all_try.json', 'w', encoding='utf-8') as outfile:
    json.dump(results, outfile, ensure_ascii=False, indent=4)