class first_main:

    def first_list(self):
        list = [0, 1, 4, 9, 16]
        # 1.列表推导式
        print(first_main.list_fir(self))

        # 2.切片（切片是左闭右开）
        # 2.1:步数为正
        print(first_main.list_two(self, list))
        #
        # # 2.2:步数为负 (开始是第一位， 结束是第二位)
        print(first_main.list_three(self, list))

        # 3.排序（排序推荐用sorted函数，reverse=True是降序，不加上是升序）
        print(first_main.list_dict(self, list))

        return False

    def list_fir(self):
        list_ret = [i * i for i in range(5)]
        return list_ret

    def list_two(self, list):
        dict_list_two = {}
        first_get_num = list[::1]
        two_get_num = list[1::]  # 1, 4, 9, 16
        three_get_num = list[:2:]  # 0, 1

        dict_list_two["first_get_num"] = first_get_num
        dict_list_two["two_get_num"] = two_get_num
        dict_list_two["three_get_num"] = three_get_num

        return dict_list_two

    def list_three(self, list):
        dict_list_three = {}
        new_first_get_num = list[::-1] # 16, 9, 4, 1, 0
        new_two_get_num = list[:2:-1]  # 16, 9,
        new_three_get_num = list[1::-1]  # 1, 0

        dict_list_three["new_first_get_num"] = new_first_get_num
        dict_list_three["new_two_get_num"] = new_two_get_num
        dict_list_three["new_three_get_num"] = new_three_get_num

        return dict_list_three

    def list_dict(self, list):
        staus_list = [{'name':'mike','age':'19'},{'name':'peter','age':'20'},{'name':'lily','age':'18'}]
        print(type(staus_list))
        print(sorted(list))
        print("按年龄排序", sorted(staus_list, key=lambda x: x['age'], reverse=True))

    def first_dict(self):
        # 1.字典推导式
        dict = {
            "name": "mike", "age": 18, "Number": "15926811113"
        }
        dict_ret = {k: v for (k, v) in dict.items()}
        if dict_ret:
            return dict_ret

        return False


xcl = first_main()
xcl.first_list()
