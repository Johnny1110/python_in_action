class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        return self.process(s, numRows)

    def process(self, data, numRows):
        ans_str = ''
        data_len = len(data)
        for row in range(numRows):
            full_skip_step = (numRows-1)*2
            if full_skip_step == 0 or len(data) == 0:
                # 直接返回原本 data
                return data
            first_skip_step = (numRows-1-row)*2
            sec_skip_step = full_skip_step-first_skip_step

            round_time = int(len(data)/numRows)

            current_index = row
            try:
                ans_str += data[current_index]
                for time in range(round_time+1):
                    if first_skip_step != 0:
                        current_index += first_skip_step
                        ans_str += data[current_index]
                    if sec_skip_step != 0:
                        current_index += sec_skip_step
                        ans_str += data[current_index]
            except Exception:
                continue

        return ans_str


if __name__ == '__main__':
    s = ""
    numRows = 3
    sol = Solution()
    user_ans = sol.convert(s, numRows)
    act_ans = ""
    print("回答: ", user_ans)
    print("答案: ", act_ans)
    try:
        assert user_ans.__eq__(act_ans)
        print("結果: 正確")
    except Exception:
        print("結果: 錯誤")