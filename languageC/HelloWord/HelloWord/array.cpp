#include<stdio.h>
#include<memory.h>
/*
int main()
{
	int arr[10] = { 1, 2, 3, 4, 5, 6, 7, 8, 9, 0};
	//此时数组的长度10正好对应10个元素，若数组长度10大于括号对应的元素，则用0代替
	int arr2[10] = {}; //此时方括号里面的元素都是0
	int arr3[] = { 456, 485, 8484, 4848, 454 }; //若方括号里面没有数字，则系统自动填充，用于方括号中元素过多时

	//访问元素
	printf("%d\n", arr[0]); // 数值为1
	//修改元素
	arr[0] = 100;
	printf("%d\n", arr[0]); // 数值为100

	// 数组所占空间大小 = 单个元素所占空间大小 * 数组元素个数 int arr[10] 占用了40个字节

	//数组整理赋值（整体赋值需要用内存赋值memcpy）
	memcpy(arr2, arr, sizeof(arr2)); 
	// arr2 为目标数组， arr为原始数组，sizeof(arr1)为需要复制多少数据 目标数组和原始数组的大小不能小于sizeof(arr1)的数据
	for (int i = 0; i < 10; i++) {
		printf("%d ", arr2[i]);
	}
	return 0;
}
*/