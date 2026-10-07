DEBUG = False

# TC O(n) SC O(n) solution
class Solution:
    def candy(self, ratings: list[int]) -> int:
        n = len(ratings)


        candies = [1 for _ in range(n)] # default minimal candy
        prev_slop = 0
        last_rate_idx = -1

        def update_candies(slop_start:int, slop_end:int, slop:int):
            nonlocal prev_slop, last_rate_idx

            if DEBUG:
                print(f"update candies slop={slop} from {slop_start} to {slop_end}: ratings={ratings[slop_start: slop_end+1]}")

            if slop > 0: # step up
                for i in range(slop_start, slop_end+1):
                    candies[i] = max(i-slop_start+1, candies[i])
                prev_slop = slop
                last_rate_idx = slop_end
            elif slop < 0: # step down
                for i in range(slop_end, slop_start-1, -1):
                    candies[i] = max(slop_end-i+1, candies[i])
                prev_slop = slop
                last_rate_idx = slop_end
            else: # flat slop
                # for i in range(slop_start, slop_end+1):
                #     candies[i] = 1
                prev_slop = slop
                last_rate_idx = slop_end


        slop = 0  # slop = -1: step down; slop = 1: step up; slop = 0: uknown
        slop_start = 0 # inclusive

        i=0
        while i<n:
            if DEBUG:
                print(f"    START i={i} slop={slop}  slop_start={slop_start}")

            curr_rating = ratings[i]
            if i == n-1:
                update_candies(slop_start, i, slop)
                break

            # look ahead means slop of ratings[i] is known
            la_rating = ratings[i+1] # look ahead rating
            if DEBUG:
                print(f"        curr_rating={curr_rating} la rating={la_rating}")

            if slop > 0:
                if la_rating > curr_rating: # keep step up
                    i += 1
                elif la_rating < curr_rating: # curr_rating is peak
                    update_candies(slop_start, i, slop)

                    slop_start = i  # start next step down slop. ratings[i] is shared!
                    i += 1
                    slop = -1    
                else: # la_rating == curr_rating: # end current slop
                    update_candies(slop_start, i, slop)

                    # start from scatch at ratings[i+1]
                    i += 1
                    slop_start = i
                    slop = 0                
            elif slop < 0:
                if la_rating < curr_rating: # keep step down
                    i += 1
                elif la_rating > curr_rating: # curr_rating is bottom
                    update_candies(slop_start, i, slop)

                    slop_start = i # start new step up slop. ratings[i] is shared!
                    slop = 1
                    i += 1
                else: # flat slop
                    update_candies(slop_start, i, slop)

                    # start from scratch
                    i += 1
                    slop_start = i
                    slop = 0                                        
            else: # slop = 0
                if la_rating < curr_rating: # start step down
                    slop_start = i
                    slop = -1
                    i += 1
                elif la_rating > curr_rating: # start step up
                    slop_start = i
                    slop = 1
                    i += 1
                else: # flat
                    i += 1        
        if DEBUG:
            print(f"candies={candies}")
        answer = 0
        for c in candies:
            answer += c
        return answer    
