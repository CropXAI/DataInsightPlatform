from supabase import create_client, Client
import pandas as pd

# Настройка доступа к Supabase
url = "*"  # URL проекта Supabase
key = "*"  # Секретный ключ API
supabase: Client = create_client(url, key)

# Функция для получения данных из таблицы
def fetch_data_from_supabase(table_name):
    # Получаем данные из таблицы
    response = supabase.table(table_name).select("*").execute()
    

    data = response.data  # Список словарей
    df = pd.DataFrame(data)
    return df
  
