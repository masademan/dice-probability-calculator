import sys
import shutil

def moreSums(found_sums, new_vals):
    if len(found_sums) == 0:
        return {val: 1 for val in new_vals}

    new_sums = {}
    for found_sum in found_sums:
        for val in new_vals:
            new_sum = found_sum + val
            if new_sum not in new_sums:
                new_sums[new_sum] = 0
            new_sums[new_sum] += found_sums[found_sum]
    return new_sums

def histogram(data, num_chars_max=100):
    max_count = max(data.values())
    longest_char_len = len(prettyPrintNums(max(data.keys())))
    sorted_keys = sorted(data.keys())
    num_chars_per_val = {}

    for val in sorted_keys:
        num_chars = data[val] * (num_chars_max - longest_char_len - 2) / max_count
        num_chars_per_val[val] = num_chars

    num_before_collapse = 3
    print_status_per_val = {val: 2 for val in data}
    same_counter = 0
    for index in range(1, len(sorted_keys)):
        current_val = sorted_keys[index]
        prev_val = sorted_keys[index - 1]

        prev_num_chars = num_chars_per_val[prev_val]
        prev_num_chars = int(prev_num_chars) + (1 if prev_num_chars % 1 >= 0.5 else 0)
        
        num_chars = num_chars_per_val[current_val]
        num_chars = int(num_chars) + (1 if num_chars % 1 >= 0.5 else 0)

        if prev_num_chars + num_chars == 0 and index < len(sorted_keys) - 1:
            same_counter += 1
        else:
            if same_counter >= num_before_collapse:
                max_offset = num_before_collapse + 2
                if index == len(sorted_keys) - 1: max_offset -= 2

                for offset in range(1, max_offset):
                    offset_index = index - offset
                    if offset_index > 0:
                        offset_val = sorted_keys[offset_index]
                        print_status_per_val[offset_val] = min(2, print_status_per_val[offset_val] + 1)
                        if offset < num_before_collapse + 1:
                            print_status_per_val[offset_val] = min(2, print_status_per_val[offset_val] + 1)

            same_counter = 0
            continue

        if same_counter >= num_before_collapse:
            prev_print_status = print_status_per_val[prev_val]
            print_status_per_val[current_val] = max(0, prev_print_status - 1)

    """
    Make it so that repeated empty string are collapsed
    Example:
    1: 
    2:
    3:
    4:
    5:
    6:
    7:
    8:
    9:
    10:
    11:
    12:

    Turns into:
    1:
    2:
    3:
    ...
    ...
    10:
    11:
    12:
    """

    """
    Use a dict with val to int to print when dict[val] is 2, when dict[val] is 1 print "...", and when dict[val] is 0, don't print anything
    A sliding window to create this dict, this makes it so that if it doesn't make sense to collapse the empty strings, it won't
    Example of the dict being made with the example above:
    {1: 2, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 2}
    {1: 2, 2: 2, 3: 2, 4: 1, 5: 2, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 2}
    {1: 2, 2: 2, 3: 2, 4: 1, 5: 0, 6: 2, 7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 2}
    {1: 2, 2: 2, 3: 2, 4: 1, 5: 0, 6: 0, 7: 2, 8: 2, 9: 2, 10: 2, 11: 2, 12: 2}
    ...
    {1: 2, 2: 2, 3: 2, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 2}
    {1: 2, 2: 2, 3: 2, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0}
    {1: 2, 2: 2, 3: 2, 4: 1, 5: 0, 6: 0, 7: 0, 8: 0, 9: 1, 10: 2, 11: 2, 12: 2}
    """

    for val in sorted_keys:
        print_status = print_status_per_val[val]

        if print_status == 2:
            pretty_print_val = prettyPrintNums(val)
            num_spaces = longest_char_len - len(pretty_print_val)
            print(f"{pretty_print_val}{" " * num_spaces}: ", end="")

            num_chars = num_chars_per_val[val]

            if int(num_chars) > 0:
                print("="*int(num_chars), end="")
                if num_chars%1 >= 0.5:
                    print(".")
                else:
                    print()
            elif num_chars >= 0.5:
                print(".")
            else:
                print("")
        elif print_status == 1:
            print("...")

def diceSumPossibilities(numDice, diceNums):
    if numDice == 0:
        return {}
    return moreSums(diceSumPossibilities(numDice - 1, diceNums), diceNums)

def bestDiceSum(numDice, diceNums, data=None):
    if not data:
        data = diceSumPossibilities(numDice, diceNums)

    best_sum = 0
    best_values = []

    for value in data:
        if data[value] > best_sum:
            best_sum = data[value]
            best_values = []
        if data[value] == best_sum:
            best_values.append(value)
    return best_values, data

def betterRound(num):
    new_num = int(num)

    if num % 1 >= 0.5:
        return new_num + 1
    return new_num

def prettyPrintNums(num, scientific=False, digits_of_precision=2):
    scientific_num_threshold = 10**19

    if not scientific or num < scientific_num_threshold:
        str_num = str(num)
        reversed_num = str_num[::-1]
        reassembled_nums = []
        for i in range(len(reversed_num)):
            reassembled_nums.append(reversed_num[i])
            if i % 3 == 2 and i < len(reversed_num) - 1:
                reassembled_nums.append(",")
        return "".join(reassembled_nums)[::-1]
    else:
        str_num = str(num)

        first_part = betterRound(int(str_num[:digits_of_precision + 2]) / 10) / (10 ** digits_of_precision)
        second_part = len(str_num) - 1

        return f"{first_part} * 10^{second_part}"

def printBestDiceSum(numDice, diceNums, data=None):
    best_vals, data = bestDiceSum(numDice, diceNums, data)
    num_combos = sum(data.values())
    digits_of_precision = 2
    scientific = True

    if len(best_vals) == 0:
        print("ERROR: Got 0 values for the best vals")
        return
    elif len(best_vals) == 1:
        print((f"Best dice sum is {prettyPrintNums(best_vals[0], scientific=scientific, digits_of_precision=digits_of_precision)} with it "
               f"appearing {prettyPrintNums(data[best_vals[0]], scientific=scientific, digits_of_precision=digits_of_precision)} out of "
               f"{prettyPrintNums(num_combos, scientific=scientific, digits_of_precision=digits_of_precision)} times"))
    elif len(best_vals) == 2:
        print((f"Best dice sums are {prettyPrintNums(best_vals[0], scientific=scientific, digits_of_precision=digits_of_precision)} and "
               f"{prettyPrintNums(best_vals[1], scientific=scientific, digits_of_precision=digits_of_precision)} with them both appearing "
               f"{prettyPrintNums(data[best_vals[0]], scientific=scientific, digits_of_precision=digits_of_precision)} out of "
               f"{prettyPrintNums(num_combos, scientific=scientific, digits_of_precision=digits_of_precision)} times"))
    elif len(best_vals) >= 3:
        listed_vals = []

        for index in range(len(best_vals) - 1):
            listed_vals.append(f"{prettyPrintNums(best_vals[index], scientific=scientific, digits_of_precision=digits_of_precision)}, ")
        listed_vals.append(f"and {prettyPrintNums(best_vals[-1], scientific=scientific, digits_of_precision=digits_of_precision)}")

        print((f"Best dice sums are {"".join(listed_vals)} with them each appearing {prettyPrintNums(data[best_vals[0]], scientific=scientific, digits_of_precision=digits_of_precision)} "
              f"out of {prettyPrintNums(num_combos, scientific=scientific, digits_of_precision=digits_of_precision)} times"))

    print(f"This is a probability of {data[best_vals[0]]*100/num_combos:.{digits_of_precision}f}%")

def isInt(num, msg = None):
    try:
        return int(num)
    except:
        if not msg:
            print("ERROR: Input must be an integer", file=sys.stderr)
        else:
            print(msg, file=sys.stderr)
        sys.exit(-1)

def parseNumsList(list_nums):
    split_nums = list_nums.split(", ")

    for index in range(len(split_nums)):
        split_nums[index] = isInt(split_nums[index], msg=f"ERROR: Numbers at index {index} of list_nums must be an integer")
    
    return split_nums

def parseDiceNums(dice_nums):
    parse_type = ""

    if dice_nums[0] == "(" and dice_nums[-1] == ")":
        parse_type = "R"
    elif dice_nums[0] == "[" and dice_nums[-1] == "]":
        parse_type = "L"
    
    if not parse_type:
        print("ERROR: Invalid dice_nums given, neither list nor range", file=sys.stderr)
        sys.exit(-1)

    parsed_num_list = parseNumsList(dice_nums[1:-1])
    if parse_type == "R":
        return list(range(parsed_num_list[0], parsed_num_list[1] + 1))
    return parsed_num_list

def parseHistogramWidth(histogram_width):
    split_histogram_settings = histogram_width.split("/")

    if len(split_histogram_settings) == 1:
        return isInt(histogram_width, msg="ERROR: The width of the histogram must be inputted as an integer")
    elif len(split_histogram_settings) == 2:
        return shutil.get_terminal_size().columns * isInt(split_histogram_settings[0], msg="ERROR: The numerator of the histogram fraction must be an integer") /\
                                                    isInt(split_histogram_settings[1], msg="ERROR: The denominator of the histogram fraction must be an integer")

    print("ERROR: Invalid histogram settings inputted, fraction can only have 2 parts", file=sys.stderr)
    sys.exit(-1)


if __name__ == "__main__":
    default_num_dice = 3
    num_dice = input(f"Num dice (default={default_num_dice}): ")
    num_dice = isInt(num_dice, msg="ERROR: num_dice must be an integer") if len(num_dice) > 0 else default_num_dice

    default_dice_nums = "(1, 6)"
    print("\nNums on the dice")
    print("For a list of nums, write in the form '[A, B, C, ..., X, Y, Z]', i.e., '[1, 2, 3, 4]', the ', ' matters!")
    print("For an inclusive range, write in the form '(S, E)', i.e., '(1, 6)' for '[1, 2, 3, 4, 5, 6]', again, the ', ' matters!")
    dice_nums = input(f"Input (default={default_dice_nums}): ")
    if len(dice_nums) == 0: dice_nums = default_dice_nums
    dice_nums = parseDiceNums(dice_nums)

    print("\nMax horizontal chars for histogram")
    print("To disable the histogram, input '-1'")
    print("For a fraction of the terminal width, write in the form 'A/B' with no spaces")
    print("For an absolute width value, write in the form 'A' like a normal number")
    default_histogram_width = shutil.get_terminal_size().columns - 5
    histogram_width = input(f"Input (default=current terminal width - 5 [{default_histogram_width}]): ")
    if histogram_width == "-1": histogram_width = -1
    elif histogram_width == "": histogram_width = default_histogram_width
    else: histogram_width = parseHistogramWidth(histogram_width)

    print("\n")

    data = diceSumPossibilities(num_dice, dice_nums)
    printBestDiceSum(num_dice, dice_nums, data)

    if histogram_width != -1:
        print()
        histogram(data, histogram_width)

    print()