import time


def get_current_highest():
    """获取当前时间戳"""
    return int(time.time())


def sum_data(a, b):
    """计算函数"""
    return a + b


def set_token(token: str):
    """设置token，直接返回字典"""
    return {"Authorization": token}


def skip():
    return True


def skip_if(user_id):
    if user_id > 300:
        return True
    else:
        return False


def sql():
    return "select * from sp_goods;"
