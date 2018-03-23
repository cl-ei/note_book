#include <string.h>

/*
 * stack
 *
 */

typedef struct StackNode{
    struct Stack *pNext;
    int nData;
} StackNode;

void push_stack(int data, StackNode** pHead){
    StackNode* Node = (StackNode*)malloc(sizeof(StackNode));
    Node->nData = data;
    Node->pNext = NULL;

    if (*pHead == NULL){
        *pHead = Node;
    }else{
        Node->pNext = *pHead;
        *pHead = Node;
    }
}

int pop_stack(int *data, StackNode** pHead){
    if (pHead==NULL || *pHead == NULL) return -1;

    *data = (*pHead)->nData;
    StackNode* temp = *pHead;
    *pHead = (*pHead)->pNext;

    free(temp);
    return 0;
}

void print_stack(StackNode *pHead){
    while(1){
        printf("%d, ", pHead->nData);
        if(!pHead->pNext) break;

        pHead = pHead->pNext;
    }
    printf("\n");
}

void stack_main(){
    printf("run stack test.\n");

    StackNode* stack = NULL;

    push_stack(1, &stack);
    push_stack(2, &stack);
    push_stack(4, &stack);


    print_stack(stack);

    int a = 0;
    pop_stack(&a, &stack);
    print_stack(stack);

}

/*
 * list
 *
 */

typedef struct ListNode{
    int nData;
    struct ListNode *pNext;
} ListNode;


ListNode* merge_list(ListNode *pHead1, ListNode* pHead2){
    if (pHead1 == NULL){
        return pHead2;
    }
    if (pHead2 == NULL){
        return pHead1;
    }

    ListNode *pHead = pHead1->nData <= pHead2->nData ? pHead1 : pHead2;
    ListNode *pTemp;

    while(pHead1 != NULL && pHead2 != NULL){
        if(pHead1->nData <= pHead2->nData){
            pTemp = pHead1->pNext;
            pHead1->pNext = pHead2;
            pHead1 = pTemp;
        }else{
            pTemp = pHead2->pNext;
            pHead2->pNext = pHead1;
            pHead2 = pTemp;
        }
    }

    return pHead;
}

void print_list(ListNode *pHead){
    while(pHead != NULL){
        printf("%d, ", pHead->nData);
        pHead = pHead->pNext;
    }
    printf("\n----\n");
}

void list_test(){
    ListNode *pHead1 = (ListNode*)malloc(sizeof(ListNode));
    pHead1->nData = 1;

    pHead1->pNext = (ListNode*)malloc(sizeof(ListNode));
    pHead1->pNext->nData = 3;

    pHead1->pNext->pNext = (ListNode*)malloc(sizeof(ListNode));
    pHead1->pNext->pNext->nData = 5;
    pHead1->pNext->pNext->pNext = NULL;


    ListNode *pHead2 = (ListNode*)malloc(sizeof(ListNode));
    pHead2->nData = 2;

    pHead2->pNext = (ListNode*)malloc(sizeof(ListNode));
    pHead2->pNext->nData = 4;
    pHead2->pNext->pNext = NULL;

    print_list(pHead1);
    print_list(pHead2);
    print_list(merge_list(pHead1, pHead2));
}

/*
 * bin tree
 *
 */

typedef struct BinTreeNode{
    struct BinTreeNode *pLeft;
    struct BinTreeNode *pRight;
    int nData;
} BinTreeNode;

BinTreeNode* create_tree_node(int data){
    BinTreeNode* pHead = (BinTreeNode*)malloc(sizeof(BinTreeNode));
    if (pHead == NULL) return NULL;

    pHead->nData = data;
    pHead->pLeft = NULL;
    pHead->pRight = NULL;
    return pHead;
}

BinTreeNode* create_test_data(){
    BinTreeNode *pHead = create_tree_node(1);

    pHead->pLeft = create_tree_node(2);
    pHead->pRight = create_tree_node(3);

    pHead->pLeft->pLeft = create_tree_node(4);
    pHead->pLeft->pRight = create_tree_node(5);

    pHead->pRight->pLeft = create_tree_node(6);
    pHead->pRight->pRight = create_tree_node(7);

    return pHead;
}

void pre_order_print(BinTreeNode* pHead){
    if(pHead != NULL){
        printf("%d", pHead->nData);
        pre_order_print(pHead->pLeft);
        pre_order_print(pHead->pRight);
    }
}

void in_order_print(BinTreeNode* pHead){
    if(pHead != NULL){
        in_order_print(pHead->pLeft);
        printf("%d", pHead->nData);
        in_order_print(pHead->pRight);
    }
}

void post_order_print(BinTreeNode* pHead){
    if(pHead != NULL){
        post_order_print(pHead->pLeft);
        post_order_print(pHead->pRight);
        printf("%d", pHead->nData);
    }
}

void bintree_test() {
    BinTreeNode* pHead = create_test_data();
    pre_order_print(pHead);
    printf("\n");

    in_order_print(pHead);
    printf("\n");

    post_order_print(pHead);
    printf("\n");
}
