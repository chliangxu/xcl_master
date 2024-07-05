#include<stdio.h>

int ke()
{
	int x;
	char l;
	scanf("%d", &x);
	l = x >= 10 ? 'Y' : 'N'; // 真为 Y，假为 N
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
		printf("不及格 \n");
	}
	else if ( c >= 60 && c < 70 )
	{
		printf("及格 \n");
	}
	else if (c >= 70 && c < 80)
	{
		printf(" 一般 \n");
	}
	else if (c >= 80 && c < 90)
	{
		printf("良好 \n");
	}
	else
	{
		printf("优秀 \n");
	}
	lo = ke();
	return 0;
}
*/