import math

class Algorithm(object):

    def __init__(self):
        return

    def run(self, target_throughput: list, current_throughput: list, total_prb_avail: int, total_prb_used: list):
        
        # Check
        if sum(target_throughput) == 0:
            dedicated_ratio = [0] * len(total_prb_used)
            min_ratio = [1/len(current_throughput)] * len(current_throughput)
            return dedicated_ratio, min_ratio
        
        if sum(total_prb_used) == 0 or sum(current_throughput) == 0:
            dedicated_ratio = [0] * len(total_prb_used)
            min_ratio = [x / sum(target_throughput) * 100  for x in target_throughput]
            return dedicated_ratio, min_ratio

        if self.check_overload(target_throughput, current_throughput, total_prb_avail, total_prb_used) == True:
            dedicated_ratio = [x / sum(target_throughput) * 100 for x in target_throughput]
            min_ratio = dedicated_ratio
            return dedicated_ratio, min_ratio
        
        else:
            satisfied_flag = self.check_satisfied(target_throughput, current_throughput)
            if sum(satisfied_flag) == len(satisfied_flag):
                # Keep the same setting
                dedicated_ratio = [x / sum(total_prb_used) * 100 for x in total_prb_used]
                min_ratio = dedicated_ratio

                return dedicated_ratio, min_ratio
            
            else:
                # Configure the setting
                return self.alloc_prb(target_throughput, current_throughput, target_throughput)


    def check_overload(self, target_throughput, current_throughput, total_prb_avail, total_prb_used):
        # Todo: check whether need this or not
        maximum_possible_throughput = sum(current_throughput) * total_prb_avail / sum(total_prb_used)
        maximum_expected_throughput = sum(target_throughput)
        
        if maximum_expected_throughput > maximum_possible_throughput:
            return True
        else:
            return False

    def check_satisfied(self, target_throughput, current_throughput):
        s = []
        for i in range(0, len(target_throughput)):
            if current_throughput[i] > target_throughput[i]:
                s.append(1)
            else:
                s.append(0)

        return s

    def alloc_prb(self, target_throughput: list, current_throughput: list, total_prb_used: list):

        diff_throughput = []
        for i in range(0, len(current_throughput)):
            diff_throughput.append(current_throughput[i] - target_throughput[i])

        print(diff_throughput)
        # Find the most value &&  value > 0 
        v = diff_throughput.index(max(diff_throughput))

        # Find the most value && value < 0
        k = diff_throughput.index(min(diff_throughput))

        # Calculate the exceed portion of PRB of v
        p = math.floor(0.1 * diff_throughput[v] * total_prb_used[v] / current_throughput[v])

        # Increase and descrease
        total_prb_used[v] = total_prb_used[k] - p

        total_prb_used[k] = total_prb_used[k] + p

        # Calculate ratio
        dedicated_ratio = [x / sum(total_prb_used) * 100  for x in total_prb_used]
        
        min_ratio = dedicated_ratio

        return dedicated_ratio, min_ratio

    def check_constrant(self, ratio: list):
        list_len = len(ratio)
        if ratio == [0] * list_len:
            return ratio
        else:
            checked_ratio = [math.floor(x) for x in ratio]
            checked_ratio[-1] = 100 - sum(checked_ratio[:-1])
            return checked_ratio


# if __name__ == "__main__":
#     a = Algorithm()
#     dedicated_ratio, min_ratio = a.run(
#         target_throughput = [100000, 100000, 200000], 
#         current_throughput = [0, 313968, 1160512],
#         total_prb_avail = 106, 
#         total_prb_used = [0, 0, 0]
#     )
   
#     print(dedicated_ratio, min_ratio)