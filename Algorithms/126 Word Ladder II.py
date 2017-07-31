class Solution(object):
    def findLadders(self, beginWord, endWord, wordList):
        """
        :type beginWord: str
        :type endWord: str
        :type wordList: List[str]
        :rtype: List[List[str]]
        """
        def can_be_next(s, d):
            repeat = 0
            for __ in range(len(s)):
                if s[__] != d[__]:
                    repeat += 1
                if repeat > 1:
                    return False
            return True

        result = [beginWord]
        current = beginWord
        for word in wordList:
            if can_be_next(current, word):
                result.append(word)
                current = word
                if current == endWord:
                    break
            else:
                continue

        return result


if __name__ == "__main__":
    test_case = [
        ("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"])
    ]
    solution = Solution()
    for t in test_case:
        r = solution.findLadders(*t)
        print r
