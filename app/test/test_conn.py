from sqlalchemy import create_engine, text

url = "postgresql://postgres:dNXZOACpHGpOeFvcVXDKcTKVrNpyfsMn@crossover.proxy.rlwy.net:42781/railway"

engine = create_engine(url)

with engine.connect() as conn:
    result = conn.execute(text("SELECT 1"))
    print(result.fetchone())
    print("Connection successful")

# run command: python app.test.test_conn

