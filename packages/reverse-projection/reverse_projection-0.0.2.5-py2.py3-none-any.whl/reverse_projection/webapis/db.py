import sqlite3, time, json
from pathlib import Path
import pandas as pd
from flask import session, current_app
import joblib
from uuid import uuid4

# from .utils import get_feature_ind
from .data import round_data
from .utils import get_json, get_form
# from .algorithms import Decomposition

class DBMSG:

    def __init__(self, state=True, message="", return_values=None) -> None:
        self.state_ = state
        self.message_ = message
        self.return_values_ = return_values
    
    @property
    def state(self): return self.state_

    @property
    def message(self): return self.message_

    @property
    def return_values(self): return self.return_values_

    def __str__(self):
        return f'''
        state: {self.state}
        message: {self.message}
        return values: {self.return_values}
        '''

field_processor = {
    "ID": int,
    "NAME": json.loads,
    "CREATED_T": json.loads,
    "MODIFIED_T": json.loads,
    "CREATED_T_STAMP": json.loads,
    "MODIFIED_T_STAMP": json.loads,
    "DATASET": pd.read_json,
    "NUMBER_IND": json.loads,
    "TARGET_IND": json.loads,
    "FEATURE_IND": json.loads,
    "SHAPE": json.loads,
    "FEATURE_NAME": json.loads,
    "COLUMN": json.loads,
    "FEATURE_RANGE": json.loads,
    "USER_ID": int,

    "OMIT_IND": json.loads,
    "DECOMPOSER": json.loads,
    "SCALER": json.loads,
    "RECT_RANGE": json.loads,
    "AXIS": json.loads,
    "UID": json.loads,

    "OTHERS": json.loads,
}

class SQLiteDB:

    def __init__(self, url, user_id=None, init=False) -> None:
        self.path = Path(url)
        self.pkls = self.path.parent.joinpath("pkls")
        if not self.pkls.exists():
            self.pkls.mkdir()
        self.init = init
        self.user_id = user_id
    
    def init_db(self) -> None:
        con = sqlite3.connect(str(self.path))
        cur = con.cursor()
        # 创建一张新的用户表
        # LEVEL -1->root, 0->default, 1->normal
        exec_str = '''
            CREATE TABLE user
            (
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                USERNAME                        TEXT NOT NULL,
                PASSWD                          TEXT NOT NULL,
                LEVEL                       INTEGER DEFAULT 1
            )
        ;'''
        cur.execute(exec_str)
        # 创建一张新的数据集表
        # NAME 数据名
        # CREATED_T 创建时间
        # MODIFIED_T 修改时间
        # CREATED_T_STAMP 创建时间戳
        # MODIFIED_T_STAMP 修改时间戳
        # DATASET 数据(df->json)
        # NUMBER_IND 序号列index
        # TARGET_IND 目标列index
        # SHAPE (x, x)
        # FEATURE_NAMES 特征名
        # TITLES 全部变量名
        exec_str = '''
            CREATE TABLE dataset
            (
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                NAME                            TEXT NOT NULL,
                CREATED_T                       TEXT NOT NULL,
                MODIFIED_T                      TEXT NOT NULL,
                CREATED_T_STAMP                 TEXT NOT NULL,
                MODIFIED_T_STAMP                TEXT NOT NULL,
                DATASET                         TEXT NOT NULL,
                NUMBER_IND                      TEXT NOT NULL,
                TARGET_IND                      TEXT NOT NULL,
                FEATURE_IND                     TEXT NOT NULL,
                SHAPE                           TEXT NOT NULL,
                FEATURE_NAME                    TEXT NOT NULL,
                COLUMN                          TEXT NOT NULL,
                FEATURE_RANGE                   TEXT NOT NULL,
                USER_ID                      INTEGER NOT NULL,
                OTHERS                          TEXT NOT NULL
            )
        ;'''
        cur.execute(exec_str)
        exec_str = '''
            CREATE TABLE model
            (
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                NAME                            TEXT NOT NULL,
                CREATED_T                       TEXT NOT NULL,
                MODIFIED_T                      TEXT NOT NULL,
                CREATED_T_STAMP                 TEXT NOT NULL,
                MODIFIED_T_STAMP                TEXT NOT NULL,
                DATASET                         TEXT NOT NULL,
                NUMBER_IND                      TEXT NOT NULL,
                TARGET_IND                      TEXT NOT NULL,
                OMIT_IND                        TEXT NOT NULL,
                FEATURE_IND                     TEXT NOT NULL,
                FEATURE_NAME                    TEXT NOT NULL,
                COLUMN                          TEXT NOT NULL,
                DECOMPOSER                      TEXT NOT NULL,
                SCALER                          TEXT NOT NULL,
                RECT_RANGE                      TEXT NOT NULL,
                FEATURE_RANGE                   TEXT NOT NULL,
                AXIS                            TEXT NOT NULL,
                USER_ID                      INTEGER NOT NULL,
                UID                             TEXT NOT NULL,
                OTHERS                          TEXT NOT NULL
            )
        ;'''
        cur.execute(exec_str)
        con.commit()
        # 创建root用户和default用户
        cur.execute("INSERT INTO user (USERNAME, PASSWD, LEVEL) VALUES ('root', 'SHU66133513_LUKTIAN', -1);")
        cur.execute("INSERT INTO user (USERNAME, PASSWD, LEVEL) VALUES ('default', 'default', 0);")
        con.commit()
        con.close()
    
    def __enter__(self):
        if self.path.exists() and self.init:
            self.path.unlink()
        if not self.path.exists():
            self.init_db()
        self.con = sqlite3.connect(str(self.path))
        if self.user_id is None:
            try:
                self.user_id = session.get("user_id")
            except RuntimeError:
                self.user_id = None
            if not self.user_id:
                try:
                    self.user_id = get_json("userId")
                except:
                    self.user_id = get_form("userId")
            try:
                self.user_id = int(self.user_id)
            except:
                self.user_id = 0
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.con.close()
        self.user_id = ""

    
    def save_pkl(self, uid, model):
        joblib.dump(model, str(self.pkls.joinpath(uid)))
        return self

    def load_pkl(self, uid): 
        return joblib.load(str(self.pkls.joinpath(uid)))

    def delete_pkl(self, uid):
        if self.pkls.joinpath(uid).exists():
            self.pkls.joinpath(uid).unlink()

    
    # 注册用户
    def add_user(self, username: str, passwd: str) -> DBMSG:
        cur = self.con.cursor()
        exec_str = f'''
            SELECT USERNAME FROM user WHERE username=='{username}'
        ;'''
        cur.execute(exec_str)
        result = cur.fetchall()
        # 说明没有重名的
        if len(result) == 0:
            exec_str = f'''
                INSERT INTO user (USERNAME, PASSWD) 
                VALUES ('{username}', '{passwd}')
            ;'''
            cur.execute(exec_str)
            self.con.commit()
            return DBMSG(True, "注册成功")
        # 说明有重名的
        elif len(result) > 0:
            return DBMSG(False, "与已有用户名重复")
    
    # 检查用户登录
    def check_login(self, username: str, passwd: str) -> DBMSG:
        cur = self.con.cursor()
        exec_str = f'''
            SELECT ID, USERNAME, PASSWD
            FROM user
            WHERE USERNAME == '{username}'
        ;'''
        cur.execute(exec_str)
        result = cur.fetchall()
        # 输入的用户名不存在
        if len(result) == 0:
            return DBMSG(False, "输入的用户不存在")
        # 输入用户名存在，检查密码
        elif len(result) != 0:
            result = result[0] # 第一条记录, [id, username, passwd]
            # 密码不一致
            if passwd != result[2]:
                return DBMSG(False, "密码不正确")
            # 密码正确
            elif passwd == result[2]:
                return DBMSG(True, "登录成功", {"user_id": result[0], "username": result[1]})
    
    # 通过user_id获取用户
    def get_user_by_id(self, user_id) -> DBMSG:
        cur = self.con.cursor()
        exec_str = f'''
            SELECT USERNAME FROM user WHERE ID=='{user_id}'
        ;'''
        cur.execute(exec_str)
        result = cur.fetchall()[0][0]
        return DBMSG(True, "", {"user_name": result})
    
    # 添加数据集
    def add_dataset(
            self, 
            name: str,
            created_t: str,
            modified_t: str,
            created_t_stamp: str,
            modified_t_stamp: str,
            dataset: str,
            number_ind: str,
            target_ind: str,
            feature_ind: str,
            shape: str,
            column: str,
            feature_name: str, 
            feature_range: str,
            others: str,
            ) -> DBMSG:
        insert_dict = {
            "NAME": name, # TEXT
            "CREATED_T": created_t, # TEXT
            "MODIFIED_T": modified_t, # TEXT
            "CREATED_T_STAMP": created_t_stamp, # TEXT
            "MODIFIED_T_STAMP": modified_t_stamp, # TEXT
            "DATASET": dataset, # TEXT
            "NUMBER_IND": number_ind, # INTEGER
            "TARGET_IND": target_ind, # TEXT
            "FEATURE_IND": feature_ind, # TEXT
            "SHAPE": shape, # TEXT
            "FEATURE_NAME": feature_name, # TEXT
            "COLUMN": column, # TEXT
            "FEATURE_RANGE": feature_range, # TEXT
            "USER_ID": self.user_id, # INTEGER
            "OTHERS": others, # TEXT
        }
        insert_key_str = ", ".join([ key for key in insert_dict.keys() ])
        insert_value_str = ""
        for index, (insert_key, insert_value) in enumerate(insert_dict.items()):
            if insert_key in ["USER_ID"]:
                insert_value_str += str(insert_value)
            else:
                insert_value_str += f"'{str(insert_value)}'"
            if index < len(insert_dict)-1:
                insert_value_str += ", "
        cur = self.con.cursor()
        exec_str = f'''INSERT INTO dataset ({insert_key_str}) VALUES ({insert_value_str});'''
        cur.execute(exec_str)
        self.con.commit()
        return DBMSG(True, "数据添加成功")

    # 根据id获取dataset，将sql的信息转化为python中的格式
    def get_dataset_by_id(self, dataset_id: int, raw:bool=False, post:bool=False) -> DBMSG:
        cur = self.con.cursor()
        exec_str = (f'''
            SELECT 
            *
            FROM dataset
            WHERE ID=={dataset_id}
            AND USER_ID=={self.user_id}
        ;''')
        cur.execute(exec_str)
        result = cur.fetchall()
        if len(result) == 0:
            return DBMSG(False, "没有该数据集")
        else:
            fet_dataset = result[0]
            fields = [ i[0] for i in cur.description]
            fet_dataset = self.process_dataset(fet_dataset, fields, raw)
            if post:
                fet_dataset["dataset"] = round_data(fet_dataset["dataset"]).values.tolist()
            return DBMSG(True, "", fet_dataset)
    
    # 预处理单个dataset
    def process_dataset(self, fet_dataset: tuple, fields: iter, raw: bool=False) -> DBMSG:
        new_fet_dataset = {}
        for key, value in zip(fields, fet_dataset):
            if raw:
                new_fet_dataset.update({key: value})
            else:
                new_fet_dataset.update({key.lower(): field_processor[key](value)})
        return new_fet_dataset

    # 删除单个dataset
    def delete_dataset_by_id(self, dataset_id: int) -> DBMSG:
        cur = self.con.cursor()
        cur.execute(f'''
            DELETE FROM dataset WHERE dataset.id=={dataset_id} AND USER_ID=={self.user_id}
        ;''')
        self.con.commit()
        return DBMSG(True, "删除成功")
    
    # 更新单个dataset
    def update_dataset(self, dataset_id: int, dataset: pd.DataFrame) -> DBMSG:
        cur = self.con.cursor()
        dataset = dataset.to_json(orient='records', force_ascii=False)
        time_stamp = time.time()
        time_t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        time_stamp = json.dumps(time_stamp)
        time_t = json.dumps(time_t)
        exec_str = f'''
            UPDATE dataset SET
            DATASET='{dataset}',
            MODIFIED_T='{str(time_t)}',
            MODIFIED_T_STAMP='{str(time_stamp)}'
            WHERE ID=={dataset_id} AND USER_ID=={self.user_id}
        ;'''
        cur.execute(exec_str)
        self.con.commit()
        return DBMSG(True, "修改成功")
    
    # 获取数据集列表
    def get_dataset_list(self) -> DBMSG:
        cur = self.con.cursor()
        keys = ["ID", "NAME", "CREATED_T", "MODIFIED_T", "CREATED_T_STAMP", "MODIFIED_T_STAMP"]
        exec_str = f'''
            SELECT {", ".join(keys)}
            FROM dataset WHERE USER_ID=={self.user_id}
        ;'''
        cur.execute(exec_str)
        result = cur.fetchall()
        if len(result) == 0:
            # return_values = [{ i:"" for i in keys}]
            return_values = []
        else:
            return_values = []
            for index, key in enumerate(result):
                processed_dataset = self.process_dataset(key, keys)
                processed_dataset.update({"no": index+1})
                return_values.append(processed_dataset)
        return DBMSG(return_values=return_values)

    # 添加单个模型
    def add_model(
            self, 
            name: str, 
            created_t: str,
            modified_t: str,
            created_t_stamp: str,
            modified_t_stamp: str,
            dataset: str,
            number_ind: str,
            target_ind: str,
            omit_ind: str,
            feature_ind: str,
            feature_name: str,
            column: str, 
            feature_range: str,
            decomposer: str,
            scaler: str,
            rect_range: str,
            axis: str,
            uid: str,
            others: str,
            model,
        ) -> DBMSG:

        insert_dict = {
            "NAME": name, # TEXT
            "CREATED_T": created_t, # TEXT
            "MODIFIED_T": modified_t, # TEXT
            "CREATED_T_STAMP": created_t_stamp, # TEXT
            "MODIFIED_T_STAMP": modified_t_stamp, # TEXT
            "DATASET": dataset, # TEXT
            "NUMBER_IND": number_ind, # TEXT
            "TARGET_IND": target_ind, # TEXT
            "OMIT_IND": omit_ind, #TEXT
            "FEATURE_IND": feature_ind, # TEXT
            "FEATURE_NAME": feature_name, # TEXT
            "COLUMN": column, # TEXT
            "FEATURE_RANGE": feature_range, # TEXT
            "DECOMPOSER": decomposer, # TEXT
            "SCALER": scaler, # TEXT
            "RECT_RANGE": rect_range, # TEXT
            "AXIS": axis, # TEXT
            "USER_ID": self.user_id, # INTEGER
            "UID": uid, # TEXT
            "OTHERS": others,  # TEXT
        }
        insert_key_str = ", ".join([ key for key in insert_dict.keys() ])
        insert_value_str = ""
        for index, (insert_key, insert_value) in enumerate(insert_dict.items()):
            if insert_key in ["CREATED_T_STAMP", "MODIFIED_T_STAMP", "NUMBER_IND", "USER_ID"]:
                insert_value_str += str(insert_value)
            else:
                insert_value_str += f"'{str(insert_value)}'"
            if index < len(insert_dict)-1:
                insert_value_str += ", "
        
        cur = self.con.cursor()
        exec_str = f'''INSERT INTO model ({insert_key_str}) VALUES ({insert_value_str});'''
        cur.execute(exec_str)
        self.con.commit()
        self.save_pkl(json.loads(uid), model)
        return DBMSG(True, "模型添加成功")
    
    # 根据id获取模型
    def get_model_by_id(self, model_id: int, raw=False) -> DBMSG:
        cur = self.con.cursor()
        exec_str = (f'''
            SELECT 
            *
            FROM model
            WHERE ID=={model_id}
            AND USER_ID=={self.user_id}
        ;''')
        cur.execute(exec_str)
        result = cur.fetchall()
        if len(result) == 0:
            return DBMSG(False, "没有该模型")
        else:
            fet_model = result[0]
            fields = [ i[0] for i in cur.description]
            fet_model = self.process_model(fet_model, fields, raw)
            return DBMSG(True, "模型下载成功", fet_model)
    
    # 预处理单个模型，将sql的信息转化为python中的格式
    def process_model(self, fet_model: tuple, fields, raw: bool=False) -> dict:
        new_fet_model = dict()
        for key, value in zip(fields, fet_model):
            if raw:
                new_fet_model.update({key: value})
            else:
                new_fet_model.update({key.lower(): field_processor[key](value)})
        if "uid" in new_fet_model.keys() and not raw:
            new_fet_model["model"] = self.load_pkl(new_fet_model["uid"])
        if raw:
            new_fet_model.pop("USER_ID")
        return new_fet_model

    # 删除单个模型
    def delete_model_by_id(self, model_id: int) -> DBMSG:
        cur = self.con.cursor()
        cur.execute(f'''
            SELECT UID FROM model WHERE ID=={model_id} AND USER_ID=={self.user_id}
        ''')
        UID = cur.fetchall()[0][0]
        self.delete_pkl(json.loads(UID))
        cur.execute(f'''
            DELETE FROM model WHERE ID=={model_id} AND USER_ID=={self.user_id}
        ;''')
        self.con.commit()
        return DBMSG(True, "删除成功")
    
    # 获取模型列表
    def get_model_list(self) -> DBMSG:
        cur = self.con.cursor()
        keys = ["ID", "NAME", "CREATED_T", "MODIFIED_T", "CREATED_T_STAMP", "MODIFIED_T_STAMP"]
        exec_str = f'''
            SELECT {", ".join(keys)}
            FROM model WHERE USER_ID=={self.user_id}
        ;'''
        cur.execute(exec_str)
        result = cur.fetchall()
        if len(result) == 0:
            return_values = []
        else:
            return_values = []
            for index, key in enumerate(result):
                processed_model = self.process_model(key, keys)
                processed_model.update({"no": index+1})
                return_values.append(processed_model)
        return DBMSG(return_values=return_values)
    
    # 修改单个模型
    def update_model(
            self, 
            model_id: int,
            name: str, 
            created_t: str,
            modified_t: str,
            created_t_stamp: str,
            modified_t_stamp: str,
            dataset: str,
            number_ind: str,
            target_ind: str,
            omit_ind: str,
            feature_ind: str,
            feature_name: str,
            column: str, 
            feature_range: str,
            decomposer: str,
            scaler: str,
            rect_range: str,
            axis: str,
            uid: str,
            others: str,
            model,
        ) -> DBMSG:

        insert_dict = {
            "NAME": name, # TEXT
            "CREATED_T": created_t, # TEXT
            "MODIFIED_T": modified_t, # TEXT
            "CREATED_T_STAMP": created_t_stamp, # TEXT
            "MODIFIED_T_STAMP": modified_t_stamp, # TEXT
            "DATASET": dataset, # TEXT
            "NUMBER_IND": number_ind, # TEXT
            "TARGET_IND": target_ind, # TEXT
            "OMIT_IND": omit_ind, #TEXT
            "FEATURE_IND": feature_ind, # TEXT
            "FEATURE_NAME": feature_name, # TEXT
            "COLUMN": column, # TEXT
            "FEATURE_RANGE": feature_range, # TEXT
            "DECOMPOSER": decomposer, # TEXT
            "SCALER": scaler, # TEXT
            "RECT_RANGE": rect_range, # TEXT
            "AXIS": axis, # TEXT
            "USER_ID": self.user_id, # INTEGER
            "UID": uid, # TEXT
            "OTHERS": others,  # TEXT
        }
        # insert_key_str = ", ".join([ key for key in insert_dict.keys() ])
        # insert_value_str = ""
        # for index, (insert_key, insert_value) in enumerate(insert_dict.items()):
        #     if insert_key in ["CREATED_T_STAMP", "MODIFIED_T_STAMP", "NUMBER_IND", "USER_ID"]:
        #         insert_value_str += str(insert_value)
        #     else:
        #         insert_value_str += f"'{str(insert_value)}'"
        #     if index < len(insert_dict)-1:
        #         insert_value_str += ", "
        
        set_str = ""
        for index, (insert_key, insert_value) in enumerate(insert_dict.items()):
            if insert_key in ["CREATED_T_STAMP", "MODIFIED_T_STAMP", "NUMBER_IND", "USER_ID"]:
                set_str += f"{insert_key}=" + str(insert_value)
            else:
                set_str += f"{insert_key}=" + f"'{str(insert_value)}'"
            if index < len(insert_dict)-1:
                set_str += ", "

        cur = self.con.cursor()
        exec_str = f'''UPDATE model SET {set_str} WHERE ID=={model_id} AND USER_ID=={self.user_id};'''
        cur.execute(exec_str)
        self.con.commit()
        self.save_pkl(json.loads(uid), model)
        return DBMSG(True, "模型修改成功")


def get_sql_params_from_dataset(
    name: str,
    dataset: pd.DataFrame, 
    number_ind: int,
    target_ind: list,
    feature_ind: list
    ) -> dict:
    time_stamp = time.time()
    time_t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    feature_range = dataset.iloc[:, feature_ind].describe()\
        .loc[["min", "max"]].values.T.tolist()
    sql_p = dict()
    name = json.dumps(name)
    time_t = json.dumps(time_t)
    time_stamp = json.dumps(time_stamp)
    shape = json.dumps(dataset.shape)
    columns = json.dumps(dataset.columns.tolist())
    feature_name = json.dumps(dataset.columns[feature_ind].tolist())
    feature_range = json.dumps(feature_range)
    number_ind = json.dumps(number_ind)
    target_ind = json.dumps(target_ind)
    feature_ind = json.dumps(feature_ind)
    dataset = dataset.to_json(orient="records", force_ascii=False)
    others = json.dumps({})
    sql_p.update({
        "name": name,
        "created_t": time_t,
        "modified_t": time_t,
        "created_t_stamp": time_stamp,
        "modified_t_stamp": time_stamp,
        "dataset": dataset,
        "number_ind": number_ind,
        "target_ind": target_ind,
        "feature_ind": feature_ind,
        "shape": shape,
        "column": columns,
        "feature_name": feature_name,
        "feature_range": feature_range,
        "others": others,
    })
    return sql_p

def get_sql_params_from_model(model, modelName) -> dict:
    sql_model_p = dict()
    time_stamp = time.time()
    time_t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    time_stamp = json.dumps(time_stamp)
    time_t = json.dumps(time_t)
    name = json.dumps(modelName)
    dataset = model.dataset.to_json(orient="records", force_ascii=False)
    number_ind = json.dumps(model.number_ind)
    target_ind = json.dumps(model.target_ind)
    omit_ind = json.dumps(model.omit_ind)
    feature_ind = json.dumps(model.feature_ind)
    feature_name = json.dumps(model.feature_names.tolist())
    column = json.dumps(model.columns.tolist())
    feature_range = json.dumps(model.feature_range.tolist())
    decomposer = json.dumps(model.decomposer)
    scaler = json.dumps(model.scaler)
    rect_range = json.dumps(model.rect_range.tolist())
    axis = json.dumps(model.axis)
    uid = json.dumps(model.uid)
    others = json.dumps({})

    sql_model_p.update({
        "name": name,
        "created_t": time_t,
        "modified_t": time_t,
        "created_t_stamp": time_stamp,
        "modified_t_stamp": time_stamp,
        "dataset": dataset,
        "number_ind": number_ind,
        "target_ind": target_ind,
        "omit_ind": omit_ind,
        "feature_ind": feature_ind,
        "feature_name": feature_name,
        "column": column,
        "feature_range": feature_range,
        "decomposer": decomposer,
        "scaler": scaler,
        "rect_range": rect_range,
        "axis": axis,
        "uid": uid,
        "others": others,
    })

    sql_model_p.update({
        "model": model
    })
    return sql_model_p

if __name__ == '__main__':
    with SQLiteDB(Path(__file__).parent.joinpath("db"), True) as db:
        dbmsg = db.add_user("luktian", "ly931012")
        db.user_id = 1
        print(dbmsg)
        data = pd.DataFrame([[1,2,3], [3,4,5], [5,6,7]], columns=["A", "B", "C"])
        dbmsg = db.add_dataset("data", data, 0, [1], [2])
        print(dbmsg)
        # dbmsg = db.get_dataset_by_id(1)
        # dbmsg = db.delete_dataset_by_id(1)
        dbmsg = db.get_dataset_list()
        dbmsg = db.get_model_list()