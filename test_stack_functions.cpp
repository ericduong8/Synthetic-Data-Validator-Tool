#include <iostream>
#include <stack>
#include <vector>
#include <cassert>
using namespace std;

void iterSwapStacks(stack<int>& stack1, stack<int>& stack2);
void recurSwapStacks(stack<int>& stack1, stack<int>& stack2);
void stlSwapStacks(stack<int>& stack1, stack<int>& stack2);
void moveStacks(stack<int>& stack1, stack<int>& stack2);

void printStack(stack<int> s, const string& name) {
    cout << name << " (top to bottom): ";
    if (s.empty()) {
        cout << "(empty)";
    } else {
        while (!s.empty()) {
            cout << s.top() << " ";
            s.pop();
        }
    }
    cout << endl;
}

stack<int> createTestStack() {
    stack<int> s;
    s.push(5);
    s.push(4);
    s.push(3);
    s.push(2);
    s.push(1);
    return s;
}

bool verifyStack(stack<int> s, const vector<int>& expected) {
    if (s.size() != expected.size()) return false;
    
    for (int i = 0; i < expected.size(); i++) {
        if (s.empty() || s.top() != expected[i]) return false;
        s.pop();
    }
    return true;
}

void testIterSwapStacks() {
    cout << "\n=== Testing iterSwapStacks ===" << endl;
    stack<int> stack1 = createTestStack();
    stack<int> stack2;
    
    cout << "Before:" << endl;
    printStack(stack1, "Stack1");
    printStack(stack2, "Stack2");
    
    iterSwapStacks(stack1, stack2);
    
    cout << "After:" << endl;
    printStack(stack1, "Stack1");
    printStack(stack2, "Stack2");
    
    assert(stack1.empty());
    assert(verifyStack(stack2, {1, 2, 3, 4, 5}));
    cout << "✓ iterSwapStacks test passed!" << endl;
}

void testRecurSwapStacks() {
    cout << "\n=== Testing recurSwapStacks ===" << endl;
    stack<int> stack1 = createTestStack();
    stack<int> stack2;
    
    cout << "Before:" << endl;
    printStack(stack1, "Stack1");
    printStack(stack2, "Stack2");
    
    recurSwapStacks(stack1, stack2);
    
    cout << "After:" << endl;
    printStack(stack1, "Stack1");
    printStack(stack2, "Stack2");
    
    assert(stack1.empty());
    assert(verifyStack(stack2, {1, 2, 3, 4, 5}));
    cout << "✓ recurSwapStacks test passed!" << endl;
}

void testStlSwapStacks() {
    cout << "\n=== Testing stlSwapStacks ===" << endl;
    stack<int> stack1 = createTestStack();
    stack<int> stack2;
    
    cout << "Before:" << endl;
    printStack(stack1, "Stack1");
    printStack(stack2, "Stack2");
    
    stlSwapStacks(stack1, stack2);
    
    cout << "After:" << endl;
    printStack(stack1, "Stack1");
    printStack(stack2, "Stack2");
    
    assert(stack1.empty());
    assert(verifyStack(stack2, {1, 2, 3, 4, 5}));
    cout << "✓ stlSwapStacks test passed!" << endl;
}

void testMoveStacks() {
    cout << "\n=== Testing moveStacks ===" << endl;
    stack<int> stack1 = createTestStack();
    stack<int> stack2;
    
    cout << "Before:" << endl;
    printStack(stack1, "Stack1");
    printStack(stack2, "Stack2");
    
    moveStacks(stack1, stack2);
    
    cout << "After:" << endl;
    printStack(stack1, "Stack1");
    printStack(stack2, "Stack2");
    
    assert(stack1.empty());
    assert(verifyStack(stack2, {1, 2, 3, 4, 5}));
    cout << "✓ moveStacks test passed!" << endl;
}

int main() {
    cout << "Testing Stack Transfer Functions" << endl;
    cout << "Expected behavior: Transfer 1 2 3 4 5 (top to bottom) from Stack1 to Stack2" << endl;
    
    testIterSwapStacks();
    testRecurSwapStacks();
    testStlSwapStacks();
    testMoveStacks();
    
    cout << "\n🎉 All tests passed!" << endl;
    return 0;
}
