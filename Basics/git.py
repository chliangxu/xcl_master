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
print("hello world")