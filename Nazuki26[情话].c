#include <stdio.h>
#include <time.h>

struct Date {
    int day;
    int month;
};

int isToday(struct Date date) {
    time_t now = time(NULL);
    struct tm *today = localtime(&now);

    return (date.day == today->tm_mday && date.month == today->tm_mon + 1);
}

int main() {
    time_t now = time(NULL);
    struct tm *today = localtime(&now);
    struct Date currentDate = {today->tm_mday, today->tm_mon + 1};

    struct Date specialDate = {19, 10};  

    printf("I like you not just for one day, one month, or one year. ");
    printf("My liking for you extends beyond time.\n");

    if (isToday(specialDate)) {
        printf("Today is a special day! It's the 19th of October.\n");
    } else {
        printf("Today is %d/%d.\n", currentDate.day, currentDate.month);
    }
    
    getchar();
    return 0;
}
