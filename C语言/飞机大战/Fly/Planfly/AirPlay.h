#include<easyx.h>
//ͼ�δ��ڵĴ�С
#define BGWEIGHT 400 // ��
#define BGHEIGHT 600 // ��

//void study_easyx();
/*
1.�򿪴��ڣ�����ͼƬ������ṹ��ʵ�֣������Ķ���
2.�����ҷ��ɻ����ҷ��ɻ����ƶ�
3.�ӵ������ɣ����䣬�ͷ�
*/

IMAGE img[4]; //ͼƬ����
/* ����λ�õ��ѵ㣺
1.��Ķ����Լ�����
2.ͼƬ����ز���
*/

// ��ʼ������
void init() 
{
	//����ͼƬ

}

//�������еĹ��ܣ��������������ʼ
void start()
{
	initgraph(BGWEIGHT, BGHEIGHT);

	while (1);

	closegraph();
}

void study_easyx()
{
	initgraph(800, 800);

	// ����ͼƬ���� int a;
	IMAGE img_mm;

	// ����ͼƬ scanf("%d, &a);
	loadimage(&img_mm, "asssets/2.jpg");
	//���ͼƬ
	putimage(0, 0, &img_mm);

	getchar();

}
