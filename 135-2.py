DEBUG = False

# TC O(n) SC O(1) solution
class Solution:
    def candy(self, ratings: list[int]) -> int:
        n = len(ratings)


        prev_slope = 0
        last_rate_idx = -1
        last_peak_extra_candies = 0   # last extra candies to a peak rating
        total_candies = n

        # update either up slope or down slops
        def update_up_down_slope_candies(slop_start:int, slop_end:int, slope:int):
            nonlocal prev_slope, last_rate_idx, last_peak_extra_candies, total_candies

            if DEBUG:
                print(f"update candies slope={slope} from {slop_start} to {slop_end}: ratings={ratings[slop_start: slop_end+1]}")
                print(f"    prev_slope, last_rate_idx, last_candies, total_candies={(prev_slope, last_rate_idx, last_peak_extra_candies, total_candies)}")

            if slope > 0: # step up
                for i in range(slop_start, slop_end+1):
                    total_candies += (i-slop_start)
                prev_slope = slope
                last_rate_idx = slop_end
                last_peak_extra_candies = slop_end-slop_start
                if DEBUG:
                    print(f"    total candies={total_candies}")
            elif slope < 0: # step down
                for i in range(slop_end, slop_start-1, -1):
                    if i == last_rate_idx and prev_slope > 0:
                        total_candies -= last_peak_extra_candies
                        total_candies += max(slop_end-i, last_peak_extra_candies)
                    else:
                        total_candies += (slop_end-i)    
                prev_slope = slope
                last_rate_idx = slop_end
                last_peak_extra_candies = 0
                if DEBUG:
                    print(f"    total candies={total_candies}")


        slope = 0  # slope = -1: step down; slope = 1: step up; slope = 0: uknown
        slope_start = 0 # slope start index

        i=0
        while i<n:
            if DEBUG:
                print(f"   i={i} slope={slope}  slop_start={slope_start}")

            curr_rating = ratings[i]
            if i == n-1:
                if slope != 0:
                    update_up_down_slope_candies(slope_start, i, slope)
                break

            # look ahead means slope of ratings[i] is known
            la_rating = ratings[i+1] # look ahead rating
            if DEBUG:
                print(f"        curr_rating={curr_rating} la rating={la_rating}")

            if slope > 0:
                if la_rating < curr_rating: # curr_rating is peak
                    update_up_down_slope_candies(slope_start, i, slope)
                    slope_start = i  # start next step down slope. ratings[i] is shared!
                    slope = -1    
                elif la_rating == curr_rating: # end current slope, which reach peak
                    update_up_down_slope_candies(slope_start, i, slope)
                    # start from scatch at ratings[i+1]
                    slope_start = i+1
                    slope = 0                
            elif slope < 0:
                if la_rating > curr_rating: # curr_rating is bottom
                    update_up_down_slope_candies(slope_start, i, slope)

                    slope_start = i # start new step up slope. ratings[i] is shared!
                    slope = 1
                elif la_rating == curr_rating: # flat slope
                    update_up_down_slope_candies(slope_start, i, slope)
                    # start from scratch
                    slope_start = i+1
                    slope = 0                                        
            else: # slope = 0
                if la_rating < curr_rating: # start step down
                    slope_start = i
                    slope = -1
                elif la_rating > curr_rating: # start step up
                    slope_start = i
                    slope = 1

            i += 1        

        return total_candies
