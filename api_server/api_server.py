from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from utils.csv_to_pdf import csv_to_pdf, csv_to_pdf_with_watermark
from utils.json_to_csv import json_to_csv
import textwrap
from os import remove
from utils.path_dict import output_pdf_dir, root_dir
import yaml


app = FastAPI()

config_path = root_dir / "config.yaml"
with open(config_path, "r") as f:
    config = yaml.safe_load(f)
# 設定允許的來源 (origins)
origins = config["cors"]["origins"]

# 加入 CORS 中介軟體
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 設定允許的來源
    allow_credentials=True,  # 允許傳送 Cookie
    allow_methods=["*"],  # 允許的 HTTP 方法，如 GET、POST 等
    allow_headers=["*"],  # 允許的 HTTP 標頭
)


class DataList(BaseModel):
    name: str
    lists: list


@app.get("/")
def read_root():
    return {"result": "Get OK"}


@app.post("/api/datalist")
async def create_datalist(datalist: DataList):
    try:

        # 過濾出需要的資料
        # textwrap.fill將字串格式化，每行最多 25個字符，自動換行
        filtered_lists = [
            {
                "顯示名稱": item["displayName"],
                "狀態": item["state"],
                "數值": item["value"],
                "燈號": item["itemState"],
                "狀態敘述": textwrap.fill(item["comment"], width=25),
                "時間": item["time"],
            }
            for item in datalist.lists
        ]
        json_to_csv(datalist.name, filtered_lists)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    return {"result": "Done"}


@app.post("/api/datalist_pdf")
async def create_datalist_pdf(datalist: DataList):
    try:

        # 過濾出需要的資料
        # textwrap.fill將字串格式化，每行最多 25個字符，自動換行
        filtered_lists = [
            {
                "顯示名稱": item["displayName"],
                "狀態": item["state"],
                "數值": item["value"],
                "燈號": item["itemState"],
                "狀態敘述": textwrap.fill(item["comment"], width=25),
                "時間": item["time"],
            }
            for item in datalist.lists
        ]

        json_to_csv(datalist.name, filtered_lists)
        csv_to_pdf(datalist.name)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    return {"result": "Done"}


@app.post("/api/datalist_pdf_watermark")
async def create_datalist_pdf_watermark(datalist: DataList):
    try:
        # 過濾出需要的資料
        # textwrap.fill將字串格式化，每行最多 25個字符，自動換行
        filtered_lists = [
            {
                "顯示名稱": item["displayName"],
                "狀態": item["state"],
                "數值": item["value"],
                "燈號": item["itemState"],
                "狀態敘述": textwrap.fill(item["comment"], width=25),
                "時間": item["time"],
            }
            for item in datalist.lists
        ]

        json_to_csv(datalist.name, filtered_lists)
        csv_to_pdf_with_watermark(datalist.name, mode="text")

        remove(output_pdf_dir / (datalist.name + ".pdf"))
        remove(output_pdf_dir / ("watermark" + ".pdf"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    return {"result": "Done"}


@app.post("/api/datalist_pdf_watermark_image")
async def create_datalist_pdf_watermark(datalist: DataList):
    try:
        # 過濾出需要的資料
        # textwrap.fill將字串格式化，每行最多 25個字符，自動換行
        filtered_lists = [
            {
                "顯示名稱": item["displayName"],
                "狀態": item["state"],
                "數值": item["value"],
                "燈號": item["itemState"],
                "狀態敘述": textwrap.fill(item["comment"], width=25),
                "時間": item["time"],
            }
            for item in datalist.lists
        ]

        json_to_csv(datalist.name, filtered_lists)
        csv_to_pdf_with_watermark(datalist.name, mode="image")

        remove(output_pdf_dir / (datalist.name + ".pdf"))
        remove(output_pdf_dir / ("watermark" + ".pdf"))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
    return {"result": "Done"}
