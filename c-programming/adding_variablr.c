# include<stdio.h>

int main() {
    int a;
    int b;
    printf("Enter two integers: ");
    scanf("%d %d", &a, &b);
    printf("The sum of %d and %d is: %d\n", a, b, a + b);
    return 0;
}