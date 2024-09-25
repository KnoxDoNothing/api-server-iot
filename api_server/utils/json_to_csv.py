import csv
from utils.path_dict import output_csv_dir



def json_to_csv(csv_name, lists): 
    output_csv_dir.mkdir(parents=True, exist_ok=True)

    csv_file_path = output_csv_dir/(csv_name+'.csv')
    
    
    # 將 JSON 資料寫入 CSV 檔案並使用 'utf-8-sig' 來自動加入 BOM,避免excel中文亂碼
    with open(csv_file_path, mode="w", newline="", encoding="utf-8-sig") as csv_file:
        fieldnames = lists[0].keys()  # 使用第一筆資料的鍵作為欄位名稱
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader() 
        writer.writerows(lists) 

