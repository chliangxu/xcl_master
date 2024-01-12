#include<stdio.h>
//多重选择语句

/*
int main()
{
	char letter;
	while (1)
	{
		scanf("%c", &letter);
		switch (letter)
		{
		case 'a':
			printf("alpha \n");
			break; //switch中的break是只对switch中的语句产生效果的，并不能对while产生影响，若放在case语句之外就可以
		case 'b':
			getchar(); //这个函数的作用是：清除未被吸收的输入
			continue; //因为contine是对switch不起作用的，所以这个是对while而言的
			printf("bravo \n");
			
		default:
			printf("i don't know\n\n");
		}
		break; // 这个是对while产生效果的
	}
	return 0;
}
*/
//break的作用:遇到break，跳出switch