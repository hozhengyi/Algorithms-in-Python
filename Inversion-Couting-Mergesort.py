'''
My implementation using mergesort to count inversions given two arrays
'''

def mergeSortCountInversions(arr):
    len_arr = len(arr)       
    new_arr = []
    i,j=0,0
    global result #Declare a global var to store inversion counts
    if len_arr == 1:#Base case
        return arr
    #split and recurses
    split = len_arr//2
    left_half, right_half = arr[:split], arr[split:]
    sorted_left = mergeSortCountInversions(left_half)
    sorted_right = mergeSortCountInversions(right_half)
    len_sorted_left = len(sorted_left)
    #merging and counting procedure
    try:
        while True:
            if sorted_left[i] <= sorted_right[j]:
                new_arr.append(sorted_left[i])
                i+=1
            else:
                new_arr.append(sorted_right[j])
                result += (len_sorted_left - (i))
                j+=1 
    except:
        new_arr = new_arr + sorted_left[i:] + sorted_right[j:]
            
    return new_arr
