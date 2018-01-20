#include <iostream>
#include <stdlib.h>

using namespace std;

void right_value_ref_arg(int&& arg){
    cout << "space: " << arg;
}

int count_numbers(int x, ...){
    va_list args_pointer;
    va_start(args_pointer, x);
    cout << *va_arg(args_pointer, char*) << endl;
    va_end(args_pointer);
}

void malloc_test(){

}

int main() {
    // right_value_ref_arg(5);
    // count_numbers(1, "123");
    malloc_test();
    return 0;
}