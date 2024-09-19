#include<stdio.h>
#include<easyx.h>
#include"ResList.h"

// ���߱�ʾ 
// ǽ��0�� �ذ壺1�� ����Ŀ�ĵأ�2��С�ˣ�3�����ӣ�4�� ��������Ŀ�꣺5

// ֵ������ٻ����ӣ�����ʹ��ö�٣����缾��
enum MyEnum
{
	WALL,//ǽ
	FLOOL,//�ذ�
	BOX_DES,//���ӵ�Ŀ�ĵ�
	MAN, //С��
	BOX,//����
	HIT,//��������Ŀ��
	ALL, //�������и����ĺ� 
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

IMAGE images[ALL]; // ���ALL�����е��ߵ�����

int main()
{
	IMAGE bg_img;
	//��ʼ�ĵط�
	initgraph(SCREENWEIGHT, SCREENHEIGHT);

	//���ñ���
	loadimage(&bg_img, "��������Ϸ��Դ/blackground.bmp", 800, 800, true); // ����ط�дtrue�ǿ�������ģ�������ΧҲ��
	putimage(0, 0, &bg_img);

	// ���߱�ʾ 
	// ǽ��0�� �ذ壺1�� ����Ŀ�ĵأ�2��С�ˣ�3�����ӣ�4�� ��������Ŀ�꣺5
	loadimage(&images[WALL], "��������Ϸ��Դ/wall_right.bmp", WALLWEIGHT, WALLHEIGHT, true);
	loadimage(&images[FLOOL], "��������Ϸ��Դ/floor.bmp", FLOORWEIGHT, FLOORHEIGHT, true);
	loadimage(&images[BOX_DES], "��������Ϸ��Դ/des.bmp", DESWEIGHT, DESHEIGHT, true);
	loadimage(&images[MAN], "��������Ϸ��Դ/man.bmp", MANWEIGHT, MANHEIGHT, true);
	loadimage(&images[BOX], "��������Ϸ��Դ/box.bmp", BOXWEIGHT, BOXHEIGHT, true);
	loadimage(&images[HIT], "��������Ϸ��Դ/box.bmp", BOXWEIGHT, BOXHEIGHT, true);

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