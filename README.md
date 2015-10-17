# uc_quizzes

## 后台添加说明
* [config.py](https://github.com/chtq/uc_quizzes/tree/master/quizzes/config.py)是配置文件，“github_username”是github的用户名，
   “github_repo”是github的题库仓库repo
* 后台添加xblock，在url框中输入html网页的路径，后台会根据config.py中参数和url中的路径，拼接成一个完整的url，从github的仓库
  中读取html网页内容（所有的网页都是在仓库的_book目录下，比如你在url编辑框中输入1126/1126.html，路径就是仓库的_book/1126/1126.html    文件），最后进行处理生成前台要显示网页。
