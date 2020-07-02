class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        return self.process(x)

    def process(self, x):
        x_str = str(x)
        reversed_x = ''
        for num in reversed(range(len(x_str))):
            reversed_x += x_str[num]

        return x_str.__eq__(reversed_x)


if __name__ == '__main__':
    sol = Solution()
    input = 121
    valid = True
    user_ans = sol.isPalindrome(input)
    try:
        assert user_ans.__eq__(valid)
        print("正確")
    except Exception:
        print("錯誤")