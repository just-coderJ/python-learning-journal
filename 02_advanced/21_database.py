"""
=========================================================
📚 模块: 21 数据库访问
💡 核心对比：
1. sqlite3：DB-API 标准接口，手写 SQL，注意 commit 提交事务（类似 Java JDBC）。
2. SQLAlchemy：全栈 ORM，类对应表、实例对应行（类似 Hibernate/JPA）。
=========================================================
"""
import sqlite3

print("--- 1. SQLite 原生操作 ---")
# 任务 1：连接 test.db，创建 user 表（id 主键，name 字段）。
# 任务 2：用 execute 参数化插入数据，并调用 commit 提交。
# 任务 3：执行 select 查询，将结果转为字典列表返回。

conn = sqlite3.connect('../test/test.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS user (
        id TEXT PRIMARY KEY,
        name TEXT
    )
''')

cursor.execute('INSERT OR REPLACE INTO user (id, name) VALUES (?, ?)', ('1', 'Alice'))
cursor.execute('INSERT OR REPLACE INTO user (id, name) VALUES (?, ?)', ('2', 'Bob'))
conn.commit() # 必须提交，否则数据不会真正写入文件

cursor.execute('SELECT id, name FROM user')
rows = cursor.fetchall()

columns = [col[0] for col in cursor.description]
dict_list = [dict(zip(columns, row)) for row in rows]
print(f"原生查询结果 (字典列表): {dict_list}")

cursor.close()
conn.close()

print("\n--- 2. SQLAlchemy ORM 快速体验 ---")
# （需先 pip install sqlalchemy）
# 任务 4：用 declarative_base 定义 User 映射类。
# 任务 5：创建 DBSession，通过 session.add() 添加记录并 commit。
# 任务 6：用 session.query(User).filter(...).one() 查询。

Base = declarative_base()

class UserORM(Base):
    __tablename__ = 'user_orm'  # 指定表名

    # 定义字段，相当于 Java 里的 @Column
    id = Column(String(20), primary_key=True)
    name = Column(String(20))

engine = create_engine('sqlite:///test.db') # 连接同一个数据库文件
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

new_user = UserORM(id='3', name='Charlie')
session.add(new_user)
session.commit() # 提交事务

query_user = session.query(UserORM).filter(UserORM.id == '3').one()
print(f"ORM 查询结果: id={query_user.id}, name={query_user.name}")

session.close()
