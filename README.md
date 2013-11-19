# 1. 介绍

SwissCalc是码农专用的交互式计算器，为程序员们提供了很便利和很强大的功能。
SwissCalc支持整数、浮点数和字符串三种类型，支持复杂的表达式，支持变量，内置不少
强大的函数，支持用户自定义函数，可以很漂亮地显示二进制、八进制和十六进制。

SwissCalc最大的特点是方便。各种程序员们经常需要的工具在SwissCalc里输入，回车就
可以获得结果。加上Vim方便的编辑能力，能快速解决问题，成为您得力的助手。

==============================================================================
# 2. 安装

## 2.1 依赖

    * Vim 7.0+ 并支持Python插件
    * Python2.7

如果从源码安装Vim，需要加上参数--enable-pythoninterp。如果从发行版安装，请注意
是否支持Python插件。Mac OS X下使用MacVim会打开Python支持。Windows下从官网下安
装包也会打开Python支持。

想知道自己的Vim是否支持Python插件，有简单的方法验证。在普通模式下输入

    :py 0

如果没有报任何错误，说明您的Vim支持Python插件。

------------------------------------------------------------------------------
## 2.2 安装

### 2.2.1

如果直接安装，把所有文件解压或拷贝到Vim运行时加载的目录，比如~/.vim。请确保拷
贝完是这种结构的

    <您的运行时加载目录>/plugin/swisscalc.vim
    <您的运行时加载目录>/autoload/swisscalc.vim
    ...


### 2.2.2

如果使用vundle安装，请在vundle配置文件里加上

    Bundle 'lightxue/SwissCalc'

然后在普通模式下输入

    :BundleInstall lightxue/SwissCalc

------------------------------------------------------------------------------
## 2.3 脱离Vim运行

SwissCalc可以不依赖Vim使用，不过这样就失去了Vim的漂亮的高亮和强大的编辑功能，
也不能记录历史命令。打开方式如下

    cd autoload
    python swisscalc.py

==============================================================================
# 3. 使用方法

输入命令:ScalcSplit或其它打开命令(详见|swisscalc-commands|)打开SwissCalc。
SwissCalc设计成REPL模式，即输入(Read)、计算(Eval)、输出(Print)、继续(Loop)。
任何在提示符后面的指令会被解释计算，然后输出结果，再回到交互界面。

打开SwissCalc后，会进入插入模式，光标停在提示符后等待输入。举个例子：

    > 2+11
    13

'> '是提示符。在SwissCalc中，提示符很重要。在普通模式或插入模式，按了回车后，
当前行必须有提示符开头才会被解释计算。如果没有提示符开头，会被无视。如果您回车
后SwissCalc没有响应，有可能是提示符没有识别出来。这个机制能有效防止在输出结果
上误按回车。提示符是可配置的，详见(|swisscalc-prompt|)。

'2+11'是需要计算的表达式。SwissCalc支持多种数据类型、运算符和函数，这些后面
会介绍。

'13'是'2+11'计算出来的结果。

放些进一步的例子来吊吊胃口。

    > 2 ** (3!)
    64
    > x = sqrt(64) + (1 << 8)
    264.0
    > x + 10
    274.0
    > 0b111 + 0111 + 0x111 + 111
    464
    > setenv('bin')
    > setenv('hex')
    > _
    bin: 00000000 00000000 00000000 00000000 00000000 00000000 00000001 11010000
    dec: 464
    hex: 00 00 00 00 00 00 01 d0
    > md5('hello world')
    '5eb63bbbe01eeed093cb22bb8f5acdc3'


==============================================================================
# 4. REPL快捷键

SwissCalc的buffer内设置了一些快捷键，仅对SwissCalc的buffer有效。SwissCalc已经
尽可能少地影响Vim的正常功能。像搜索、复制、高亮等等都能正常使用。在SwissCalc里
的编辑操作应该跟其它文本一样。尤其是编辑之前计算过的的表达式再重新计算，在修正
错误和调整复杂表达式时很方便。这也是计算器配合上Vim强大的地方。不过注意输出结
果总是在buffer的最后面，这可能会让您感觉到困惑。如果觉得这给您带来困扰，可能使
用历史记录更方便。

    命令        模式            描述 ~

    <CR>        普通            计算当前行的表达式，并把结果输出到buffer最后
                                面。计算结果后面新开一行输出提示符并把光标停
                                在提示符后。

    <CR>        插入            跟普通模式下回车一样。不过最后光标停在提示符
                                后时还是插入模式。

    o           普通            跳到buffer末的提示符上。

    O           普通            同上

    <up>        插入            输出上一条执行的指令。历史输入指令记录大小是
                                有限制的，详见swisscalc-history-size

    <down>      插入            输出下一条执行的指令。与<up>操作相反。

==============================================================================
# 5. 数据类型

SwissCalc支持3种数据类型：整数、浮点数和字符串。

------------------------------------------------------------------------------
## 5.1 整数

SwissCalc的整数模拟计算机字长设置整数表示范围，详见*swisscalc-environment*里的
*word*和*signed*。整数可以用二进制、八进制、十进制和十六进制输入。比如：

    > 0b101
    5
    > 0B101
    5
    > 0101
    65
    > 0o101
    65
    > 0O101
    65
    > 101
    101
    > 0x101
    257
    > 0X101
    257

------------------------------------------------------------------------------
## 5.2 浮点数

SwissCalc的浮点数是用IEEE-754表示的，并不十分精确，不能做高精度运算。浮点数支
持小数表示和指数表示。比如：

    > 1.3
    1.3
    > 1.3e-1
    0.13

------------------------------------------------------------------------------
## 5.3 字符串

SwissCalc的字符串和整数、浮点数一样，可以存在变量里，可以当函数参数，可以当函
数返回值。字符串可以用单引号也可以用双引号包住。如果引号外面加r或R，里面的内容
不会转义。请看例子：

    > "I can sleep after using Light's SwissCalc\n"
    "I can sleep after using Light's SwissCalc\n"

    > 'I can sleep after using Light\'s SwissCalc\n'
    "I can sleep after using Light's SwissCalc\n"

    > r"I can sleep after using Light's SwissCalc\n"
    "I can sleep after using Light's SwissCalc\\n"

    > R"I can sleep after using Light's SwissCalc\n"
    "I can sleep after using Light's SwissCalc\\n"

------------------------------------------------------------------------------
## 5.4 转换

大部分情况下，不需要关心变量或参数是整数还是浮点数，SwissCalc会自动转换。 如果
需要这三种数据类型相互转换，请用*int*，*float*，*str*，详见*swisscalc-functions*。

==============================================================================
# 6. 运算符

SwissCalc支持程序员常用运算。下面会列出他们的优先级和结合性。先解释一下结合性
。结合性分为左和右两种。下看面例子：

    > 2 ** 2 ** 3
    64
    > (2 ** 2) ** 3
    64
    > 2 ** (2 ** 3)
    256

'\*\*'是左结合运算符。如果'\*\*'是右结合运算符，那个'2 \*\* 2 \*\* 3'的结果会是256。

下表是SwissCalc运算符列表，优先级从低到高。

    优先级      运算符      结合性       描述~
    0           =           right        赋值
    0           += -=       right        相加/相减并赋值
    0           *= /=       right        相乘/相除并赋值
    0           %= **=      right        相加/相减并赋值
    0           <<= >>=     right        左移/右移并赋值
    0           &= |= ^=    right        与/或/异或并赋值
    1           & | ^       left         与/或/异或
    2           << >>       left         左移/右移
    3           + =         left         相加/相减
    4           * / %       left         相乘/相除/取模
    5           !           right        阶乘，一元运算，如:5!
    6           **          left         乘方

运算符只支持整数和浮点数运算，不支持字符串。

==============================================================================
# 7. 变量

## 7.1 变量定义

在SwissCalc里，如果赋值操作的变量不存在，会自动创建。变量可以保存整数、浮点数
和字符串。变量可以用于运算符操作和当函数参数。例如：

    > x = 64
    64
    > 2 * x
    128
    > lg(x * 4)
    8.0

像'+='、'-='等这样运算并赋值的操作不能创建变量。如果这些操作符用于没有创建过的
变量，会引起语法错误。

------------------------------------------------------------------------------
## 7.2 变量作用域

SwissCalc只有一个全局的命名空间。也就是说，变量自创建起到SwissCalc的buffer关闭
都会存在。变量名和函数的命名空间不同，所以变量名可以跟函数名一样而不会引起冲
突。

------------------------------------------------------------------------------
## 7.3 内置变量

SwissCalc内置了一些实用的变量。

    变量名      描述~
    _           上一次运算结果
    e           自然常数
    pi          圆周率
    phi         黄金比例

==============================================================================
# 8. 函数

SwissCalc提供了许多内置函数，解决帮助您解决许多常见的问题。SwissCalc用很tricky
的方式支持自定义函数，满足您一些特殊的需求。如果您认为内置函数缺少常用功能，或
是您实现了对他人也有益的函数，请务必pull request或是发patch给我。

------------------------------------------------------------------------------
## 8.1 内置函数

内置函数实在太多，这里列出一些常用的函数，并介绍如何查找其它函数和函数用法。

    函数名        描述~
    help          参数是函数名的字符串，打印出函数的用法

    find_func     参数是正则表达式，打印SwissCalc可调用的函数里(内置和用户自定
                  义)匹配上的函数名。正则的语法与python的re模块一致。

    ff            同上

    funcs         无参数，打印SwissCalc所有可调用的函数(内置和用户自定义)

    vars          无参数，打印所有变量名和对应的值

    env           打印环境变量，详见swisscalc-environment

    setenv        设置环境变量，详见swisscalc-environment

    int           将参数转成整数返回。如果参数是浮点数，会截成整数。如果参数是
                  字符串，第2个参数可选。第2个参数可以指定进制。

    float         把整数或字符串转成浮点数返回

    str           把整数或浮点数转成字符串返回

    len           返回字符串长度

    printf        与C语言中printf用法类似

    print         与Python3中的print类似，打印多个参数

    hex           如果参数是整数，返回整数的十六进制字符串。如果参数是字符串，
                  打印字符串中每个字符串的十六进制数字

    md5           返回参数的md5

    sha1          返回参数的sha1

    b64enc     base64编码

    b64dec     base64解码

    htmlenc    html编码

    htmldec    html解码

    urlenc     url编码

    urldec     url解码

    ssize         把整数类型的字节大小转成人类易读的KiB、MiB等单位的字符串

    ssize         把1KB、4MiB等人类易读的字符串转成整数

    encode        字符编码转换

    uesc          unicode转义

    uunesc        unicdoe反转义

    now           当前时间戳

    strptime      时间戳转成字符串

    strftime      字符串转成时间戳

    regex         正则匹配

    sin/cos...    数学函数，Python的math模块中所有的数学函数SwissCalc都有

    ...           想了解更多请用funcs()

可能你觉得函数的用法介绍太简单了，没有关系，如果实际想用某个函数时用help()来查
看函数用法就行。想看完整函数列表，请用funcs()。如果函数名没有记清楚，请用ff()
来查找。

有一个小技巧，输入函数名时如果没有高亮，说明函数名打错了:)。

------------------------------------------------------------------------------
## 8.2 自定义函数

您可以通过自定义函数来补充内置函数的不足。如果你自定义的函数对他人也有益，请务
必pull request或发patch给我。

自定义函数写法很简单：在SwissCalc/autoload/custom.py里加上你需要的函数即可。这
个文件里所有的函数都会在SwissCalc启动时加载。

编写自定义函数请注意以下几点：

1. 自定义函数必须由Python编写。

2. 函数的参数和返回值必须是整数、浮点数、字符串三种类型之一。

3. 如果你的函数加了docstring，那么用help()可以看到你的函数的文档:)。

4. 你的函数从stdout输出的内容会输出到SwissCalc里。但是SwiissCalc读不到
   stdin和stderr的内容。

5. 如果自定义函数与内置函数的函数名相同，自定义函数会覆盖内置函数。

==============================================================================
# 9. 环境变量

SwissCalc会有一些环境变量配置自己的行为。这些环境变量和普通的变量存在不同的地
方，所以变量命名的时候请放心，不会覆盖环境变量。

    环境变量名   默认值    描述~
    bin          0         打印整数时是否打印它的二进制格式
    oct          0         打印整数时是否打印它的八进制格式
    dec          1         打印整数时是否打印它的十进制格式
    hex          0         打印整数时是否打印它的十六进制格式
    word         8         整数的字长
    signed       1         整数是否有符号

查看当前环境变量的值用env()。env()会把当前所有的环境变量名和值都打出来。设置环
境变量用函数setenv()。setenv()的第一个参数是变量名(字符串)，第二个参数可选，是
变量的值。如果第二个参数不填，那么环境变量的值反转，即原来是0的转成1，原来是非
0的转成0。

*word*和*signed*模拟了计算机的字长和是否有符号，它们决定了整数存储空间和存储范
围。也决定了*bin*和*hex*打印的字节数。

==============================================================================
# 10. 命令

SwissCalc只会打开一个buffer，但是允许有多个窗口。打开SwissCalc有以下几个命令：

*:Scalc*
    在当前窗口中打开SwissCalc

*:ScalcSplit*
    水平分割窗口并打开SwissCalc

*:ScalcVSplit*
    竖直分割窗口并打开SwissCalc

*:ScalcTab*
    新建标签页并打开SwissCalc

==============================================================================
# 11. 配置项

您可以在你的配置文件中修改SwissCalc的配置。这些配置项都有默认值，您什么都不配
置也可以正常使用SwissCalc。

## 11.1 Buffer标题

SwissCalc的buffer名字，这个名字不要和其它已经打开的buffer名字冲突。修改的这个
名字要特殊一些。

    let g:scalc_title = "__SwissCalc__"
    let g:scalc_max_history = 256

## 11.2 提示符

提示符，标识需要需要解释计算那一行。

    let g:scalc_prompt = "> "

## 11.3 历史记录数

记录历史表达式的最大数目。如果超出这个值，最旧的记录会被丢弃。用<up>和<down>可
以查看历史记录。

    let g:scalc_max_history = 256

==============================================================================
# 12. 更新日志

    版本      时间           描述~
    0.9.0     2013-11-18     Beta version.

==============================================================================
# 13. 关于

* 作者: Light Xue
* 邮箱: bkmgtp@gmail.com
* 项目主页: https://github.com/lightxue/SwissCalc

SwissCalc的目标是成为程序员的得力的助手。第一要点是便利，第二要点是强大。如果
SwissCalc切实地解决了您的问题，在学习工作中帮助了您，我会非常开心。

如果使用时发现有bug或是改进建议，请在项目主页的issue里留言。如果认为代码需要修
改，请给我pull request，或是发patch到我的邮箱。

从项目主页里可以得到最新版本的SwissCalc

在此对以下人士表示感谢

    名字                        描述~
    Guido van Rossum            如果不是Python，世界不会变得这么简单而美妙
    Bram Moolenaar              感谢你的Vim，让我这么多年来享受着编辑的乐趣
    David Beazley               你的PLY让我绕过了词法语法解析诸多黑暗的坑
    Greg Sexton                 没有你的VimCalc，就没有SwissCalc

==============================================================================
# 14. 许可证

SwissCalc使用GPLv3。 详见http://gplv3.fsf.org/



