#include <stdio.h>
//#define _CRT_SECURE_NO_WARNINGS

int main(void)
{
    //���� scanf_s
    int a = 1;
    int b = 2;
    char buf[5];
    printf("����ǰ��%d, %d\n", a, b);
    //Ĭ��scanf_s�м��ǿո����������м���Ӣ�ĵĶ��Ÿ������Ǿͱ�����Ӣ�ĵĶ��Ÿ���
    scanf_s("%d%d", &a, &b);
    printf("�����%d, %d\n", a, b);
    system("pause");
    return 0;

}