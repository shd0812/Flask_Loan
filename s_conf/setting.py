import os
BASE_PATH = os.path.dirname(   #找到utp的目录
    os.path.dirname(os.path.abspath(__file__))
)



Config_PATH = os.path.join(BASE_PATH,'s_conf','config.ini') #配置文件的路径
FANG_PATH=os.path.join(BASE_PATH,'s_conf','fang.yaml') #房缘贷的路径
QI_PATH=os.path.join(BASE_PATH,'s_conf','qi.yaml') #企缘贷的路径

