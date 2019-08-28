# heqi_addons
Heqi's addons for GoodERP.

# 和汽产品模块
在Gooderp中增加和汽产品模块 hq_product

hq_product模块安装说明
=======================================

下拉Gooderp基础代码,在安装hq_product模块前

在应用中搜索安装“GOODERP 核心模块”(或core),“Gooderp SCM模块”

安装基础模块后搜索hq_product模块进行安装


hq_product模块设置说明
----------------------------------
安装hq_product模块后,需进行epc接口密钥设置、定时任务运行以、创建产品单位设置及权限设置
(优先进行epc接口密钥设置操作)

epc接口密钥设置:

    点击顶端模块栏“产品”,点击左侧菜单栏”主数据“下的”EPC参数设置“;
    
    在客户端ID及密钥处输入client_id,secret_key,点击左上方apply进行数密钥保存设置.
    
    若无相关密钥,请发送邮件到developers@heqiauto.com 获取授权账号
    
定时任务:

    点击顶端模块栏“设置”模块,于“分享挚爱”模版右下角点击“激活开发者模式”;
    
    再次点击模块栏”设置”选项,左端菜单栏中点击 技术➡️自动化➡️安排的动作
    
    打开定时任务模块,在模块中搜索“定时获取epc品牌及参数”定时任务
    
    点击定时任务,并进行初始化手动升级(仅需初始运行一次)
   
创建产品单位设置:
    
    若数据库表uom中存在单位“个”,可忽略此步;
    
    若不存在单位“个”:
   
      点击顶端模块栏“产品”,点击左侧菜单栏”主数据“下的”商品模块“;
      
      点击创建按钮,在计量单位的可选值下拉菜单中选择“创建并编辑...”
      
      在名称中输入“个”并保存设置,随后退出界面即可.
  
 导入产品权限设置:
 
    在设置➡️用户中进行所选用户权限设置,点击进入用户明细表
    
    点击所需设置的用户,在访问权的Gooderp中勾选“产品管理员”选项.

hq_product模块使用说明
----------------------------------

模块产品导入记录:
    进行产品导入历史记录

模块EPC产品查询导入:
    可进行EPC产品依照产品类型及品牌进行产品查询及导入功能


