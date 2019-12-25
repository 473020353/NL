class RestUrlConfig:
    # 彩信推送
    url_code_verify = "http://rest.guyuaninfo.com:7000/push/api/sms/code-verify"
    url_code_get = "http://rest.guyuaninfo.com:7000/push/api/sms/code"
    # 获取AL层rest地址
    url_get_alrest = "http://rest.guyuaninfo.com:5000/pl/api/project/getalresturl"
    # 呼和浩特厕所地址
    ws_url = "wss://screen.guyuaninfo.com:3333/ws?room="
    # PLNFC巡检
    nfc_url_pre = "http://rest.guyuaninfo.com:6000/pl/nfc/controller"
    # 项目ID
    projectid = '10710051397058'
    # PL VT VA 绑定
    url_bind = 'http://rest.guyuaninfo.com:5000/pl/api/pl/vavt/add'
    # PL VT VA 解绑
    url_unbind = 'http://rest.guyuaninfo.com:5000/pl/api/pl/vavt/delete'
    # PL 数据大小端转换
    short_address = 'http://rest.guyuaninfo.com:5000/pl/api/pl/toolbox'
    # PL 微信推送
    push_wx_url = "http://rest.guyuaninfo.com:6000/wx/pushmsg"
    # mp3路径
    mp3_url = "http://127.0.0.1:8000/al/api/tts"
    # mp3静态存放路径
    mp3_path = "/var/www/html/zzal/api/web/library/"
    mp3_replace_flag = "/var/www/html/zzal"
    # 大屏推送
    screen_ws_rest_url = "https://screen.guyuaninfo.com:8080/screen/push-msg"