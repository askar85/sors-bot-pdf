import os
import fitz  # PyMuPDF
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pdf2docx import Converter
import zipfile
import sqlite3
from PIL import Image
import asyncio


  #این ربات رایگان ساخته شده است برای مردم کشورم 
  #سازنده مستر ربات 
  # ایدی تلگرام سازنده برای  نظر یا ایده برای ساخت ربات بصورت رایگان در صورت کمک به مردم کشورم باشه = @MRROBOT_DT

              
api_id = ''     # api id
api_hash = ''   # api  hash
bot_token = ""   #token bot

app = Client("pdf_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
DATABASE = "pdf_files.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS pdf_files (
                      user_id INTEGER,
                      file_name TEXT,
                      file_data BLOB
                      )''')
    conn.commit()
    conn.close()

def save_pdf_to_db(user_id, file_name, file_data):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pdf_files (user_id, file_name, file_data) VALUES (?, ?, ?)",
                   (user_id, file_name, file_data))
    conn.commit()
    conn.close()

def get_pdfs_from_db(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT file_name, file_data FROM pdf_files WHERE user_id=?", (user_id,))
    files = cursor.fetchall()
    conn.close()
    return files

def delete_pdfs_from_db(user_id):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM pdf_files WHERE user_id=?", (user_id,))
    conn.commit()
    conn.close()
    
    
      #این ربات رایگان ساخته شده است برای مردم کشورم 
  #سازنده مستر ربات 
  # ایدی تلگرام سازنده برای  نظر یا ایده برای ساخت ربات بصورت رایگان در صورت کمک به مردم کشورم باشه = @MRROBOT_DT
    

init_db()
WELCOME_MESSAGE = """
سلام، به بات PDF خوش آمدید! 📄

اینجا محلی است که شما می‌توانید فایل‌های PDF خود را مدیریت کنید و به صورت ساده و سریع انواع عملیات روی آنها انجام دهید.

از منوی زیر یکی از دستورات را انتخاب کنید:

برای بهترین استفاده از ربات و یادگیری کامل به قسمت راهنما ربات بروید 
"""

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 ذخیره فایل PDF", callback_data="save_pdf")],
        [InlineKeyboardButton("ℹ️ راهنما", callback_data="help")],
        [InlineKeyboardButton("📚 لیست ربات‌ها", callback_data="list_bots")],
        [InlineKeyboardButton("💬 پشتیبانی", url="https://t.me/MRROBOT_DT")],
    ])

def back_to_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⬅️ بازگشت به منوی اصلی", callback_data="main_menu")]
    ])

@app.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    await message.reply(WELCOME_MESSAGE, reply_markup=main_menu())

@app.on_callback_query(filters.regex("main_menu"))
async def show_main_menu(client: Client, callback_query):
    await callback_query.message.edit(WELCOME_MESSAGE, reply_markup=main_menu())


  #این ربات رایگان ساخته شده است برای مردم کشورم 
  #سازنده مستر ربات 
  # ایدی تلگرام سازنده برای  نظر یا ایده برای ساخت ربات بصورت رایگان در صورت کمک به مردم کشورم باشه = @MRROBOT_DT



@app.on_callback_query(filters.regex("help"))
async def show_help(client: Client, callback_query):
    HELP_COMMAND = """
    راهنمای استفاده از بات: ℹ️

    ⚠️ حتماً قبل از استفاده از دستورها، فایل‌های خود را با دستور 📥 ذخیره کنید.

    📥 - برای ذخیره کردن فایل‌های PDF. ابتدا فایل PDF خود را ارسال کنید، سپس دستور ذخیره را انتخاب کنید.
    📝 - برای ادغام فایل‌های PDF به یک فایل. ابتدا حداقل دو فایل PDF را ذخیره کنید و سپس این گزینه را انتخاب کنید.
    ✂️ - برای جداسازی صفحات فایل‌های PDF. ابتدا یک فایل PDF را ذخیره کنید و سپس این گزینه را انتخاب کنید.
    🔄 - برای تبدیل فایل‌های PDF به فرمت DOCX. ابتدا یک فایل PDF را ذخیره کنید و سپس این گزینه را انتخاب کنید.
    🖼️ - برای تبدیل فایل‌های PDF به تصویر. ابتدا یک فایل PDF را ذخیره کنید و سپس این گزینه را انتخاب کنید.

    با انتخاب هر گزینه، بات به شما پاسخ خواهد داد و فرآیند مورد نظر را انجام خواهد داد. در صورتی که نیاز به راهنمایی بیشتر دارید، می‌توانید با مراجعه به پشتیبانی در تماس باشید.

    ᴛᴏ ʙᴇ ᴏʀ ɴᴏᴛ ᴛᴏ ʙᴇ...🥀
    """
    await callback_query.message.edit(HELP_COMMAND, reply_markup=back_to_main_menu())

@app.on_callback_query(filters.regex("list_bots"))
async def show_list_bots(client: Client, callback_query):
    LIST_BOTS = """
    لیست ربات‌های مستر ربات

    ᴛᴏ ʙᴇ ᴏʀ ɴᴏᴛ ᴛᴏ ʙᴇ...🥀
    """
    list_bots_menu = InlineKeyboardMarkup([
        [InlineKeyboardButton("1️⃣  ربات چت هوش مصنوعی  👾", url="https://t.me/Gpt_MrRobot")],
        [InlineKeyboardButton("2️⃣  ربات مدیریت پی دی اف - 📄", url="https://t.me/PDF_MRROBOT")],
        [InlineKeyboardButton("3️⃣  ربات تبدیل متن به عکس هوش مصنوعی - 📷", url="https://t.me/text2img_MRROBOT")],
        [InlineKeyboardButton("⬅️ بازگشت به منوی اصلی", callback_data="main_menu")]
    ])
    await callback_query.message.edit(LIST_BOTS, reply_markup=list_bots_menu, disable_web_page_preview=True)

@app.on_callback_query(filters.regex("save_pdf"))
async def save_pdf_callback(client: Client, callback_query):
    user_id = callback_query.from_user.id
    await callback_query.message.reply("لطفاً فایل‌های PDF خود را ارسال کنید.", reply_markup=back_to_main_menu())

@app.on_message(filters.document & filters.private)
async def receive_pdf(client: Client, message: Message):
    if message.document.mime_type == "application/pdf":
        user_id = message.from_user.id
        status_message = await message.reply("در حال دانلود فایل، لطفاً صبور باشید...")
        
        try:
            pdf_data = await message.download()
            file_name = message.document.file_name
            
            # Convert file data to bytes
            with open(pdf_data, 'rb') as f:
                file_data = f.read()
            
            save_pdf_to_db(user_id, file_name, file_data)
            
            await status_message.edit(f"فایل {file_name} ذخیره شد.")
            
            tools_menu = InlineKeyboardMarkup([
                [InlineKeyboardButton("📝 ادغام PDF(مخلوط )", callback_data="merge_pdfs")],
                [InlineKeyboardButton("✂️ جداسازی صفحات PDF (زوج و فرد )", callback_data="split_pdfs")],
                [InlineKeyboardButton("🔄 تبدیل PDF به DOCX (word)", callback_data="pdf_to_docx")],
                [InlineKeyboardButton("🖼️ تبدیل PDF به تصویر", callback_data="pdf_to_image")],
                [InlineKeyboardButton("⬅️ بازگشت به منوی اصلی", callback_data="main_menu")]
            ])
            
            await message.reply("فایل دیگری ارسال کنید یا یک عملیات را انتخاب کنید.", reply_markup=tools_menu)
        except Exception as e:
            await status_message.edit(f"خطایی رخ داد: {e}")
    else:
        await message.reply("لطفاً فقط فایل‌های PDF ارسال کنید.")


@app.on_callback_query(filters.regex("merge_pdfs"))
async def merge_pdfs_callback(client: Client, callback_query):
    user_id = callback_query.from_user.id
    pdf_files = get_pdfs_from_db(user_id)
    
    if len(pdf_files) < 2:
        await callback_query.message.reply("حداقل دو فایل PDF برای ادغام نیاز است.")
        return
    
    output_pdf_path = f"{user_id}_merged.pdf"
    merger = fitz.open()
    status_message = await callback_query.message.reply("در حال ادغام فایل‌ها، لطفاً صبور باشید...")
    
    try:
        for file_name, file_data in pdf_files:
            with open(file_name, 'wb') as f:
                f.write(file_data)
            merger.insert_pdf(fitz.open(file_name))
        
        merger.save(output_pdf_path)
        await status_message.edit("ادغام فایل‌ها تکمیل شد. در حال ارسال فایل نهایی، لطفاً صبور باشید...")
        
        await callback_query.message.reply_document(output_pdf_path, caption="فایل‌های شما با موفقیت ادغام شدند.", reply_markup=back_to_main_menu())
    except Exception as e:
        await status_message.edit(f"خطایی رخ داد: {e}")
    finally:
        for file_name, _ in pdf_files:
            os.remove(file_name)
        if os.path.exists(output_pdf_path):
            os.remove(output_pdf_path)
        
        delete_pdfs_from_db(user_id)
        
        # Deleting files from the download directory
        for file_name, _ in pdf_files:
            if os.path.exists(file_name):
                os.remove(file_name)

@app.on_callback_query(filters.regex("split_pdfs"))
async def split_pdfs_callback(client: Client, callback_query):
    user_id = callback_query.from_user.id
    pdf_files = get_pdfs_from_db(user_id)
    
    if len(pdf_files) == 0:
        await callback_query.message.reply("هیچ فایل PDF برای جداسازی یافت نشد.")
        return
    
    pdf_file = pdf_files[0]
    file_name, file_data = pdf_file
    split_pdf_path = f"{user_id}_split"
    
    if not os.path.exists(split_pdf_path):
        os.makedirs(split_pdf_path)
    
    with open(file_name, 'wb') as f:
     f.write(bytes(file_data))

    
    pdf_document = fitz.open(file_name)
    status_message = await callback_query.message.reply("در حال جداسازی صفحات، لطفاً صبور باشید...")
    
    try:
        for page_num in range(len(pdf_document)):
            pdf_writer = fitz.open()
            pdf_writer.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
            output_path = os.path.join(split_pdf_path, f"{user_id}_page_{page_num + 1}.pdf")
            pdf_writer.save(output_path)
        
        await status_message.edit("جداسازی صفحات تکمیل شد. در حال ارسال فایل‌های نهایی، لطفاً صبور باشید...")
        
        zip_file_path = f"{split_pdf_path}.zip"
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for root, _, files in os.walk(split_pdf_path):
                for file in files:
                    zipf.write(os.path.join(root, file), file)
        
        await callback_query.message.reply_document(zip_file_path, caption="صفحات شما با موفقیت جداسازی شدند.", reply_markup=back_to_main_menu())
    except Exception as e:
        await status_message.edit(f"خطایی رخ داد: {e}")
    finally:
        os.remove(file_name)
        for root, _, files in os.walk(split_pdf_path):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(split_pdf_path)
        os.remove(zip_file_path)
        
        delete_pdfs_from_db(user_id)
        
        for file_name, _ in pdf_files:
            if os.path.exists(file_name):
                os.remove(file_name)

@app.on_callback_query(filters.regex("pdf_to_docx"))
async def pdf_to_docx_callback(client: Client, callback_query):
    user_id = callback_query.from_user.id
    pdf_files = get_pdfs_from_db(user_id)
    
    if len(pdf_files) == 0:
        await callback_query.message.reply("هیچ فایل PDF برای تبدیل یافت نشد.")
        return
    
    pdf_file = pdf_files[0]
    file_name, file_data = pdf_file
    docx_file_name = file_name.replace('.pdf', '.docx')
    
    with open(file_name, 'wb') as f:
        f.write(file_data)
    
    status_message = await callback_query.message.reply("در حال تبدیل PDF به DOCX، لطفاً صبور باشید...")
    
    try:
        cv = Converter(file_name)
        cv.convert(docx_file_name, start=0, end=None)
        cv.close()
        
        await status_message.edit("تبدیل PDF به DOCX تکمیل شد. در حال ارسال فایل نهایی، لطفاً صبور باشید...")
        
        await callback_query.message.reply_document(docx_file_name, caption="فایل PDF شما با موفقیت به DOCX تبدیل شد.", reply_markup=back_to_main_menu())
    except Exception as e:
        await status_message.edit(f"خطایی رخ داد: {e}")
    finally:
        os.remove(file_name)
        os.remove(docx_file_name)
        
        delete_pdfs_from_db(user_id)
        for file_name, _ in pdf_files:
            if os.path.exists(file_name):
                os.remove(file_name)



@app.on_callback_query(filters.regex("pdf_to_image"))
async def pdf_to_image_callback(client: Client, callback_query):
    user_id = callback_query.from_user.id
    pdf_files = get_pdfs_from_db(user_id)
    
    if len(pdf_files) == 0:
        await callback_query.message.reply("هیچ فایل PDF برای تبدیل یافت نشد.")
        return
    
    pdf_file = pdf_files[0]
    file_name, file_data = pdf_file
    images_path = f"{user_id}_images"
    
    if not os.path.exists(images_path):
        os.makedirs(images_path)
    
    with open(file_name, 'wb') as f:
        f.write(file_data)
    
    pdf_document = fitz.open(file_name)
    status_message = await callback_query.message.reply("در حال تبدیل PDF به تصاویر، لطفاً صبور باشید...")
    
    try:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            pix = page.get_pixmap()
            output_path = os.path.join(images_path, f"{user_id}_page_{page_num + 1}.png")
            pix.save(output_path)
        
        await status_message.edit("تبدیل PDF به تصاویر تکمیل شد. در حال ارسال فایل‌های نهایی، لطفاً صبور باشید...")
        
        zip_file_path = f"{images_path}.zip"
        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for root, _, files in os.walk(images_path):
                for file in files:
                    zipf.write(os.path.join(root, file), file)
        
        await callback_query.message.reply_document(zip_file_path, caption="تصاویر شما با موفقیت تبدیل شدند.", reply_markup=back_to_main_menu())
    except Exception as e:
        await status_message.edit(f"خطایی رخ داد: {e}")
    finally:
        os.remove(file_name)
        for root, _, files in os.walk(images_path):
            for file in files:
                os.remove(os.path.join(root, file))
        os.rmdir(images_path)
        os.remove(zip_file_path)
        
        delete_pdfs_from_db(user_id)

        for file_name, _ in pdf_files:
            if os.path.exists(file_name):
                os.remove(file_name)

app.run()
