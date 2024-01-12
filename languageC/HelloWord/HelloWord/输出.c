#include <stdio.h>
//#define _CRT_SECURE_NO_WARNINGS

int main(void)
{
    //输入 scanf_s
    int a = 1;
    int b = 2;
    char buf[5];
    printf("输入前：%d, %d\n", a, b);
    //默认scanf_s中间是空格隔开，如果中间用英文的逗号隔开，那就必须用英文的逗号隔开
    scanf_s("%d%d", &a, &b);
    printf("输入后：%d, %d\n", a, b);
    system("pause");
    return 0;

}