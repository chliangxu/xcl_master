#include<stdio.h>
#include<easyx.h>
int main()
{
	IMAGE bg_img;
	//开始的地方
	initgraph(800, 800);

	//设置背景
	loadimage(&bg_img, "推箱子游戏资源/blackground.bmp", 800, 800, true); // 这个地方写true是可以拉伸的，超出范围也行
	putimage(0, 0, &bg_img);
	system("pause");
	return 0;
}