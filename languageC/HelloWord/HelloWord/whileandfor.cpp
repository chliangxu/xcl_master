#include<stdio.h>


//for (计数器开始设置初始值；循环条件；计数器更新)
//	{
//		循环行为
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
//	循环行为1
//  循环行为2
//  ...
// } while(循环条件)；这里是有；的
//{
//}
int Indowhile()
{
	int x;
	do
	{
		scanf("%d", &x);
	} while (x < 0);   // 如果x的值小于0，则重新输出值，否则输出值出来
	printf("%d \n", x);
	return 0;
}

// 循环嵌套
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
	int sum = 0, i = 1; //开始时，为计数器设置初始值

	while (i <= 100) //计数器与一个有限值比较作为循环条件
	{
		sum = sum + i;
		i++;        // 更新计数器
	}
	printf("%d, %d \n", sum, i);

	get_infor = Infor();
	get_indowhile = Indowhile();
	get_morefor = MoreFor();
	return 0;
}
*/