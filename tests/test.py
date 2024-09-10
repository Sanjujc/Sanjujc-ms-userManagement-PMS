def findOptimalResources(arr, k):
    n = len(arr)

    # Edge case: if k is greater than the length of the array
    if k > n:
        return -1

    max_sum = -1
    current_sum = 0
    count_map = {}

    # Initialize the sliding window
    for i in range(k):
        if arr[i] in count_map:
            count_map[arr[i]] += 1
        else:
            count_map[arr[i]] = 1
        current_sum += arr[i]

    # Check if the initial window is valid
    if len(count_map) == k:
        max_sum = current_sum

    # Slide the window across the array
    for i in range(k, n):
        # Remove the element going out of the window
        element_out = arr[i - k]
        count_map[element_out] -= 1
        current_sum -= element_out

        if count_map[element_out] == 0:
            del count_map[element_out]

        # Add the new element coming into the window
        element_in = arr[i]
        if element_in in count_map:
            count_map[element_in] += 1
        else:
            count_map[element_in] = 1
        current_sum += element_in

        # Check if the current window is valid
        if len(count_map) == k:
            max_sum = max(max_sum, current_sum)

    return max_sum if max_sum != -1 else -1


# Sample usage
arr1 = [1, 2, 7, 7, 4, 3, 6]
k1 = 3
print(findOptimalResources(arr1, k1))  # Output should be 14

arr2 = [1, 3, 3, 1]
k2 = 3
print(findOptimalResources(arr2, k2))  # Output should be -1
