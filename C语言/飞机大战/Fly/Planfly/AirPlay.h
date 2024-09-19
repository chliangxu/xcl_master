#include<easyx.h>
//图形窗口的大小
#define BGWEIGHT 400 // 宽
#define BGHEIGHT 600 // 高

//void study_easyx();
/*
1.打开窗口，加载图片，链表结构的实现，变量的定义
2.生成我方飞机，我方飞机的移动
3.子弹的生成，发射，释放
*/

IMAGE img[4]; //图片数组
/* 现在位置的难点：
1.宏的定义以及作用
2.图片的相关操作
*/

// 初始化函数
void init() 
{
	//加载图片

}

//我们所有的功能，都从这个函数开始
void start()
{
	initgraph(BGWEIGHT, BGHEIGHT);

	while (1);

	closegraph();
}

void study_easyx()
{
	initgraph(800, 800);

	// 定义图片变量 int a;
	IMAGE img_mm;

	// 加载图片 scanf("%d, &a);
	loadimage(&img_mm, "asssets/2.jpg");
	//输出图片
	putimage(0, 0, &img_mm);

	getchar();

}
