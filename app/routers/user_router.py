from fastapi import APIRouter, status,Form
from config import TOKEN,CHAT_IDS
from utils import send_message

user_router = APIRouter()

@user_router.post("/make-order", status_code=status.HTTP_201_CREATED)
async def make_order(
    username : str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    comment: str = Form(""),
    product_name: str = Form(...),
):
    message = f'Новый заказ❗️❗️❗️❗️ \n Данные пользователя:  \n 🙎‍♂️Имя: {username} \n 📞Телефон: {phone} \n ✉️Email: {email} \n 💬Комментарий: {comment} \n 📦Товар: {product_name} '
    await send_message(TOKEN,CHAT_IDS,message)
    return {"message":"Заказ успешно оформлен"}
