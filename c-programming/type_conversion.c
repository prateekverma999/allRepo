# include<stdio.h>

int main()
{
    float x,y,z;
    int i;

    int j = (int)1.99999999;
    printf("value of j: %d\n",j);


    printf("Enter three numbers: ");
    scanf("%f %f",&x,&y);
    i = z = x * y;
    printf("your value of z:%f now become value of i:%d\n",z,i);


    return 0;
}

