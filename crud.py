from config import session
from models import User
from security import hash_password, verify_password
from sqlalchemy import select

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    hashed_password: str

def add_user(username, password):
    new_user = User(
        username=username,
        hashed_password=password
    )
    
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

def register(username, password):

    #Проверяем, что пользователь уже зарегистрирован
    stmt = select(User).where(User.username == username)
    result = session.execute(stmt)
    user = result.scalars().first()

    if user:
        print("Пользователь уже зарегистрирован")
        return
    
    #Если не зарегестрирован, то хешируем пароль
    hashed_password = hash_password(password=password)
    if hashed_password:
        """Проверяем, что пароль успешно захешировался"""
        add_user(username=username, password=hashed_password) #Добавляем пользователя в БД

        print({"message": "Пользователь успешно зарегистрирован"})
        return

    return {"messagee": "Ошибка регистрации"}

def login(username, password):

    stmt = select(User).where(User.username == username)
    result = session.execute(stmt)
    user = result.scalars().first()

    if not user:
        print("Пользователь не зарегестрирован, пожалуйста пройдите регистрацию")
        return
    
    hashed_password = user.hashed_password #получаем хешированный пароль из БД

    if verify_password(password, hashed_password):
        print("Пользователь успешно авторизован!")
        #Блок кода, для выдачи прав доступа (токена)
        return
    else:
        print("Неверный пароль")
        return