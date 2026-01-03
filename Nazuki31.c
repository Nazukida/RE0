#include <stdio.h>

int main() {
    FILE *file = fopen("data.txt", "r");
    if (file == NULL) {
        printf("Error opening file.\n");
        return 1;
    }

    char name[50];
    int age;
    char city[50];

    while (fscanf(file, "%[^,],%d,%[^\n]", name, &age, city) == 3) {
        printf("Name: %s, Age: %d, City: %s\n", name, age, city);
    }

    fclose(file);
    return 0;
}