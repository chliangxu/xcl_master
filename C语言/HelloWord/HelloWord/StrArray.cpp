#include<stdio.h>
#include<string.h>


int get_str() 
{
	/*
	C������scanf��int����������Ҫ���&�����ַ������е��ַ������벻�����&��ԭ����ʲô��
	���������str�����Ѿ�����õġ��ַ���������, ���ü�&, ��Ϊ��C�������������ʹ�����������ʼ��ַ
	��������int���飬&��Ѱַ���ţ������ĺ�����ӱ������ҵ�������ĵ�ַȻ�����ν��д洢
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