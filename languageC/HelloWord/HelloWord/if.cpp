#include<stdio.h>

int ke()
{
	int x;
	char l;
	scanf("%d", &x);
	l = x >= 10 ? 'Y' : 'N'; // ��Ϊ Y����Ϊ N
	printf("%c", l);
	return 0;
}
/*
int main()
{
	int c, lo;
	
	scanf("%d", &c);
	if (c < 2)
	{
		printf("left \n");
	}
	else
	{
		if (2 <= c && c <= 10)
		{
			printf("In \n");
		}
		else
		{
			printf("Ringht \n");
		}
	}
	if (c < 60)
	{
		printf("������ \n");
	}
	else if ( c >= 60 && c < 70 )
	{
		printf("���� \n");
	}
	else if (c >= 70 && c < 80)
	{
		printf(" һ�� \n");
	}
	else if (c >= 80 && c < 90)
	{
		printf("���� \n");
	}
	else
	{
		printf("���� \n");
	}
	lo = ke();
	return 0;
}
*/