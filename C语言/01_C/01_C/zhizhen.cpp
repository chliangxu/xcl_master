#include "Relist.h"

void zhizhen_01() {
	//1、指针的定义
	int a = 10; //定义整型变量a

	//指针定义语法： 数据类型 * 变量名 ;
	int* p;

	//指针变量赋值
	p = &a; //指针指向变量a的地址
	cout << &a << endl; //打印数据a的地址
	cout << p << endl;

	//2、指针的使用
	//通过*操作指针变量指向的内存
	cout << "*p = " << *p << endl;
}

void for_zhihzen() {
	int arr[5] = { 1, 2, 3, 4, 5 };
	int* p = arr;
	int i;
	printf("打印数组元素...\n");
	for (i = 0; i < 5; i++) {
		printf("sdsd %d \n", *(p + i));
	}
}
void zhizhen() {
		
	//zhizhen_01();
	//for_zhihzen();
	int arr[] = { 1,2,3,4,5,6,7,8,9,10 };

	int* p = arr;  //指向数组的指针

	cout << "第一个元素： " << arr[0] << endl;
	cout << "指针访问第一个元素： " << *p << endl;

	for (int i = 0; i < 10; i++)
	{
		printf("开始前f %d \n", *p);
		printf("开始前d %s \n", p);
		//利用指针遍历数组
		cout << *p << endl;
		cout << "指针访问的元素： " << *p << endl;
		p++;
		printf("开始后f %d \n", *p);
		printf("开始后d %s \n", p);
	}

	system("pause");

}