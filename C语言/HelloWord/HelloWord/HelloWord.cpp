//C语言的函数是从上往下执行的，所以主函数main最好是在下面，在同一个文件里
//整数类型：%d
//浮点类型：%f
//字符类型：%c
//字符串类型：%s

#include<stdio.h> 
int add(int a, int b)
{
	return a + b;
}

//关键词
//1.char（字符型）表示一个很小的整数 --> 数值范围（-128 -- 127）           --> 0 到 2**8 -1
//2.short(短整形）表示一个不怎么大的整数 --> -2**15 -1 到 2**15 -1         --> 0 到 2**16 -1
//3.int(整形）一般的整数都可表示 --> -2**31 -1 到 2**31 -1                 --> 0 到 2**32 -1
//4.long(长整形）用于一个较大的整数--> -2**31 -1 到 2**31 -1               --> 0 到 2**32 -1
//5.long long（加长整形）一个非常大整数 --> -2**63-1 到 2**63 -1           --> 0 到 2**64 -1
//不想要最高位当作符号位用unsigned

//小数点后数字
//float:可以表示6位数字
//double:精度范围更长（6位以上）

//sizeof：测量实体占用字节的大小
//sizeof可以测试数据类型，变量，常量的大小
//二进制的位数是8位(因为计算机中的计数单位是二进制，所以一个字节即8个二进制，所以char的数值类型转换成10进制位是-2**n -1到 2**n -1，各关键词类型的范围如上所示
//同时最高位因为被当作符号位，所以n需要减去1，不想要最高位当作符号位用unsigned

int get_size()
{	
	// char(字符型的字节大小）
	printf("sizeof char=%d \n", sizeof(char)); // 字节大小为1

	// short(短整形的字节大小
	printf("sizeof shot=%d \n", sizeof(short)); // 字节大小为2

	// int （整形的字节大小）
	printf("sizeof int=%d \n", sizeof(int)); // 字节大小为4

	// long （长整型的字节大小）
	printf("sizeof long=%d \n", sizeof(long)); // 字节大小为4

	//long long（加长整形的字节大小）
	printf("sizeof longlong=%d \n", sizeof(long long)); // 字节大小为8

	printf("sizeof float=%d \n", sizeof(float)); // 字节大小为 4

	printf("sizeof double = %d \n ", sizeof(double)); // 字节大小为 8

	return 0;
}

//例题：定义一个字符变量letter,将其初始化为大写字母A,通过ASCII中的关系，将大写字母A,变成小写字母a,并将小写字母a打印出来
int ASCII_letter()
{
	int letter = 'A';
	letter = letter + 32;

	printf("letter=%c \n", letter);
	return 0;
}
//int表示函数的返回类型是整数类型（integer）
//main表示主函数
/*int main()
{	
	//函数中的变量必须先声明，在使用
	int result;
	int get_sizes;
	int letter;
	printf("Hello World \n");

	result = add(2, 3);
	printf("%d \n", result);

	get_sizes = get_size();
	printf("%d \n ", get_sizes);

	letter = ASCII_letter();
	//return：表示函数的返回值
	return 0;						
}
*/

//标识符必须进行声明和定义之后才能使用（add, a, b, result等都是标识符）
//标识符的命令规则：
//1.标识符可以用小写字母，大写字母，数字和下划线命名
//2.标识符的第一个字符必须是字母或下划线，不能是数字
//3.标识符是区分大小写的
