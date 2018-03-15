void quick_sort(int *a, int start, int end){
    if (end <= start || start < 0) return;

    int ref = *(a + end - 1);

    int small_border = 0;
    int large_border = 0;
    int temp = 0;

    for (int i = start; i < end - 1; i++){
        if (*(a + i) <= ref){  // !important!
            if(large_border > small_border) {
                temp = *(a + start + small_border);
                *(a + start + small_border) = *(a + start + large_border);
                *(a + start + large_border) = temp;
            }

            small_border += 1;
            large_border += 1;

        }else{
            large_border += 1;
        }
    }

    *(a + end - 1) = *(a + start + small_border);
    *(a + start + small_border) = ref;

    quick_sort(a, start, start + small_border);
    quick_sort(a, start + small_border + 1, end);
}
