# uc_quizzes

## xblock安装说明
安装命令
```
$sudo -u edxapp /edx/bin/pip.edxapp install <path_of_uc_quizzes>
```
 重启edxapp
 ```
 $sudo /edx/bin/supervisorctl -c /edx/etc/supervisord.conf restart edxapp:
 ```
 删除命令
 ```
 $sudo -u edxapp /edx/bin/pip.edxapp uninstall quizzes-xblock
 ```
## 后台添加说明
* [config.py](https://github.com/chtq/uc_quizzes/tree/master/quizzes/config.py)是配置文件，“github_username”是github的用户名，
   “github_repo”是github的题库仓库repo，我的仓库是[这里](https://github.com/chtq/exercise_web)
* 后台添加xblock，在url框中输入html网页的路径，后台会根据config.py中参数和url中的路径，拼接成一个完整的url，按照github提供的[api](https://developer.github.com/v3/)，从仓库中读取html网页内容（所有的网页都是在仓库的_book目录下，比如你在url编辑框中输入1126/1126.html，按照config.py的配置对应的完整路径就是https://github.com/chtq/exercise_web/blob/master/_book/1126/1126.html），最后进行处理生成前台要显示网页。

## 前台过程
* 学生在前台回答一道题目点击提交按钮后，前台会把结果提交到后台，后台根据[config.py]((https://github.com/chtq/uc_quizzes/tree/master/quizzes/config.py))中的git_host和teacher_id这两个参数指定的gitlab服务器地址，把学生答题的结果提交到gitlab上的仓库（仓库是teacher\answer，文件路径是学生email的hash值最后两位加学生用户名加题目的编号），学生每次提交的结果都会保存。

## 习题仓库
* 目前所有md文件习题的仓库在[这里](https://github.com/chyyuu/os_course_exercise_library)
* html文件仓库[这里](https://github.com/chtq/exercise_web/_book)

## 习题转换为html过程
 * 对md文件的处理使用了工具[gitbook](https://github.com/chtq/gitbook-1.5.0)和插件[gitbook-plugin-quizzes](https://github.com/chtq/gitbook-plugin-quizzes)。在需要处理md文件目录里面，需要有3个文件[book.json](https://github.com/chtq/exercise_web/blob/master/book.json)(这是gitbook进行处理过程的配置文件)，[README.md](https://github.com/chtq/exercise_web/blob/master/README.md)（页面介绍，生成index.html），[SUMMARY.md](https://github.com/chtq/exercise_web/blob/master/SUMMARY.md)（gitbook会按照这里面指定的文件处理）。gitbook处理完后，会把md文件生成的html放在_book目录下，你可以把_book目录下的html文件提交到github上的仓库中。
 * 我的gitbook使用的版本是1.5.0（现在已经更新到2.5多了，有很大的改动），nodejs版本是v0.10.33，机器是ubuntu32位系统。如果使用别的nodejs版本，可能会有问题（下载nodejs源码重新编译安装可能会解决问题，不要使用apt-get命令安装，但是目前nodejs的版本是4.1多，gitbook1.5.0基于新版的nodejs安装所需要的npm库会有错误）。如果用64位系统，需要执行`sudo npm install`命令重新下载gitbook所需要的依赖库.

## 自动处理auto.py原理
 * 从题库[仓库](https://github.com/chyyuu/os_course_exercise_library)中把原始md文件clone下来，对文件进行预处理成并调用gitbook把md处理为html网页，最后上传到html[仓库](https://github.com/chtq/exercise_web)。
 
 
