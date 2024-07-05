#include<stdio.h>
#include<string.h>


int get_str() 
{
	/*
	C语言中scanf在int类型数组中要添加&，而字符数组中的字符串输入不用添加&的原因是什么？
	输入参数（str）是已经定义好的“字符数组名”, 不用加&, 因为在C语言中数组名就代表该数组的起始地址
	而其他的int数组，&是寻址符号，在他的后面添加变量，找到变量后的地址然后依次进行存储
	*/
	char str[20];
	scanf("%s", str);

	for (int i = 0; i < strlen(str); i++) 
	{
		str[i] = str[i] - 32;
	}
	printf(str);
	return 0;
}
/*
int main()
{
	char str[20] = "HelloWorld";
	int len2;
	int get_strs;
	printf(str);
	printf("\n");
	printf("%s", str);
	len2 = strlen(str);
	printf("\n%d\n", len2);

	get_strs = get_str();



	return 0;
}
*/