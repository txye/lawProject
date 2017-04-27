def match_pattern(inquiryStr, stateSlot):
    """
    获取用户话语中的关键信息，未完成
    目前支持：
        1）提取金额
        2）获取年龄
    例子：
        1）u"盗窃1000元钱也构成犯罪吗"
        2）u"我偷钱的时候是十七周岁，还不满十八周岁，是不是不算犯罪？"
    """
    #inquiryStr = u"我偷钱的时候是十七周岁，还不满十八周岁，是不是不算犯罪？"
    match = re.match(ur'.*[偷 盗窃](.*)元.*', inquiryStr)
    if match:
        amount = int(match.group(1))
        if(amount >= 1000 and amount < 30000):
            money = u"数额较大"
        elif amount >= 30000:
            money = u"数额巨大"
        elif(amount >= 500 and amount < 15000):
            money = u"数额较大标准的50%"
        else:
            money = u"数额不满足"
        stateSlot[u"对象"].add(money)

    match = re.match(ur'.*[满 是](.*?)周?岁.*', inquiryStr)
    if match:
        age = match.group(1)
        stateSlot[u"年龄"] = age

    match = re.match(ur'.*避.*险.*',inquiryStr)
    if match and (u"紧急" in inquiryStr or u"危急" in inquiryStr):
        stateSlot[u"特殊情况"].add("紧急避险")

    match = re.match(ur'.*被.*[胁迫 逼迫 威胁].*',inquiryStr)
    if match and (u"共同" in inquiryStr or u"协同" in inquiryStr):
        stateSlot[u"特殊情况"].add("共同犯罪被胁迫")

    match = re.match(ur'.*[提供 出售].*[凭证 整车合格证 号牌].*',inquiryStr)
    if match:
        stateSlot[u"行为"].add(u"提供或者出售机动车来历凭证、整车合格证、号牌以及有关机动车的其他证明和凭证")

    match = re.match(ur'.*犯罪.*偷开.*',inquiryStr)
    if match:
        stateSlot[u"行为"].add(u"作为犯罪工具偷开并遗弃")

    match = re.match(ur'.*[私自 未经允许 偷偷].*[开 拆].*[邮件 信件].*',inquiryStr)
    if match:
        stateSlot[u"行为"].add(u"私自开拆邮件并窃取")

    match = re.match(ur'.*[买卖 典当 拍卖 抵押].*[汽车 摩托 电动车 小车].*',inquiryStr)
    if match:
        stateSlot[u"行为"].add(u"买卖、介绍买卖、典当、拍卖、抵押机动车或者用其抵债")

    match = re.match(ur'.*[拆解 拼装 组装].*[汽车 摩托 电动车 小车].*',inquiryStr)
    if match:
        stateSlot[u"行为"].add(u"拆解、拼装或者组装机动车")

    match = re.match(ur'.*[修改 改变].*[汽车 摩托 电动车 小车].*[发动机号 识别代号].*',inquiryStr)
    if match:
        stateSlot[u"行为"].add(u"修改机动车发动机号、车辆识别代号")

    match = re.match(ur'.*[偷开].*油气.*阀门.*',inquiryStr)
    if match:
        stateSlot[u"行为"].add(u"偷开油气井、油气管道等油气设备阀门")

    match = re.match(ur'.*[窝藏 转移 收购 加工 代为销售].*[隐藏 掩饰 隐瞒].*',inquiryStr)
    if match:
        stateSlot[u"行为"].add(u"窝藏、转移、收购、加工、代为销售或者以其他方法掩饰、隐瞒")

    match = re.match(ur'.*非法.*[采种 采脂 挖笋 掘根 剥树皮].*',inquiryStr)
    if match:
        stateSlot[u"行为"].add(u"非法采种、采脂、挖笋、掘根、剥树皮")

    match = re.match(ur'.*[掩饰 隐藏 隐瞒].*[收益 利益 获得].*',inquiryStr)
    if match:
        stateSlot[u"行为"].add(u"掩饰、隐瞒犯罪所得及其产生的收益")
