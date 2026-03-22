#include <stdio.h>
#include <string.h>

int main() {
    char naam[8];
    int admin = 0;

    printf("Voer je naam in: ");
    gets(naam);   // expres onveilig voor demo

    printf("Hallo %s\n", naam);

    if (admin == 1) {
        printf("Adminrechten verkregen!\n");
    } else {
        printf("Normale gebruiker.\n");
    }

    return 0;
}