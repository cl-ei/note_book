
class Solution(object):
    def isNumber(self, s):
        is_start = True
        has_dot = False
        has_e = False
        has_num = False
        has_blank = False
        end_with = ""
        for c in s:
            if "0" <= c <= "9":
                if has_blank:
                    return False
                else:
                    end_with = "n"
                    is_start = False
                    has_num = True
            elif c == ".":
                if has_dot or has_e or has_blank:
                    return False
                else:
                    end_with = "d"
                    is_start = False
                    has_dot = True
            elif c == "e":
                if has_e or is_start or not has_num:
                    return False
                else:
                    end_with = "e"
                    is_start = False
                    has_e = True
            elif c == " ":
                if is_start:
                    continue
                else:
                    has_blank = True
            elif c in "+-":
                if is_start or end_with == "e":
                    is_start = False
                    continue
                else:
                    return False
            else:
                return False

        return has_num and end_with in ["n", "d"]


if __name__ == "__main__":
    x = Solution()
    test_str = {
        "1": True,
        ".1": True,
        "1.": True,
        " 0": True,
        "1 ": True,
        "-1.": True,
        "46.e3": True,
        " 005047e+6": True,
        ". 1": False,
        ".": False,
        "1 4": False,
        "e": False,
        "e3": False,
        "0e": False,
        "3 .9": False,
        ".e1": False,
        "0e ": False,
        "1 .": False,
        "+ 1": False,
    }
    for _ in test_str:
        rst = x.isNumber(_)
        if rst != test_str[_]:
            print "Failed: [%s]" % _
            break
    else:
        print "Pass !"
