

Version:1.6.0.13
    fix: 修复soap调用超时失效
    fix: 修复同一个request/task中调用其他多个task导致的任务丢失问题

Version:1.6.0.5
    fix: 修改redis返回值解析错误


Version:1.6.0.4
    add：增加flower监控
    add: 增加异步cache装饰器，注意如果被装饰的函数需要用的coroutine，需要最后使用coroutine装饰器


Version:1.6.0.3
    fix: 修复收到没有user-agent的请求
    add: 同步http请求增加post json功能
    add: 增加worker可配置并行大小


Version:1.6.0.2
    add: 增加异步redis的返回值解析


Version:1.6.0.1
    fix: 修复to_plain错误


Version:1.6.0.0
    fix: 更新支持最新tornado==5.x

Vsersion:1.5.0.21
    fix: urllib兼容性问题

Version:1.5.0.19
    fix: 修复异步执行celery任务时无法确定任务是否被执行的问题
    fix: 修复任务执行时设置tracking_started属性

Version:1.5.0.18
    fix: 异步redis增加断开重连机制

Version:1.5.0.15:
    update: 异步http请求改用requests库

Version 1.5.0.13:
    update: 设置默认异步http客户端为curl

Version 1.5.0.8:
    update: api接口增加status_code参数，允许更改返回错误码

Version 1.5.0.0:
    update: 增加对py3和win平台的适配

Version: 1.4.2.7
    add: 增加异步http request的重试机制

Version: 1.4.2.6
    fix: 回滚1.4.2.5的修改

Version: 1.4.2.5
    fix: subprocess不检检查exit code,部分shell（curl）不遵守非0即错的规范

Version: 1.4.2.4
    add: 增加task计划任务

Version: 1.4.1.20
    fix: component序列化问题

Version: 1.4.1.19
    fix: 同步连接池最大连接数及获取连接逻辑

Version: 1.4.1.18
    fix: mysql InterfaceError

Version 1.4.1.16
    add: 增加soap调用
    update: task client不需要task_class参数
    fix: 修复task自动集成CeleryTask类

Version 1.4.1.15
    fix: 修复非web组件调用thrift没有requestid错误
    update: service合并多个handler为一个,并自动集成ABLogic

Version: 1.4.1.14
    fix: 修复task 测试用例
    fix: 修复只有一个service时不fork进程，只有在多于一个service时才使用多进程
    fix: 修复调用service后，释放掉组件使用权
    update: 通过web层调用service，requestid透传
    fix: service层并发时，使用同一连接问题

Version: 1.4.1.13
    add: 调用task层时，调用方的requestid会成为本次任务的taskid， 任务的requesid也为透传id
    fix: celery错误日志打印
    fix: celery回调后的组件释放
    fix: 同步http_request增加超时和重试机制
    fix: 2.7版本下使用subprocess32替代subprocess


Version 1.4.1.12
    fix: 修复thrift同步异步客户端与server连接正常


Version 1.4.1.11:
    add: Api和Page异常时console日志打印
    fix: AsynThrift修复


Version 1.4.1.9:
    fix: Mysql同步查询无返回


Version 1.4.1.8:
    fix: Redis组件没有ping和reconnect


Version 1.4.1.7:
    fix: 修复redis组件


Version 1.4.1.6：
    add: 增加fastcelery脚本工具
    update: fastweb.app.loader.load_component参数更改
    fix: redis参数问题
    add: fast脚本工具

Version 1.4.1.3
    add: 增加fasthrift脚本，帮助快速生成thrift桩代码和fastweb的配置文件
    fix: 配置文件中name属性去掉，与section name歧义
    update: 移除yaml形式默认日志配置，修改为json形式
    fix: 日志系统每次开启都会生成info.log和error.log
    fix: service层rpc调用完成没有返回值，注意idl中要有返回值类型
    fix: 同步任务调用时，增加超时时间参数
    add: service层ABLogic可以调用组件，调用方式与web层相同
    add: 增加fasthrift工具
    add: 使用travis进行持续集成


Version 1.4.1.1
    fix: 修复同步调用系统命令函数，原采用subprocess调用系统命令，每次都需要创建子进程，面对大并发情况，性能较差
    update: fastweb.service.start_server -> start_service_server
    update: fastweb.service.MicroService -> Service
    fix: 修复task和service加载方式


Version 1.4.1:
    update: fastweb.loader.load_configuration 只用来加载非组件类的配置文件，这些配置是在业务中需要使用的
    update: fastweb.loader.load_component 用来加载制定配置文件中的组件，只会进行组件的加载，非组件的配置会被忽略掉，可以多次的加载不同的配置，以满足大量组件写在不同的配置文件中
            以上两条是为了配置文件的分离，使它们在物理上就是隔离的，防止混淆
    update: fastweb.web.start_server -> fastweb.web.start_web_server
    add: 增加依赖celery的任务系统，包括worker的运行和通过web层调用任务，具体参看fastweb.task和examples.task


Version 1.4.0:
    update: fastweb.loader.load_manager -> fastweb.loader.load_component
    fix: 修复mysql注入问题
    fix: 修复异步重试机制
    fix: 修复断开连接后的重新连接
    fix: 修复query后需要commit操作
    fix: 修复配置文件数字转换从float更改成int,解决数据库数字字符串问题
    fix: mysql防注入修复
    add: 增加handler级别线程池，处理阻塞操作
    fix: mysql.ping 使用reconnect参数，当连接没有断开时会报错(2003, "Can't connect to MySQL server on 'x.x.x.x' (fd x already registered)").
         该错误并非一个致命错误，只是一个警告





