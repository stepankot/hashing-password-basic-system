from passlib.context import CryptContext

PAPPER = "M9Hotp@ssword"

#Создаем функцию, которая будет применять паппер

#Создаем CryptContext, который будет использоваться для шифрования паролей
pwd_context = CryptContext(
    schemes=["argon2"],
    default="argon2",
    deprecated="auto",
    argon2__memory_cost=102400, #объем памяти
    argon2__time_cost=3, #Кол-во итераций
    argon2__parallelism=4, #Параллельность
    argon2__type="ID",
)

#Создаем функцию, которая будет применять паппер
def _apply_papper(password: str) -> str:
    if PAPPER:
        return password + PAPPER
    return password

#Создаем функцию, которая будет хэшировать пароль
def hash_password(password: str) -> str:
    """Хешируем пароль"""
    if password:
        return pwd_context.hash(_apply_papper(password))
    
    return None

#Функция, которая проверяет пароль.
#Хешированный пароль будем брать из БД
def verify_password(password: str, hashed_password: str) -> bool:
    """Проверяем пароли если совпадают вернёт true"""
    if password and hashed_password:
        return pwd_context.verify(_apply_papper(password), hashed_password)
    
    return False

#
def needs_rehash(hashed: str) -> bool:
    """
    Проверяет, нужно ли пересчитать хеш под новыми параметрами.
    Полезно делать при логине: если True — ре-хешируем и сохраняем новый в БД.
    """
    try:
        return pwd_context.needs_update(hashed)
    except ValueError:
        return True  # если не знаем алгоритм — лучше перехешировать