# main.py
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from test_runner import run_test
from descriptions import descriptions
import io
import sys
import logging
from fastapi import WebSocket
import asyncio
from multiprocessing import Queue as mpQueue
from multiprocessing import Manager
from queue import Empty
from fastapi.websockets import WebSocketDisconnect


# --- صف لاگ برای Process ها ---
manager = Manager()
log_queue = manager.Queue()

#--- هندلر لاگ اختصاصی اضافه شد که لاگ‌ها رو داخل log_queue بذاره---
class WebSocketLogHandler(logging.Handler):
    def __init__(self, queue: mpQueue):
        super().__init__()
        if queue is None:
            raise ValueError("log_queue cannot be None")
        self.queue = queue

    def emit(self, record):
        msg = self.format(record)
        self.queue.put(msg)


# --- تنظیمات Logger ---
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# جلوگیری از اضافه شدن هندلر تکراری
if not logger.handlers:
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    ws_handler = WebSocketLogHandler(log_queue)
    ws_handler.setFormatter(formatter)
    logger.addHandler(ws_handler)


# --- FastAPI ---
app = FastAPI(
    title="Parallel Processing API",
    description="Run thread/process-based scenarios via FastAPI",
    version="1.0"
)

# --- برای فعال کردن دسترسی از مرورگر محلی---
#وارنینگ middleware نوع type-check است و می‌توان آن را نادیده گرفت
app.add_middleware( # type: ignore[arg-type]
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- سرو کردن فایل‌های استاتیک از پوشه static---
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
def serve_index():
    with open("static/index.html", encoding="utf-8") as f:
        return f.read()

# --- Run Scenario ---
@app.get("/run")
def run_scenario(
    section: int = Query(..., ge=1, le=8, description="Section number (1 to 8)"),
    scenario: int = Query(..., ge=1, le=3, description="Scenario number (1 to 3)"),
    mode: str = Query(..., regex="^(thread|process)$", description="Execution mode: thread or process")
):
    output = []

    buffer = None
    sys_stdout = None

    if mode == "thread":
        # فقط برای thread stdout را بگیریم
        buffer = io.StringIO()
        sys_stdout = sys.stdout
        sys.stdout = buffer



    try:
        run_test(section, scenario, mode, log_queue=log_queue)
        if mode == "thread":
            sys.stdout = sys_stdout
            output = buffer.getvalue().splitlines()

        desc = descriptions[mode][section][scenario] # توضیحات

        if mode == "process":
            output = ["Logs will be streamed via WebSocket"]

        return {
            "success": True,
            "output": output,
            "description": desc
        }


    except KeyError:
        if mode == "thread" and sys_stdout is not None:
            sys.stdout = sys_stdout
        return {"success": False, "error": "Invalid section or scenario number!"}


    except Exception as e:
        if mode == "thread":
            sys.stdout = sys_stdout
        return {"success": False, "error": str(e)}

# --- WebSocket برای Process ها ---
@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
    await websocket.accept()
    print("WebSocket connected")  # برای دیباگ
    try:
        while True:
            try:
                msg = log_queue.get_nowait()  # غیربلوکینگ
                print(
                    f"Sending to WebSocket: {msg}, Queue size: {log_queue.qsize()}")  #  اضافه کردن برای دیباگ اندازه صف
                await websocket.send_text(msg)
            except Empty:
                await asyncio.sleep(0.1)  # صبر کوتاه برای چک بعدی
            except WebSocketDisconnect:  #  مدیریت قطع اتصال توسط کلاینت
                print("WebSocket disconnected by client")
                break
            except Exception as e:  #  اصلاح خطای سینتکسی (حذف پرانتز اضافی)
                print(f"WebSocket error: {e}")
                break
    finally:
     print("WebSocket closed")  #  تغییر ترتیب برای چاپ پیام قبل از بستن
     await websocket.close()