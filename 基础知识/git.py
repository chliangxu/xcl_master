"""
git相关的代码及注意事项

a.git初始化项目。

    git init   --将当前目录初始化为项目根目录，会在该目录下生成一个 .git文件夹

    git init  项目名称   --在该目录下创建 ‘项目名称’ 文件夹，并将该文件夹初始化为项目根目录，并生成一个.git文件夹

b.git 版本合入

    git add .   --将所有工作区修改内容 提交到暂存区，（git status 查看文件状态， 文件由红变绿）

    git add 文件名   --将工作区指定文件 提交到暂存区，可多次提交，（git status 查看文件状态， 文件由红变绿）

    git reset  HEAD 文件名  --git add 的反操作，将文件从暂存区去掉

    git commit -m '提交信息'  --将暂存区信息提交到版本库

    git reset --soft  HEAD   --git commit 的反操作

    git reset --hard HEAD  --从版本库，回退代码到上次提交的代码库样子，注意会覆盖掉工作区修改内容

c.git分支切换

　　git branch 分支名   --创建分支

　　git checkout 分支名  --切换到某个具体的分支

d.git常用命令

　　git status  --查看当前文件状态

　　git log  --查看commit记录

    git rev-parse HEAD --查看本地的commit

　　git reflog  --查看所有变更记录

    git checkout --file // 撤销工作区的修改
    //查看Git配置信息
    git config -list
    //设置用户名和密码（一般只需要设置一次）
    git config --global user.name 'name'
    git config --global user.email 'email'


    //初始化
    git init
    //拉取远程master分支上内容
     git stash save '备注信息'

        //当前开发分支时，需要到另一个分支去更改一些东西，可以使用，然后直接切需要的分支就行，他会将第
       //  一个分支东西存在stash中，不删除，不提交

    git stash pop 弹出第一个 stash（该 stash 会从历史删除）

    git stash apply 可以达到 git stash pop 的效果，但是 stash 会在 list 中，不会删除

    git stash list 查看 stash 的列表

    git stash apply stash 名 切换到具体的 stash

    git fetch origin master
    //提交本地文件到暂存区
    git add .
    //查看暂存区状态
    git status
    //比较暂存区和工作区的差异
    git diff
    //将暂存区内容添加到本地仓库中
    git commit -m"注释"
    //提交合并请求
    git merge origin/master
    //推送到远程分支
    git push origin

    //查看本地分支
    git branch
    //查看所有远程分支
    git branch -r
    //查看所有分支
    git branch -a
    //创建本地分支
    git branch 分支名
    //建立本地分支和远程分支的映射关系
    git branch --set-upstream-to origin/分支名
    //撤销本地分支与远程分支的映射关系
    git branch --unset-upstream
    //查看本地分支和远程分支的映射关系
    git branch -vv
    //创建新分支并立即切换到该分支下
    git checkout -b 分支名
    //删除本地分支
    git branch -d 分支名
    //删除远程分支
    git push origin --delete 分支名
    //同步远程分支
    git fetch origin --prune
    //切换分支
    git checkout 分支名
    //拉取远程信息（同步远程分支）
    git pull
    //查看历史提交记录
    git log
    //查看指定文件的修改记录
    git blame 文件名
    //打标签
    git tag -a 标签名 -m"注释"
    //关联远程地址
    git remote add origin 远程地址
    //解除关联
    git remote rm origin
    //查看所有远程仓库
    git remote -v


e.常用命令

    // 文件相关的命令
    1.touch a //创建一个a文件

        1-1.mkdir test // 创建一个test的文件夹

    2.echo 1234 >> a //把1234这个内容放入a文件

    3.cat a //打开a文件，读取出a文件中的内容

    4.rm -rf 文件名 // 删除文件

    5.ls 文件夹名 // 查看对应文件夹中的内容

    6.ls -l // 拉出最近git提交记录以及对应修改的文件名

        6-1.ls -l -a // 拉出最近git提交记录以及对应修改的文件名,隐藏的文件也显示

    // cd快速切换路径
    1.cd - // 将工作路径切换到上一状态

    2.cd / // 进入根目录

    3.cd 文件名 // 进入某个目录

    4.

"""