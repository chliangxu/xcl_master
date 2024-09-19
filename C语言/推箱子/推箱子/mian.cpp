#include<stdio.h>
#include<easyx.h>
#include"ResList.h"

// 道具表示 
// 墙：0， 地板：1， 箱子目的地：2，小人：3，箱子：4， 箱子命中目标：5

// 值不会减少或增加，可以使用枚举，比如季节
enum MyEnum
{
	WALL,//墙
	FLOOL,//地板
	BOX_DES,//箱子的目的地
	MAN, //小人
	BOX,//箱子
	HIT,//箱子命中目标
	ALL, //上面所有个数的和 
};


int map[LINE][COLUMN] = {
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
	{ 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0 },
	{ 0, 1, 4, 1, 0, 2, 1, 0, 2, 1, 0, 0 },
	{ 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0 },
	{ 0, 1, 0, 2, 0, 1, 1, 4, 1, 1, 1, 0 },
	{ 0, 1, 1, 1, 0, 3, 1, 1, 1, 4, 1, 0 },
	{ 0, 1, 2, 1, 1, 4, 1, 1, 1, 1, 1, 0 },
	{ 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0 },
	{ 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 },
};

IMAGE images[ALL]; // 这个ALL是所有道具的总数

int main()
{
	IMAGE bg_img;
	//开始的地方
	initgraph(SCREENWEIGHT, SCREENHEIGHT);

	//设置背景
	loadimage(&bg_img, "推箱子游戏资源/blackground.bmp", 800, 800, true); // 这个地方写true是可以拉伸的，超出范围也行
	putimage(0, 0, &bg_img);

	// 道具表示 
	// 墙：0， 地板：1， 箱子目的地：2，小人：3，箱子：4， 箱子命中目标：5
	loadimage(&images[WALL], "推箱子游戏资源/wall_right.bmp", WALLWEIGHT, WALLHEIGHT, true);
	loadimage(&images[FLOOL], "推箱子游戏资源/floor.bmp", FLOORWEIGHT, FLOORHEIGHT, true);
	loadimage(&images[BOX_DES], "推箱子游戏资源/des.bmp", DESWEIGHT, DESHEIGHT, true);
	loadimage(&images[MAN], "推箱子游戏资源/man.bmp", MANWEIGHT, MANHEIGHT, true);
	loadimage(&images[BOX], "推箱子游戏资源/box.bmp", BOXWEIGHT, BOXHEIGHT, true);
	loadimage(&images[HIT], "推箱子游戏资源/box.bmp", BOXWEIGHT, BOXHEIGHT, true);

	for (int i = 0; i < LINE; i++)
	{
		for (int j = 0; j < COLUMN; j++)
		{
			putimage(SCREEN_X+j* BOXWEIGHT, SCREEN_Y+i* BOXHEIGHT,&images[map[i][j]]);
		}
	}

	system("pause");
	return 0;
}