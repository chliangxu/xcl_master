#include<stdio.h>
#include<easyx.h>
int main()
{
	IMAGE bg_img;
	//��ʼ�ĵط�
	initgraph(800, 800);

	//���ñ���
	loadimage(&bg_img, "��������Ϸ��Դ/blackground.bmp", 800, 800, true); // ����ط�дtrue�ǿ�������ģ�������ΧҲ��
	putimage(0, 0, &bg_img);
	system("pause");
	return 0;
}