import duckdb
import os
from pathlib import Path
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import pandas as pd
import numpy as np

# PostgreSQL bağlantı bilgileri
PG_HOST = os.getenv('POSTGRES_HOST', 'postgres')
PG_PORT = os.getenv('POSTGRES_PORT', '5432')
PG_DB = os.getenv('POSTGRES_DB', 'am4db')
PG_USER = os.getenv('POSTGRES_USER', 'admin')
PG_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'admin123')

def create_tables():
    """PostgreSQL'de tabloları oluştur"""
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    try:
        # Airports tablosu
        cur.execute("""
        DROP TABLE IF EXISTS airports;
        CREATE TABLE airports (
            id INTEGER PRIMARY KEY,
            name VARCHAR(255),
            fullname VARCHAR(255),
            country VARCHAR(100),
            continent VARCHAR(50),
            iata VARCHAR(10),
            icao VARCHAR(10),
            lat DECIMAL(10,6),
            lng DECIMAL(10,6),
            rwy INTEGER,
            market INTEGER,
            hub_cost DECIMAL(12,2),
            rwy_codes TEXT
        )
        """)

        # Aircrafts tablosu
        cur.execute("""
        DROP TABLE IF EXISTS aircrafts;
        CREATE TABLE aircrafts (
            id INTEGER PRIMARY KEY,
            shortname VARCHAR(50),
            manufacturer VARCHAR(100),
            name VARCHAR(100),
            type VARCHAR(50),
            priority INTEGER,
            eid INTEGER,
            ename VARCHAR(100),
            speed INTEGER,
            fuel DECIMAL(10,2),
            co2 DECIMAL(10,2),
            cost DECIMAL(12,2),
            capacity INTEGER,
            rwy INTEGER,
            check_cost DECIMAL(12,2),
            range INTEGER,
            ceil INTEGER,
            maint DECIMAL(12,2),
            pilots INTEGER,
            crew INTEGER,
            engineers INTEGER,
            technicians INTEGER,
            img TEXT,
            wingspan DECIMAL(10,2),
            length DECIMAL(10,2)
        )
        """)

        # Routes tablosu
        cur.execute("""
        DROP TABLE IF EXISTS routes;
        CREATE TABLE routes (
            yd INTEGER,
            jd INTEGER,
            fd INTEGER,
            d DECIMAL(10,2)
        )
        """)

        print("Tablolar başarıyla oluşturuldu!")
    except Exception as e:
        print(f"Tablo oluşturma hatası: {str(e)}")
    finally:
        cur.close()
        conn.close()

def clean_dataframe(df, table_name):
    """DataFrame'i temizle ve hazırla"""
    # NaN değerleri temizle
    df = df.replace({np.nan: None})
    
    # String sütunlarındaki boşlukları temizle
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Tekrarlanan ID'leri temizle
    if 'id' in df.columns:
        df = df.drop_duplicates(subset=['id'], keep='first')
    
    return df

def wait_for_postgres():
    """PostgreSQL'in hazır olmasını bekle"""
    max_retries = 30
    retry_interval = 2

    for i in range(max_retries):
        try:
            conn = psycopg2.connect(
                host=PG_HOST,
                port=PG_PORT,
                database=PG_DB,
                user=PG_USER,
                password=PG_PASSWORD
            )
            conn.close()
            print("PostgreSQL bağlantısı başarılı!")
            return True
        except Exception as e:
            print(f"PostgreSQL'e bağlanılamıyor, {retry_interval} saniye sonra tekrar denenecek... ({i+1}/{max_retries})")
            time.sleep(retry_interval)
    
    return False

def import_parquet_to_postgres():
    """Parquet dosyalarını PostgreSQL'e aktar"""
    if not wait_for_postgres():
        print("PostgreSQL'e bağlanılamadı. İşlem iptal ediliyor.")
        return

    # Tabloları oluştur
    create_tables()

    # PostgreSQL bağlantısı
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )
    cur = conn.cursor()
    
    # Parquet dosyalarının bulunduğu dizin
    data_dir = Path("/data")
    
    # Her bir parquet dosyası için
    parquet_files = {
        'airports.parquet': 'airports',
        'aircrafts.parquet': 'aircrafts',
        'routes.parquet': 'routes'
    }
    
    for parquet_file, table_name in parquet_files.items():
        file_path = data_dir / parquet_file
        if not file_path.exists():
            print(f"Uyarı: {parquet_file} dosyası bulunamadı!")
            continue
            
        print(f"{parquet_file} dosyası {table_name} tablosuna aktarılıyor...")
        
        try:
            # Parquet dosyasını pandas ile oku
            df = pd.read_parquet(file_path)
            print(f"Parquet dosyasından {len(df)} kayıt okundu")
            print(f"Sütunlar: {', '.join(df.columns)}")
            
            # DataFrame'i temizle
            df = clean_dataframe(df, table_name)
            print(f"Temizleme sonrası {len(df)} kayıt kaldı")
            
            # Tablo sütunlarını al
            cur.execute(f"""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
            """)
            table_columns = [row[0] for row in cur.fetchall()]
            print(f"Tablo sütunları: {', '.join(table_columns)}")
            
            # DataFrame'i PostgreSQL'e aktar
            columns = ','.join(df.columns)
            values = ','.join(['%s' for _ in df.columns])
            
            insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
            
            # Veriyi batch'ler halinde aktar
            batch_size = 1000
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                cur.executemany(insert_query, batch.values.tolist())
                conn.commit()
                print(f"Batch aktarıldı: {i+1} - {min(i+batch_size, len(df))}")
            
            # Kayıt sayısını kontrol et
            cur.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cur.fetchone()[0]
            print(f"{table_name} tablosuna toplam {count} kayıt aktarıldı")
            
        except Exception as e:
            print(f"Hata: {table_name} tablosuna veri aktarılırken hata oluştu:")
            print(str(e))
            conn.rollback()
    
    cur.close()
    conn.close()
    print("Tüm veriler başarıyla aktarıldı!")

if __name__ == "__main__":
    import_parquet_to_postgres() 