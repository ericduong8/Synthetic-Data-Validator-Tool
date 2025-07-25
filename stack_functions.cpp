#include <iostream>
#include <stack>
using namespace std;

void iterSwapStacks(stack<int>& stack1, stack<int>& stack2) {
    int element;
    int stackSize = stack1.size();
    int i, j;
    
    for (j = 0; j < stackSize; j++) {
        element = stack1.top();
        stack1.pop();
        
        for (i = 0; i < j; i++) {
            stack1.push(stack2.top());
            stack2.pop();
        }
        
        stack2.push(element);
        
        for (i = 0; i < j; i++) {
            stack2.push(stack1.top());
            stack1.pop();
        }
    }
}

void recurSwapStacks(stack<int>& stack1, stack<int>& stack2) {
    if (stack1.empty()) {
        return;
    }
    
    int element = stack1.top();
    stack1.pop();
    
    recurSwapStacks(stack1, stack2);
    
    stack2.push(element);
}

void stlSwapStacks(stack<int>& stack1, stack<int>& stack2) {
    stack1.swap(stack2);
}

void moveStacks(stack<int>& stack1, stack<int>& stack2) {
    stack2 = stack1;
    while (!stack1.empty()) {
        stack1.pop();
    }
}
