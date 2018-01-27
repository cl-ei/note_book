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
    return 0;
}

void malloc_test(){
    int ** d2;
    d2 = (int **)malloc(sizeof(int *)*2);
    cout << "d2: " << d2 << endl;

    int * temp;
    for (int i = 0; i < 2; i++){
        temp = (int*)malloc(sizeof(int)*2);
        cout << "i: " << i << ", temp: " << temp << endl;

        d2[i] = temp;
    }
    d2[1][1] = 9;

    cout << "addr d[0]: " << &d2[1] << endl
        << sizeof(int **) << endl;

    cout << d2[1][1] << " - " << &d2[1][1] << endl;

    // cpp11
    auto cpp_d2 = new int[2][3];
    cout << "typeof cpp_d2: " << typeid(cpp_d2).name() << endl;

    int (*cpp_d22)[3] = new int[2][3];
    cout << "typeof cpp_d22: " << typeid(cpp_d22).name() << endl;
}

int main() {
    // right_value_ref_arg(5);
    // count_numbers(1, "123");
    malloc_test();
    return 0;
}