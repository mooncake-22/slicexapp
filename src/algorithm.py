import math

class Algorithm(object):

    def __init__(self):
        return

    def run(self, target_throughput: list, current_throughput: list, total_prb_avail: int, total_prb_used: list):
        
        # Check
        if sum(target_throughput) == 0:
            dedicated_ratio = [0] * len(total_prb_used)
            if sum(current_throughput) == 0:
                min_ratio = [math.floor(100 / len(total_prb_used))] * len(total_prb_used)
            else:
                min_ratio = [1/len(current_throughput)] * len(current_throughput)
            return dedicated_ratio, min_ratio
        
        if sum(total_prb_used) == 0 or sum(current_throughput) == 0:
            dedicated_ratio = [0] * len(total_prb_used)
            min_ratio = [x / sum(target_throughput) * 100  for x in target_throughput]
            return dedicated_ratio, min_ratio

        return self.alloc_prb(target_throughput, current_throughput, total_prb_used)


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
        current_sum = 0
        target_sum = 0

        throughput_ratio = sum(current_throughput) / sum(target_throughput)
        for i in range(0, len(current_throughput)):
            if current_throughput[i] == 0:
                diff_throughput.append(0)
            else:
                diff_throughput.append(target_throughput[i] - current_throughput[i])
                # diff_throughput.append(current_throughput[i] - target_throughput[i])
        print(target_throughput)
        print(current_throughput)
        print(total_prb_used)

        for i in range(0, len(current_throughput)):
            if current_throughput[i] == 0:
                total_prb_used[i] = 10
            else:
                total_prb_used[i] = math.ceil(1.05 * total_prb_used[i] * target_throughput[i] / current_throughput[i] + 1)

        # # Find the most value &&  value > 0 
        # v = diff_throughput.index(max(diff_throughput))

        # # Find the most value && value < 0
        # k = diff_throughput.index(min(diff_throughput))

        # # Calculate the exceed portion of PRB of v
        # if current_throughput[v] > 0:
        #     p = math.floor(0.1 * diff_throughput[v] * total_prb_used[v] / current_throughput[v])
        # else:
        #     p = 0

        # # Increase and descrease
        # total_prb_used[v] = total_prb_used[v] + p

        # total_prb_used[k] = total_prb_used[k] - p

        # Calculate ratio
        if(sum(total_prb_used)>100):
            dedicated_ratio = [math.floor(x / sum(total_prb_used) * 100)  for x in total_prb_used]
        else:
            dedicated_ratio = total_prb_used
        
        min_ratio = dedicated_ratio

        print(dedicated_ratio, min_ratio)

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
#         target_throughput = [600000, 400000, 400000], 
#         current_throughput = [639856, 404224, 526720],
#         total_prb_avail = 106, 
#         total_prb_used = [39, 25, 36]
#     )
   
#     print(dedicated_ratio, min_ratio)