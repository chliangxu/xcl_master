//C���Եĺ����Ǵ�������ִ�еģ�����������main����������棬��ͬһ���ļ���
//�������ͣ�%d
//�������ͣ�%f
//�ַ����ͣ�%c
//�ַ������ͣ�%s

#include<stdio.h> 
int add(int a, int b)
{
	return a + b;
}

//�ؼ���
//1.char���ַ��ͣ���ʾһ����С������ --> ��ֵ��Χ��-128 -- 127��           --> 0 �� 2**8 -1
//2.short(�����Σ���ʾһ������ô������� --> -2**15 -1 �� 2**15 -1         --> 0 �� 2**16 -1
//3.int(���Σ�һ����������ɱ�ʾ --> -2**31 -1 �� 2**31 -1                 --> 0 �� 2**32 -1
//4.long(�����Σ�����һ���ϴ������--> -2**31 -1 �� 2**31 -1               --> 0 �� 2**32 -1
//5.long long���ӳ����Σ�һ���ǳ������� --> -2**63-1 �� 2**63 -1           --> 0 �� 2**64 -1
//����Ҫ���λ��������λ��unsigned

//С���������
//float:���Ա�ʾ6λ����
//double:���ȷ�Χ������6λ���ϣ�

//sizeof������ʵ��ռ���ֽڵĴ�С
//sizeof���Բ����������ͣ������������Ĵ�С
//�����Ƶ�λ����8λ(��Ϊ������еļ�����λ�Ƕ����ƣ�����һ���ֽڼ�8�������ƣ�����char����ֵ����ת����10����λ��-2**n -1�� 2**n -1�����ؼ������͵ķ�Χ������ʾ
//ͬʱ���λ��Ϊ����������λ������n��Ҫ��ȥ1������Ҫ���λ��������λ��unsigned

int get_size()
{	
	// char(�ַ��͵��ֽڴ�С��
	printf("sizeof char=%d \n", sizeof(char)); // �ֽڴ�СΪ1

	// short(�����ε��ֽڴ�С
	printf("sizeof shot=%d \n", sizeof(short)); // �ֽڴ�СΪ2

	// int �����ε��ֽڴ�С��
	printf("sizeof int=%d \n", sizeof(int)); // �ֽڴ�СΪ4

	// long �������͵��ֽڴ�С��
	printf("sizeof long=%d \n", sizeof(long)); // �ֽڴ�СΪ4

	//long long���ӳ����ε��ֽڴ�С��
	printf("sizeof longlong=%d \n", sizeof(long long)); // �ֽڴ�СΪ8

	printf("sizeof float=%d \n", sizeof(float)); // �ֽڴ�СΪ 4

	printf("sizeof double = %d \n ", sizeof(double)); // �ֽڴ�СΪ 8

	return 0;
}

//���⣺����һ���ַ�����letter,�����ʼ��Ϊ��д��ĸA,ͨ��ASCII�еĹ�ϵ������д��ĸA,���Сд��ĸa,����Сд��ĸa��ӡ����
int ASCII_letter()
{
	int letter = 'A';
	letter = letter + 32;

	printf("letter=%c \n", letter);
	return 0;
}
//int��ʾ�����ķ����������������ͣ�integer��
//main��ʾ������
/*int main()
{	
	//�����еı�����������������ʹ��
	int result;
	int get_sizes;
	int letter;
	printf("Hello World \n");

	result = add(2, 3);
	printf("%d \n", result);

	get_sizes = get_size();
	printf("%d \n ", get_sizes);

	letter = ASCII_letter();
	//return����ʾ�����ķ���ֵ
	return 0;						
}
*/

//��ʶ��������������Ͷ���֮�����ʹ�ã�add, a, b, result�ȶ��Ǳ�ʶ����
//��ʶ�����������
//1.��ʶ��������Сд��ĸ����д��ĸ�����ֺ��»�������
//2.��ʶ���ĵ�һ���ַ���������ĸ���»��ߣ�����������
//3.��ʶ�������ִ�Сд��
