from typing import List

DEBUG = False

class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        coins.sort()
        # best_result = 2**31

        # def update_best_result(result):
        #     nonlocal best_result
        #     if result < best_result:
        #         print(f" update best_result={result}")
        #         best_result = result

        def update_solution(solution, coin, count):
            if solution is None:
                return
            n = solution.get(coin)
            if n is None:
                solution[coin] = count
            else:
                solution[coin] = solution[coin] + count

        call_count = 0
        # call count=89011
        # call count=99701

        def countCoins(coins, endIdx, amount, memo, depth, coin_cnt):
            nonlocal call_count
            call_count += 1

            # if coin_cnt >= best_result:
            #     if DEBUG:
            #         print(f" skip countCoins: amount={amount} depth={depth} coin_cnt={coin_cnt}")
            #     return -1

            if DEBUG:
                print(f" countCoins start: amount={amount} depth={depth} coin_cnt={coin_cnt}")

            result = memo.get(amount)
            if result is not None:               
                if DEBUG:
                    print(f" found cached result for amount={amount} depth={depth} result={result}")
                return result

            result = [-1, {}]           

            if amount == 0:
                result = [0, {}]                
            elif amount < coins[0]:
                result = [-1, {}]
            else:
                while coins[endIdx] > amount:
                    if DEBUG:
                        print(f" decrease endIdx={endIdx}")
                    endIdx -= 1

                if endIdx == 0:
                    if amount % coins[endIdx] == 0:
                        if DEBUG:
                            print(f" use single coin={coins[endIdx]}")
                        result = [amount // coins[endIdx], {coins[endIdx]:amount // coins[endIdx] }]
                    else:
                        result = [-1, {}]
                else:
                    for i in reversed(range(endIdx+1)): 
                        amount2 = amount-coins[i]
                        sub_result = countCoins(coins, endIdx, amount2, memo, depth+1, coin_cnt+1)
                        if sub_result[0] >= 0:
                            if DEBUG:
                                print(f"  amount={amount-coins[i]} tmp result={sub_result}")
                            if result[0] < 0 or sub_result[0]+1 < result[0]: 
                                result = sub_result.copy()
                                result[0] = result[0] + 1
                                update_solution(result[1], coins[endIdx], 1)  

            # if amount == 0:
            #     print(f"  memo.0={result}")
            memo[amount] = result             
            # update_solution(solution, coins[endIdx], 1)
            # if result_solution is not None:
            #     for k, v in result_solution.items():
            #         update_solution(solution, k, v)
                               
            return result
        #end of def countCoins

        if amount == 0:
            return 0
            
        # for k in reversed(range(len(coins))):
        #     largest_coin = coins[k]
        #     largest_coin_count = amount // largest_coin
        #     if True or DEBUG:
        #         print(f"  k={k} largest_coin={largest_coin} largest_coin_count={largest_coin_count}")
        #     if largest_coin_count < 1:
        #         continue

        #     # if largest_coin_count >= best_result:
        #     #     continue
            
        #     if amount % largest_coin > 0:
        #         if largest_coin_count >= best_result:
        #             continue

        #         if k == 0:
        #             continue

               
        #         for m in reversed(range(1, min(largest_coin_count+1, best_result+1))):
        #             memo2 = {}
        #             for j in range(k):
        #                 memo2[coins[j]] = 1    

        #             amount2 = amount - m * largest_coin
        #             result2 = countCoins(coins, k-1, amount2, memo2, 0, 0)
        #             print(f" k={k} m={m} amount2={amount2} result2={result2} coins={coins[:k]}")
        #             # k=3 m=14 amount2=509 result2=5 coins=[5, 188, 306]
        #             if result2 > 0:
        #                 update_best_result(min(m+result2, best_result))
        #     else:
        #             update_best_result(min(best_result, largest_coin_count))
        #     print(f" k={k} best_result={best_result}")

        # print(f" call count={call_count}")
        # return -1 if best_result == 2**31 else best_result           
                   
                


        memo={}
        for c in coins:
            memo[c] = [1, {c: 1}]
 
        ret = countCoins(coins, len(coins)-1, amount, memo, 0, 0)   
        print(f" call count={call_count} solution={ret}")
        return ret[0]        

if __name__ == '__main__':
    import sys
    import time

    DEBUG = False
    selected_tests = None  # None: run all; else set of 1-based indices from argv

    for a in sys.argv[1:]:
        if a == "-d":
            DEBUG = True
        elif a.replace(",", "").isdigit() and "," in a:
            if selected_tests is None:
                selected_tests = set()
            for part in a.split(","):
                part = part.strip()
                if part.isdigit():
                    selected_tests.add(int(part))
        elif a.isdigit():
            if selected_tests is None:
                selected_tests = set()
            selected_tests.add(int(a))
        else:
            print(
                f"Unknown argument: {a!r} (use -d and/or 1-based test indices, e.g. 1 2 4)",
                file=sys.stderr,
            )
            sys.exit(2)

    if selected_tests is not None and len(selected_tests) == 0:
        print("Test selection is empty.", file=sys.stderr)
        sys.exit(2)
    else:
        print(f"selected_tests={selected_tests}")

    tests = [
        {"n": 1, "coins": [1, 2, 5], "amount": 11, "expected": 3},
        {"n": 2, "coins": [2], "amount": 3, "expected": -1},
        {"n": 3, "coins": [1], "amount": 0, "expected": 0},
        {"n": 4, "coins": [1], "amount": 1, "expected": 1},
        {"n": 5, "coins": [1, 3, 4], "amount": 6, "expected": 2},
        {"n": 6, "coins": [186, 419, 83, 408], "amount": 6249, "expected": 20},
        {"n": 7, "coins": [1, 2147483647], "amount": 2, "expected": 2},
        {"n": 8, "coins": [3, 7], "amount": 5, "expected": -1},
        {"n": 9, "coins": [1, 2, 5, 10, 13], "amount": 30, "expected": 3},
        {"n": 10, "coins": [1, 2, 5], "amount": 100, "expected": 20},
        {"n": 11, "coins": [1, 3, 5], "amount": 8, "expected": 2},
        {"n": 12, "coins": [216,94,15,86], "amount": 5372, "expected": 26},
        {"n": 13, "coins": [5,306,188,467,494], "amount": 7047, "expected": 18},
        {"n": 14, "coins": [5,306,188], "amount": 509, "expected": 5},
        {
            "n": 15,
            "coins": list(range(1, 101)),
            "amount": 1097,
            "expected": 11,
        },
        {
            "n": 16,
            "coins": [2,4,6,8,10,12,14,16,18,20,22,24],
            "amount": 9999,
            "expected": -1,
        },
    ]

    solution = Solution()

    t1 = int(time.time() * 1000)

    for index, test in enumerate(tests, 1):
        if selected_tests is not None and test["n"] not in selected_tests:
            continue

        coins = test["coins"]
        amount = test["amount"]
        expected = test["expected"]

        try:
            print(f"\nTEST {index} coins={coins} amount={amount}")
            if DEBUG:
                print(f"  expected={expected}")
            result = solution.coinChange(coins, amount)
            if result != expected:
                print(f"test {index} FAIL: n={test['n']}")
                print(f"  got:      {result}")
                print(f"  expected: {expected}")
            else:
                print(f"test {index} OK: n={test['n']} (result={result})")
        except Exception as e:
            print(f"test {index} ERROR: {e}")
            raise

    t2 = int(time.time() * 1000)
    print(f"Total test duration: {t2 - t1} ms")
