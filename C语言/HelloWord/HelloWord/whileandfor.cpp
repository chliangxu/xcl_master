#include<stdio.h>


//for (��������ʼ���ó�ʼֵ��ѭ������������������)
//	{
//		ѭ����Ϊ
//   }
int Infor()
{
	int i, sum = 0;
	for (i = 1; i <= 100; i++)
	{
		sum = sum + i;
	}
	printf("%d %d \n", i, sum);
	return 0;
}


// do{
//	ѭ����Ϊ1
//  ѭ����Ϊ2
//  ...
// } while(ѭ������)���������У���
//{
//}
int Indowhile()
{
	int x;
	do
	{
		scanf("%d", &x);
	} while (x < 0);   // ���x��ֵС��0�����������ֵ���������ֵ����
	printf("%d \n", x);
	return 0;
}

// ѭ��Ƕ��
int MoreFor()
{
	for (char c = 'A'; c <= 'E'; c++)
	{
		for (int i = 0; i <= 9; i++)
		{
			printf("%c%d ", c, i);
		}
		printf("\n");
	}
	return 0;
}
/*
int main()
{	
	int get_infor, get_indowhile,get_morefor;
	int sum = 0, i = 1; //��ʼʱ��Ϊ���������ó�ʼֵ

	while (i <= 100) //��������һ������ֵ�Ƚ���Ϊѭ������
	{
		sum = sum + i;
		i++;        // ���¼�����
	}
	printf("%d, %d \n", sum, i);

	get_infor = Infor();
	get_indowhile = Indowhile();
	get_morefor = MoreFor();
	return 0;
}
*/