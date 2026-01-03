#include <stdio.h>
#include <string.h>
#include <math.h>

void donut(int paramA, int paramB) {
    float A1 = paramA, B1 = paramB, R1 = 1, R2 = 2, K2 = 5, K1 = A1 * 45 / (B1 + 2);
    int d[1760];
    float z[1760];
    char b[1760];
    float angleA = 0, angleB = 0;

    printf("\x1b[2J"); // Clear screen
    int width = 80; // Terminal width
    int height = 24; // Terminal height
    int centerX = width / 2; // Center of terminal width
    int centerY = height / 2; // Center of terminal height

    for (;;) {
        memset(b, 32, 1760);
        memset(d, 0, 1760 * sizeof(int));
        memset(z, 0, 1760 * sizeof(float));

        for (float j = 0; j < 6.28; j += 0.07) {
            for (float i = 0; i < 6.28; i += 0.02) {
                float sin_i = sin(i), cos_j = cos(j), sin_A = sin(angleA), sin_j = sin(j),
                      cos_A = cos(angleA), cos_j2 = cos_j + 2, mess = 1 / (sin_i * cos_j2 * sin_A + 
                      sin_j * cos_A + 5), cos_i = cos(i), cos_B = cos(angleB), sin_B = sin(angleB),
                      t = sin_i * cos_j2 * cos_A - sin_j * sin_A;

                // Adjust the center position based on terminal dimensions
                int x = centerX + (int)(30 * mess * (cos_i * cos_j2 * cos_B - t * sin_B));
                int y = centerY + (int)(15 * mess * (cos_i * cos_j2 * sin_B + t * cos_B));
                int o = x + width * y;
                int N = 8 * ((sin_j * sin_A - sin_i * cos_j * cos_A) * cos_B - sin_i * cos_j2 * sin_A - sin_j * cos_A - cos_i * cos_j * sin_B);

                if (y >= 0 && y < height && x >= 0 && x < width && mess > z[o]) {
                    z[o] = mess;
                    d[o] = ".,-~:;=!*#$@"[N > 0 ? N : 0];
                }
            }
        }

        printf("\x1b[H");
        for (int k = 0; k < 1760; k++)
            putchar(k % width ? d[k] : 10);

        angleA += 0.02; // Adjust rotation speed
        angleB += 0.01;
    }
}

int main() {
    donut(8, 20); // Adjust parameters A and B for different donut sizes
    return 0;
}
