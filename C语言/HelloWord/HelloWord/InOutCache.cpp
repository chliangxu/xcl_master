#include<stdio.h>
#include<Windows.h>
#include<conio.h>
//#include<unistd.h>


/*
int main() {
	for (int i = 0; i < 10; i++) {
		printf("hello world %d \n", i);
		Sleep(500);
	}
	char c1, c2, c3;
	c1 = getchar(); //输入字符
	putchar(c1); //输出字符
	getchar();
	/*
	为什么需要在写一个getchar?
	因为如果没有第二个getchar的话，程序在运行到第一个getchar时程序阻碍，会让你输入字符，然后回车，数据就会输入到缓存区，
	第一个getchar会在缓存区中把第一个字符拿到，然后putchar并打印第一个字符，程序继续运行，运行到c2那里的getchar，因为
	缓存区还有一个数据，不会阻塞程序，getchar会获取到 \n , 然后程序继续执行，putchar打印 \n 。但是这并不符合我们的预想，
	所以在上述地方在加上一个getchar,提前获取\n,从而达到目标。
	c2 = getchar(); 
	putchar(c2);

	c3 = getch(); // 输入函数，无需回车，没有缓存区，getchar立刻获取对应字符
	putchar(c3);
	
	return 0;
}*/