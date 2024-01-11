#include <stdio.h>
#include <stdlib.h>


void print_array(int *a, int n)
{
	int i = 0;
	for (i = 0; i < n; i++)
	{
		printf("%d ", a[i]);
	}
	printf("\n");
}

void sort_array(int *a, int n)
{
	int i, j, temp;
	for (i = 0; i < n - 1; i++)
	{
		for (j = i + 1; j < n; j++)
		{
			if (a[i] > a[j])
			{
				temp = a[i];
				a[i] = a[j];
				a[j] = temp;
			}
		}
	}
}
int main(void)
{
	int a[] = { 10, 7, 1, 9, 4, 6, 7, 3, 2, 0 };
	int n;
	int i = 0;
	int j = 0;
	int temp = 0;

	n = sizeof(a) / sizeof(a[0]); //Ԫ�ظ���
	printf("n = %d\n", n);

	printf("����ǰ");
	print_array(a, n);

	//ѡ����������
	sort_array(a, n);

	printf("�����");
	print_array(a, n);

	printf("\n");
	system("pause");
	return 0;
}