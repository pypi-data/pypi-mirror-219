# IOR SDK文档
## 初始化SDK

    config = IORConfig()
    config.set_is_poa(True)
    config.set_is_print(True)
    ior = IORSdk(config)
    ior.init_service()


## 获取服务

    ior.tempctrl //默认服务

    ior.get('tempctrl') //查找服务


### 默认的服务有(构造函数初始化):
+ tempctrl
+ permission
+ role
+ exchange

### 预设置的服务有(init_service初始化):
+ stcc
+ datac
+ ctcc
+ mdcc
+ gncc
+ inft1
+ contract1


### 用户注册服务
用户可以通过registerService接口注册需要的服务

    ior.registerService('myContract',TZContractTemplateService(self.w3, self._config, '0x88Ee1aa55C8eD81DB4366077D65a86Abb440FA54'))


### 支持的服务
+ [CertificateService](#CertificateService) 
+ [ExchangeService](#ExchangeService) 
+ [RoleControlService](#RoleControlService)
+ [PermissionControlService](#PermissionControlService)
+ [TZContractTemplateService](#TZContractTemplateService)
+ [TZTemplateControlService](#TZTemplateControlService)

### CertificateService
构造函数为:

    def __init__(self, w3, config, address)

w3为web3的实例，可以从iorsdk对象获取<p>
config为iorconfig<p>
address为服务地址<p>

初始化示例:

    ior.registerService('mycert1',CertificateService(ior.w3, ior.config, '0x9B2c7f3222e483Ff5c563286fE7510497B836007'))

####服务API
##### mint
颁布一个证书，事务接口

    def mint(self, to: str, public_key: str, private_key: str)

+ to: 颁布证书的目标地址，地址一般为对方的公钥
+ public_key: 发行证书的用户公钥
+ private_key: 发行证书的用户私钥

返回
+ blockHash: 区块的哈希地址
+ transactionHash: 事务的哈希地址
+ receipt: 回执，可以通过回执获取证书的Id

##### authorize
使用权授权，事务接口

    def authorize(self, to: str, original_token_id: int, public_key: str, private_key: str)

+ to: 颁布证书的目标地址，地址一般为对方的公钥
+ original_token_id: 目标证书Id
+ public_key: 发行证书的用户公钥
+ private_key: 发行证书的用户私钥

返回
+ blockHash: 区块的哈希地址
+ transactionHash: 事务的哈希地址
+ receipt: 回执，可以通过回执获取使用权证书的Id


##### set authorize approval
使用权授权人员设置，事务接口

    def set_authorize_approval(self, token_id, operator, approved, public_key, private_key)

+ token_id: 目标证书Id
+ operator: 使用权授权审批人员的地址，地址一般为审批人员的公钥
+ approved: 是否审批通过, True/False
+ public_key: 发行证书的用户公钥
+ private_key: 发行证书的用户私钥

返回
+ blockHash: 区块的哈希地址
+ transactionHash: 事务的哈希地址
+ receipt: 回执，可以通过回执获取使用权证书的Id



##### create option
创建期权，事务接口

    def create_option(self, to, original_token_id, price, effect_date, public_key, private_key)

+ to: 使用权期权人员的地址，地址一般为被授权人员的公钥
+ original_token_id: 目标证书Id
+ price: 期权价格
+ effect_date: 期权到期时间
+ public_key: 授权证书的用户公钥
+ private_key: 授权证书的用户私钥

返回
+ blockHash: 区块的哈希地址
+ transactionHash: 事务的哈希地址
+ receipt: 回执，可以通过回执获取使用权证书的Id


##### token uri
查看证书URI，只读接口

    def token_uri(self, token_id)

+ token_id: 目标证书Id

返回
+ uri: 证书的URI




### ExchangeService
构造函数为:

    def __init__(self, w3, config)

w3为web3的实例，可以从iorsdk对象获取<p>
config为iorconfig<p>
使用的地址为iorconfig中 TZExchange 指定的地址

初始化示例:

    ior.registerService('exchange',ExchangeService(ior.w3, ior.config))

####服务API
##### exchange
转让证书，事务接口

    def exchange(self, cert_address: str, token_id: int, from_address: str, to_address: str, price: int, public_key: str,
                 private_key: str)

+ cert_address: 证书模板地址
+ token_id: 证书Id
+ from_address: 转让证书的用户地址
+ to_address: 转让证书的目标地址，地址一般为对方的公钥
+ price: 目标转让价格计数
+ public_key: 发行证书的用户公钥
+ private_key: 发行证书的用户私钥

返回
+ receipt: 回执，可以通过回执获取证书的Id


##### exchange with feed
附带前置条件的转让证书，事务接口

    def exchange_with_feed(self, cert_address: str, token_id: int, from_address: str, to_address: str, price: int,
                           fee: int, feeds: list[str], percents: list[int], public_key: str, private_key: str)

+ cert_address: 证书模板地址
+ token_id: 证书Id
+ from_address: 转让证书的用户地址
+ to_address: 转让证书的目标地址，地址一般为对方的公钥
+ price: 目标转让价格计数
+ fee: 前置转让费计数
+ feeds: 前置条件地址列表
+ percents: 前置转让费百分比列表，和feeds参数对应，即每个feeds中的地址能获取fee * percent的转让费
+ public_key: 发行证书的用户公钥
+ private_key: 发行证书的用户私钥

返回
+ receipt: 回执，可以通过回执获取证书的Id




### RoleControlService
构造函数为:

    def __init__(self, w3, config)

w3为web3的实例，可以从iorsdk对象获取<p>
config为iorconfig<p>
使用的地址为iorconfig中 RoleControl 指定的地址

初始化示例:

    ior.registerService('role',RoleControlService(ior.w3, ior.config))

####服务API
##### add role
添加角色，事务接口

    def add_role(self, role_name: str, admin_role: str, permission_role: str, permissions: list[str],
                 permission_contract_addrs: list[str], public_key: str, private_key: str)

+ role_name: 角色名称
+ admin_role: 角色管理员角色名称
+ permission_role: 权限管理员角色名称
+ permissions: 权限列表
+ permission_contract_addrs: 权限模板地址
+ public_key: 添加角色的用户公钥
+ private_key: 添加角色的用户私钥

返回
+ receipt: 回执


##### add permission
添加权限，事务接口

    def add_permission(self, role_name, permissions, permission_contract_addrs, public_key, private_key)

+ role_name: 角色名称
+ permissions: 权限列表
+ permission_contract_addrs: 权限模板地址
+ public_key: 添加角色的用户公钥
+ private_key: 添加角色的用户私钥

返回
+ receipt: 回执


##### grant role
为用户授予角色，事务接口

    def grant_role(self, role_name: str, to: str, public_key: str, private_key: str)

+ role_name: 角色名称
+ to: 目标用户地址
+ public_key: 添加角色的用户公钥
+ private_key: 添加角色的用户私钥

返回
+ receipt: 回执


##### revoke role
为用户回收角色，事务接口

    def revoke_role(self, role_name: str, to: str, public_key: str, private_key: str)

+ role_name: 角色名称
+ to: 目标用户地址
+ public_key: 添加角色的用户公钥
+ private_key: 添加角色的用户私钥

返回
+ receipt: 回执


##### has role
为用户检查是否具备角色，只读接口

    def has_role(self, role_name: str, to: str):

+ role_name: 角色名称
+ to: 目标用户地址
+ public_key: 添加角色的用户公钥
+ private_key: 添加角色的用户私钥

返回
+ res: True or False



### PermissionControlService
构造函数为:

    def __init__(self, w3, config)

w3为web3的实例，可以从iorsdk对象获取<p>
config为iorconfig<p>
使用的地址为iorconfig中 PermissionControl 指定的地址
支持用户自定义权限控制模板，请使用registerService注册

初始化示例:

    ior.registerService('permission',PermissionControlService(ior.w3, ior.config))

####服务API
##### add permission
为指定数据添加权限，事务接口

    def add_permission(self, permission_name: str, data: list[str], operations: list[int],
                       default_operations: list[int], parent: list[int], hash_values: list[str], public_key: str,
                       private_key: str)

+ permission_name:权限名称
+ data: 数据关键字列表
+ operations: 数据操作标识列表，按位标识：0x1,0x2各是一种权限，0x3是这两种权限的组合
+ default_operations: 数据操作标识列表，按位标识：0x1,0x2各是一种权限，0x3是这两种权限的组合
+ parent: 权限父节点数据哈希列表
+ hash_values: 权限哈希列表
+ public_key: 发行证书的用户公钥
+ private_key: 发行证书的用户私钥

返回
+ receipt: 回执

##### del permission
为指定数据删除权限，事务接口

    def del_permission(self, permission_name: str, data: list[str], public_key: str, private_key: str)

+ permission_name: 权限名称
+ data: 数据关键字列表
+ public_key: 发行证书的用户公钥
+ private_key: 发行证书的用户私钥

返回
+ receipt: 回执

##### check permission
为指定数据检查权限，只读接口

    def check_permission(self, permission_name: str, data: str, operations: int)

+ permission_name:权限名称
+ data:数据关键字
+ operations: 数据操作标识列表，按位标识：0x1,0x2各是一种权限，0x3是这两种权限的组合

返回
+ res: True or False

### TZTemplateControlService
构造函数为:

    def __init__(self, w3, config)

w3为web3的实例，可以从iorsdk对象获取<p>
config为iorconfig<p>
使用的地址为iorconfig中 TZTemplateControl 指定的地址

目前支持的模板为：
* 合同模板 TZContractTemplate
* 工作流模板 TZWorkflowTemplate

初始化示例:

    ior.registerService('tempctrl',TZTemplateControlService(ior.w3, ior.config))

####服务API
##### register
注册模板，事务接口

    def register(self, template: str, category: int, name: str, ratio: int, public_key: str, private_key: str)

+ template: 模板地址
+ category: 模板分类
+ name: 模板名称
+ ratio: 分成比例，整数，会除以1000后计算
+ public_key: 发行证书的用户公钥
+ private_key: 发行证书的用户私钥

返回
+ receipt: 回执，可以通过回执获取模板的Id


##### start
启动模板，事务接口

    def start(self, template_id: int, public_key: str, private_key: str)

+ template_id:模板Id
+ public_key: 发行证书的用户公钥
+ private_key: 发行证书的用户私钥

返回
+ receipt: 回执，可以通过回执获取模板的状态


##### end
结束模板，事务接口

    def end(self, template_id: int, public_key: str, private_key: str)

+ template_id: 模板Id
+ public_key: 发行证书的用户公钥
+ private_key: 发行证书的用户私钥

返回
+ receipt: 回执，可以通过回执获取模板的状态


##### request template
请求模板实例，事务接口

    def request_template(self, template_id: int, hash_value: str, end_time: int, public_key: str,
                         private_key: str)

+ template_id: 模板Id
+ hash_value: 模板实例对应的数据哈希
+ end_time: 模板实例结束时间
+ public_key: 发行证书的用户公钥
+ private_key: 发行证书的用户私钥

返回
+ receipt: 回执，可以通过回执获取模板实例的Id



### TZContractTemplateService
构造函数为:

    def __init__(self, w3, config, address)

w3为web3的实例，可以从iorsdk对象获取<p>
config为iorconfig<p>
address为模板地址

初始化示例:

    self.registerService('contract1',TZContractTemplateService(self.w3, self.config, '0x59400c0ad731d23032B68E6B3f5ac0F8862eb83f'))


####服务API
##### init
合同模板实例初始化，事务接口

    def init(self, ins_id: int, signatories: list[str], payer: str, payees: list[str],
             share_ratios: list[int], public_key: str, private_key: str)

+ ins_id: 模板实例Id
+ signatories:合同签约人地址列表
+ payer: 合同付款人地址
+ payees: 合同收款人地址列表
+ share_ratios: 合同分成比例列表，和payees一一对应
+ public_key: 发行合同的用户公钥
+ private_key: 发行合同的用户私钥

返回
+ receipt: 回执，可以通过回执获取合同的状态


##### start
合同模板实例启动，事务接口

    def start(self, ins_id: int, public_key: str, private_key: str)

+ ins_id: 模板实例Id
+ public_key: 发行合同的用户公钥
+ private_key: 发行合同的用户私钥

返回
+ receipt: 回执，可以通过回执获取合同的状态


##### sign
合同模板实例，签约人签字，事务接口

    def sign(self, ins_id: int, public_key: str, private_key: str)

+ ins_id: 模板实例Id
+ public_key: 发行合同的用户公钥
+ private_key: 发行合同的用户私钥

返回
+ receipt: 回执，可以通过回执获取合同的状态


##### end
合同模板实例完成合同，事务接口

    def end(self, ins_id: int, public_key: str, private_key: str)

+ ins_id: 模板实例Id
+ public_key: 发行合同的用户公钥
+ private_key: 发行合同的用户私钥

返回
+ receipt: 回执，可以通过回执获取合同的状态



##### get payees
合同模板实例查看收款人地址列表，只读接口

    def get_payees(self, ins_id: int) -> list[str]:

+ ins_id: 模板实例Id

返回
+ res: 收款人地址列表



##### get ratio
合同模板实例查看指定收款人分成比例，只读接口

    def get_ratio(self, ins_id: int, payee: str)

+ ins_id: 模板实例Id
+ payee: 收款人地址

返回
+ res: 分成比例

