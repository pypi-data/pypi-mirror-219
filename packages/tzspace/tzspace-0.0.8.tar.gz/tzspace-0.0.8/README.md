# IOR SDK文档
## IOR简介

> IOR全称Internet of Rights,主要是解决如何在互联网上进行产权管理，资源分配，团队协作。<p>
> IOR出自于IEEE组织下的3816标准，是区块链之上的逻辑层，在现实场景中解决实际问题的整体方案。<p>
> IOR的项目地址:https://github.com/tzspace-ior/tzspacesdk<p>

## 下载安装

> IOR的SDK是Python实现的，并已经上传到pypi.org，可以通过命令行安装

    pip install tzspace -i https://pypi.org/simple

> tzspace是基于IOR标准的整体解决方案，其中iorsdk是tzspace的一部分

## 引用SDK
> 引用SDK的API

    from ior.iorsdk import IORSdk, IORConfig

> 引用SDK的工具

    from ior.util.web3_utils import keccak256

## 初始化SDK

    config = IORConfig()
    
    //POA环境使用
    config.set_is_poa(True)

    //设置打印
    config.set_is_print(True)

    config.set_provider('https://127.0.0.1:8545')

    ior = IORSdk(config)
    ior.init_service()


## 获取服务

    ior.tempctrl //默认服务

    ior.get('tempctrl') //查找服务

## 示例代码
### 证书Certificates

    from ior.iorsdk import IORSdk, IORConfig
    from ior.util.web3_utils import keccak256,to_text,to_address
    from ior.core.tz_contract_template_service import TZContractTemplateService

    #main test for example
    config = IORConfig()
    contract_addresses = {
        "RoleControl": "0x5FbDB2315678afecb367f032d93F642f64180aa3",
        "PermissionControl": "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512",
        "TZTemplateControl": "0x2279B7A0a67DB372996a5FaB50D91eAA73d2eBe6",
        "TZExchange": "0x59400c0ad731d23032B68E6B3f5ac0F8862eb83f"
    }
    default_contract_addresses = {        
        "STCCertificate": "0x9fE46736679d2D9a65F0992F2272dE9f3c7fa6e0",
        "DATACertificate": "0xCf7Ed3AccA5a467e9e704C703E8D87F634fB0Fc9",
        "CTCCertificate": "0xDc64a140Aa3E981100a9becA4E685f962f0cF6C9",
        "MDCCertificate": "0x5FC8d32690cc91D4c39d9d3abcBD16989F875707",
        "GNCCertificate": "0x0165878A594ca255338adfa4d48449f69242Eb8F",
        "INFT1Certificate": "0xa513E6E4b8f2a923D98304ec87F64353C4D5C853"
    }
    config.set_contract_addresses(contract_addresses)
    config.set_default_service_contract_addresses(default_contract_addresses)
    #config.set_is_poa(True)
    config.set_provider('http://127.0.0.1:8545/')
    config.set_is_print(True)
    ior = IORSdk(config)
    ior.init_service()

    cert = ior.get('stcc')

    pub = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    pk = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

    pub1,pk1 = ior.create_account()
    pub2,pk2 = ior.create_account()
    pub3,pk3 = ior.create_account()

    _,tokenId = cert.mint(pub,pub,pk)
    cert.set_authorize_approval(tokenId,pub1,True,pub,pk)
    h = cert.is_authorize_approved(tokenId,pub1)
    print(h)

    mp = cert.token_id_mapping_item(tokenId)
    print(mp)
    _,nId=cert.authorize(pub2,tokenId,pub1,pk1)
    mp = cert.token_id_mapping_item(tokenId)
    print(mp)

    cert.safeTransferFrom(pub2,pub3,nId,pub2,pk2)

### 角色权限RoleControl And PermissionControl

    from ior.iorsdk import IORSdk, IORConfig
    from ior.util.web3_utils import keccak256,to_text,to_address
    from ior.core.tz_contract_template_service import TZContractTemplateService

    #main test for example
    config = IORConfig()
    contract_addresses = {
        "RoleControl": "0x5FbDB2315678afecb367f032d93F642f64180aa3",
        "PermissionControl": "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512",
        "TZTemplateControl": "0x2279B7A0a67DB372996a5FaB50D91eAA73d2eBe6",
        "TZExchange": "0x59400c0ad731d23032B68E6B3f5ac0F8862eb83f"
    }
    config.set_contract_addresses(contract_addresses)
    #config.set_is_poa(True)
    config.set_provider('http://127.0.0.1:8545/')
    config.set_is_print(True)
    ior = IORSdk(config)
    ior.init_service()
    print(ior.role)

    pub = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    pk = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

    pub1,pk1 = ior.create_account()
    pub2,pk2 = ior.create_account()
    pub3,pk3 = ior.create_account()

    permission = "AddData"
    permissions = [permission]
    roleName = "Role1"
    adminRoleName = "AdminRole"
    permissionRoleName = "PermissionRole"
    rolectrl = ior.role
    pctrl = ior.permission
    permissionContractAddrs = [pctrl.address]

    #只需要添加一次
    #rolectrl.add_role(roleName,adminRoleName,permissionRoleName,permissions,permissionContractAddrs,pub,pk)

    rolectrl.grant_role(adminRoleName,pub1,pub,pk)
    rolectrl.grant_role(permissionRoleName,pub2,pub1,pk1)
    rolectrl.grant_role(roleName,pub3,pub1,pk1)

    permissionAdmin = "AdminRole"
    pctrl.grant_role(permissionAdmin,pub2,pub,pk)

    permissionAdmin2 = "AdminRole2"
    pctrl.grant_role(permissionAdmin2,pub2,pub,pk)

    addrs = [pctrl.address]
    rolectrl.add_permission(roleName,permissions,addrs,pub2,pk2)

    #read 0x01, write 0x02, read and write 0x03
    data = ["username","idcard"]
    operations = [0x02,0x03]
    defaultOperations = [0x01,0x02]
    parent = ["1.2.121.1.3.21.2","1.2.121.1.3.21.2"]
    dhash = data;

    pctrl.add_permission(permission,data,operations,defaultOperations,parent,dhash,pub2,pk2)

    data1 = "username"
    operation = 0x02
    h = rolectrl.check_permission(roleName,permission,data1,operation)
    print(h)

    data2 = "idcard"
    operation2 = 0x02
    h = rolectrl.check_permission(roleName,permission,data2,operation2)
    print(h)

    operation3 = 0x01
    h = rolectrl.check_permission(roleName,permission,data2,operation3)
    print(h)

    rolectrl.del_permission(roleName,[permission],pub2,pk2)

    operation4 = 0x01
    h = rolectrl.check_permission(roleName,permission,data1,operation4)
    print(h)

### 模板TempleteControl

    from ior.iorsdk import IORSdk, IORConfig
    from ior.util.web3_utils import keccak256,to_text,to_address
    from ior.core.tz_contract_template_service import TZContractTemplateService

    #main test for example
    config = IORConfig()
    contract_addresses = {
            "RoleControl": "0x5FbDB2315678afecb367f032d93F642f64180aa3",
            "PermissionControl": "0xe7f1725E7734CE288F8367e1Bb143E90bb3F0512",
            "TZTemplateControl": "0x2279B7A0a67DB372996a5FaB50D91eAA73d2eBe6",
            "TZExchange": "0x59400c0ad731d23032B68E6B3f5ac0F8862eb83f"
        }
    config.set_contract_addresses(contract_addresses)
    #config.set_is_poa(True)
    config.set_provider('http://127.0.0.1:8545/')
    config.set_is_print(True)
    ior = IORSdk(config)
    ior.init_service()
    print(ior.tempctrl)

    pub = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
    pk = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"

    ior.registerService('contract2',TZContractTemplateService(ior.w3, config
        , '0x8A791620dd6260079BF849Dc5567aDC3F2FdC318'))
    contract = ior.get('contract2')

    #初始化模板Id
    tmp_id = 1
    #只需要启动一次
    #ior.tempctrl.start(tmp_id, pub,pk)

    #注册的结果返回0，需要根据实际结果查看, pub和pk可以是任意用户, 根据模板设计
    _,ins_id = ior.tempctrl.request_template(tmp_id,'测试',2669296503, pub,pk)

    contract.init(ins_id, ['0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266']
        , '0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266'
        , ['0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266']
        , [10000]
        , pub, pk)

    contract.start(ins_id, pub, pk)
    contract.sign(ins_id, pub, pk)
    contract.end(ins_id, pub, pk)

    payees = contract.get_payees(ins_id)
        for payee in payees:
        addr = to_address(to_text(payee[12:]))
        ratio = contract.get_ratio(ins_id, addr)

## 服务列表
### 默认服务(构造函数初始化):
+ tempctrl
+ role
+ permission
+ exchange

### 预设置服务(init_service初始化):

|关键字|简称|含义|全称|
|:-|:-|:-|:-|
|stcc|STC|Storage|STCCertificate|
|datac|DTC|Data|DATACertificate|
|ctcc|CTC|Computing|CTCCertificate|
|mdcc|MDC|Model|MDCCertificate|
|gncc|GNC|Gene|GNCCertificate|
|inft1|INFT1|ImageNFT1|INFT1Certificate|
|contract1|CTRT|Contract1|TZContractTemplate|


### 用户注册服务
> 用户可以通过registerService接口注册需要的服务

    ior.registerService('myContract',TZContractTemplateService(self.w3, self._config
        , '0x88Ee1aa55C8eD81DB4366077D65a86Abb440FA54'))


### 目前支持的服务
+ [CertificateService](#CertificateService) 
+ [ExchangeService](#ExchangeService) 
+ [RoleControlService](#RoleControlService)
+ [PermissionControlService](#PermissionControlService)
+ [TZContractTemplateService](#TZContractTemplateService)
+ [TZTemplateControlService](#TZTemplateControlService)

### CertificateService
> 构造函数为:

    def __init__(self, w3, config, address)

> w3为web3的实例，可以从iorsdk对象获取<p>
> config为iorconfig<p>
> address为服务地址<p>

> 初始化示例:

    ior.registerService('mycert1',CertificateService(ior.w3, ior.config
        , '0x9B2c7f3222e483Ff5c563286fE7510497B836007'))

#### 服务API
##### approve
> 授权执行转移，事务接口

    def approve(self, to: str, token_id: int
        , public_key: str, private_key: str)

+ to: 授权的目标地址，地址一般为对方的公钥
+ token_id: 被授权的证书Id
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执

##### set approve for all
> 授权执行当前用户下的所有的证书转移，事务接口

    def set_approve_for_all(self, operator: str, approved: bool
        , public_key: str, private_key: str):

+ operator: 授权的目标地址，地址一般为对方的公钥
+ approved: 是否授权，True或者False
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执

##### mint
> 颁布一个证书，事务接口

    def mint(self, to: str
        , public_key: str, private_key: str)

+ to: 颁布证书的目标地址，地址一般为对方的公钥
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执
+ tokenId: 证书的Id

##### authorize
> 使用权授权，事务接口

    def authorize(self, to: str, original_token_id: int
        , public_key: str, private_key: str)

+ to: 颁布证书的目标地址，地址一般为对方的公钥
+ original_token_id: 目标证书Id
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执
+ tokenId: 证书的Id


##### set authorize approval
> 使用权授权人员设置，事务接口

    def set_authorize_approval(self, token_id: int, operator: str, approved: bool
        , public_key: str, private_key: str)

+ token_id: 目标证书Id
+ operator: 使用权授权审批人员的地址，地址一般为审批人员的公钥
+ approved: 是否审批通过, True/False
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执



##### create option
> 创建期权，事务接口

    def create_option(self, to: str, original_token_id: int, price: int, effect_date: int
        , public_key: str, private_key: str)

+ to: 使用权期权人员的地址，地址一般为被授权人员的公钥
+ original_token_id: 目标证书Id
+ price: 期权价格
+ effect_date: 期权到期时间
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执
+ tokenId: 证书的Id


##### token uri
> 查看证书URI，只读接口

    def token_uri(self, token_id: int)

+ token_id: 目标证书Id

> 返回
+ uri: 证书的URI




### ExchangeService
> 构造函数为:

    def __init__(self, w3, config)

> w3为web3的实例，可以从iorsdk对象获取<p>
> config为iorconfig<p>
> 使用的地址为iorconfig中 TZExchange 指定的地址<p>

> 初始化示例:

    ior.registerService('exchange',ExchangeService(ior.w3, ior.config))

#### 服务API
##### exchange

> 转让证书，事务接口

    def exchange(self, cert_address: str, token_id: int, from_address: str
        , to_address: str, price: int
        , public_key: str, private_key: str)

+ cert_address: 证书模板地址
+ token_id: 证书Id
+ from_address: 转让证书的用户地址
+ to_address: 转让证书的目标地址，地址一般为对方的公钥
+ price: 目标转让价格计数
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执


##### exchange with feed

> 附带前置条件的转让证书，事务接口

    def exchange_with_feed(self, cert_address: str, token_id: int, from_address: str
        , to_address: str, price: int, fee: int, feeds: list[str], percents: list[int]
        , public_key: str, private_key: str)

+ cert_address: 证书模板地址
+ token_id: 证书Id
+ from_address: 转让证书的用户地址
+ to_address: 转让证书的目标地址，地址一般为对方的公钥
+ price: 目标转让价格计数
+ fee: 前置转让费计数
+ feeds: 前置条件地址列表
+ percents: 前置转让费百分比列表，和feeds参数对应，即每个feeds中的地址能获取fee * percent的转让费(万分比,除以10000)
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执




### RoleControlService

> 构造函数为:

    def __init__(self, w3, config)

> w3为web3的实例，可以从iorsdk对象获取<p>
> config为iorconfig<p>
> 使用的地址为iorconfig中 RoleControl 指定的地址<p>

> 初始化示例:

    ior.registerService('role',RoleControlService(ior.w3, ior.config))

> 示例代码:

    from ior.util.web3_utils import keccak256

    ...


    pk,pub = ior.create_account()
    pk1,pub1 = ior.create_account()
    pk2,pub2 = ior.create_account()
    pk3,pub3 = ior.create_account()

	...

	permissionAddress = '0x9B2c7f3222e483Ff5c563286fE7510497B836007'
    addrs = [permissionAddress]
    permission = keccak256("AddData"))
	permissions = [permission]
	roleName = keccak256("Role1")
	adminRoleName = keccak256("AdminRole")
	permissionRoleName = keccak256("PermissionRole")

	permissionAdmin = keccak256("AdminRole")
	permissionAdmin2 = keccak256("AdminRole2")
	data = [keccak256("username"),keccak256("idcard")]
	
	# adminRoleName manage ${roleName} and its permision roles
	ior.role.addRole(roleName,adminRoleName,permissionRoleName,permissions,permissionAddress,pub,pk); 

	# pub1 can manage ${roleName} 
	ior.role.grantRole(adminRoleName,pub1,pub,pk)
	# pub2 can manage ${roleName} 
	ior.role.grantRole(permissionRoleName,pub2,pub,pk) #can add permission

	# pub1 grant ${roleName} 
	ior.role.grantRole(roleName,pub3,pub1,pk1)

	# pub2 can add permission because of it has been granted permissionRoleName
	ior.role.addPermission(roleName,permissions,addrs,pub2,pk2)

    operations = [0x01,0x03];
    defaultOperations = [0x01,0x01];
    parent = [keccak256("1.2.121.1.3.21.2"),keccak256("1.2.121.1.3.21.2")];
    hash = data;

	# pub2 has been granted permissionAdmin role 
    ior.permission.grantRole(permissionAdmin,pub2,pub,pk)
    ior.permission.grantRole(permissionAdmin2,pub2,pub,pk) #error
	ior.permission.addPermission(permission,data,operations,defaultOperations,parent,hash,pub2,pk2)

	
    operation = 0x03;

	dataU = keccak256("username")
    ior.role.checkPermission(roleName,permission,dataU,operation)

	dataI = keccak256("idcard")
    ior.role.checkPermission(roleName,permission,dataI,operation)

    ior.role.delPermission(roleName,[permission],pub2,pk2)
    ior.role.checkPermission(roleName,permission,dataU,operation)



#### 服务API
##### add role

> 添加角色，事务接口

    def add_role(self, role_name: str, admin_role: str, permission_role: str
        , permissions: list[str], permission_contract_addrs: list[str]
        , public_key: str, private_key: str)

+ role_name: 角色名称
+ admin_role: 角色管理员角色名称
+ permission_role: 权限管理员角色名称
+ permissions: 权限列表
+ permission_contract_addrs: 权限模板地址
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执


##### add permission

> 添加权限，事务接口

    def add_permission(self, role_name: str, permissions: list[str], permission_contract_addrs: list[str]
        , public_key: str, private_key: str)

+ role_name: 角色名称
+ permissions: 权限列表
+ permission_contract_addrs: 权限模板地址
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执


##### grant role

> 为用户授予角色，事务接口

    def grant_role(self, role_name: str, to: str
        , public_key: str, private_key: str)

+ role_name: 角色名称
+ to: 目标用户地址
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执


##### revoke role

> 为用户回收角色，事务接口

    def revoke_role(self, role_name: str, to: str
        , public_key: str, private_key: str)

+ role_name: 角色名称
+ to: 目标用户地址
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执


##### has role

> 为用户检查是否具备角色，只读接口

    def has_role(self, role_name: str, to: str):

+ role_name: 角色名称
+ to: 目标用户地址
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ res: 是否具备角色，True或者False

##### check permission

> 为指定数据检查权限，只读接口

    def check_permission(self, role_name: str, permission_name: str, data: str, operations: int)

+ permission_name:权限名称
+ permission_name:权限名称
+ data:数据关键字
+ operations: 数据操作标识列表，按位标识：0x1,0x2各是一种权限，0x3是这两种权限的组合，每个位含义由合约自行定义

> 返回
+ res: 是否具备权限，True或者False

### PermissionControlService

> 构造函数为:

    def __init__(self, w3, config)

> w3为web3的实例，可以从iorsdk对象获取<p>
> config为iorconfig<p>
> 使用的地址为iorconfig中 PermissionControl 指定的地址<p>
> 支持用户自定义权限控制模板，请使用registerService注册<p>

> 初始化示例:

    ior.registerService('permission',PermissionControlService(ior.w3, ior.config))

#### 服务API
##### add permission

> 为指定数据添加权限，事务接口

    def add_permission(self, permission_name: str, data: list[str], operations: list[int]
        , default_operations: list[int], parent: list[int], hash_values: list[str]
        , public_key: str, private_key: str)

+ permission_name:权限名称
+ data: 数据关键字列表
+ operations: 数据操作标识列表，按位标识：0x1,0x2各是一种权限，0x3是这两种权限的组合
+ default_operations: 默认数据操作标识列表，按位标识：0x1,0x2各是一种权限，0x3是这两种权限的组合
+ parent: 权限父节点数据哈希列表
+ hash_values: 权限哈希列表
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执

##### del permission

> 为指定数据删除权限，事务接口

    def del_permission(self, permission_name: str, data: list[str]
        , public_key: str, private_key: str)

+ permission_name: 权限名称
+ data: 数据关键字列表
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执


### TZTemplateControlService

> 构造函数为:

    def __init__(self, w3, config)

> w3为web3的实例，可以从iorsdk对象获取<p>
> config为iorconfig<p>
> 使用的地址为iorconfig中 TZTemplateControl 指定的地址<p>

> 目前支持的模板为：
* 合同模板 TZContractTemplate
* 工作流模板 TZWorkflowTemplate

> 初始化示例:

    ior.registerService('tempctrl',TZTemplateControlService(ior.w3, ior.config))

#### 服务API
##### register

> 注册模板，事务接口

    def register(self, template: str, category: int, name: str, ratio: int
        , public_key: str, private_key: str)

+ template: 模板地址
+ category: 模板分类
+ name: 模板名称
+ ratio: 分成比例，整数，万分比(除以10000)
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执
+ templateId: 模板Id


##### start

> 启动模板，事务接口

    def start(self, template_id: int
        , public_key: str, private_key: str)

+ template_id:模板Id
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执
+ state: 模板的状态


##### end
> 结束模板，事务接口

    def end(self, template_id: int
        , public_key: str, private_key: str)

+ template_id: 模板Id
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执
+ state: 模板的状态


##### request template

> 请求模板实例，事务接口

    def request_template(self, template_id: int, hash_value: str, end_time: int
        , public_key: str, private_key: str)

+ template_id: 模板Id
+ hash_value: 模板实例对应的数据哈希
+ end_time: 模板实例结束时间
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执
+ instanceId: 模板实例的Id



### TZContractTemplateService

> 构造函数为:

    def __init__(self, w3, config, address)

> w3为web3的实例，可以从iorsdk对象获取<p>
> config为iorconfig<p>
> address为模板地址<p>

> 初始化示例:

    self.registerService('contract1',TZContractTemplateService(self.w3, self.config
        , '0x59400c0ad731d23032B68E6B3f5ac0F8862eb83f'))


#### 服务API
##### init

> 合同模板实例初始化，事务接口

    def init(self, ins_id: int, signatories: list[str], payer: str
        , payees: list[str], share_ratios: list[int]
        , public_key: str, private_key: str)

+ ins_id: 模板实例Id
+ signatories:合同签约人地址列表
+ payer: 合同付款人地址
+ payees: 合同收款人地址列表
+ share_ratios: 合同分成比例列表，和payees一一对应, 万分比(除以10000)
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执
+ state: 合同实例的状态


##### start

> 合同模板实例启动，事务接口

    def start(self, ins_id: int
        , public_key: str, private_key: str)

+ ins_id: 模板实例Id
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执
+ state: 合同实例的状态


##### sign

> 合同模板实例，签约人签字，事务接口

    def sign(self, ins_id: int
        , public_key: str, private_key: str)

+ ins_id: 模板实例Id
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执
+ state: 合同实例的状态


##### end

> 合同模板实例完成合同，事务接口

    def end(self, ins_id: int
        , public_key: str, private_key: str)

+ ins_id: 模板实例Id
+ public_key: 执行的用户公钥
+ private_key: 执行的用户私钥

> 返回
+ receipt: 回执
+ state: 合同实例的状态



##### get payees

> 合同模板实例查看收款人地址列表，只读接口

    def get_payees(self, ins_id: int) -> list[str]:

+ ins_id: 模板实例Id

> 返回
+ res: 收款人地址列表



##### get ratio

> 合同模板实例查看指定收款人分成比例，只读接口

    def get_ratio(self, ins_id: int, payee: str) -> int

+ ins_id: 模板实例Id
+ payee: 收款人地址

> 返回
+ res: 分成比例, 万分比(除以10000)

