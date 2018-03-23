
void print_array(int *a, int start_index, int end_index){
    for(int i = start_index; i <= end_index; i++){
        printf("%d, ", a[i]);
    }
    printf("\n");
}

void quick_sort(int *a, int start_index, int end_index){

    if (end_index <= start_index || start_index < 0 || end_index < 0) {
        return;
    }

    int ref = *(a + end_index);

    int small_border = 0;
    int large_border = 0;
    int temp = 0;

    for (int i = start_index; i < end_index; i++) {
        if (*(a + i) <= ref) {
            if (large_border > small_border) {
                temp = *(a + start_index + small_border);
                *(a + start_index + small_border) = *(a + start_index + large_border);
                *(a + start_index + large_border) = temp;
            }

            small_border += 1;
            large_border += 1;

        } else {
            large_border += 1;
        }
    }
    *(a + end_index) = *(a + start_index + small_border);
    *(a + start_index + small_border) = ref;

    quick_sort(a, start_index, start_index + small_border - 1);
    quick_sort(a, start_index + small_border + 1, end_index);
}

void merge(int *a, int *temp_ptr, int start_index, int mid_index, int end_index){
    int arr_index = start_index;
    int arr2_index = mid_index + 1;
    int temp_index = start_index;

    while(arr_index < mid_index + 1 && temp_index < end_index + 1){
        if (a[arr_index] <= a[arr2_index]){
            temp_ptr[temp_index++] = a[arr_index++];
        }else{
            temp_ptr[temp_index++] = a[arr2_index++];
        }
    }
    while(arr_index <= mid_index){
        temp_ptr[temp_index++] = a[arr_index++];
    }
    while(arr2_index <= end_index){
        temp_ptr[temp_index++] = a[arr2_index++];
    }
    for (int i = start_index; i < temp_index; i++){
        a[i] = temp_ptr[i];
    }
}
void merge_sort(int *a, int *temp_ptr, int start_index, int end_index){
    int mid = 0;
    if (start_index >= end_index){
        return;
    }

    mid = (start_index + end_index)/2;
    merge_sort(a, temp_ptr, start_index, mid);
    merge_sort(a, temp_ptr, mid + 1, end_index);
    merge(a, temp_ptr, start_index, mid, end_index);
}
