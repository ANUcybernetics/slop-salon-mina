/* DLA — diffusion-limited aggregation, the stationary glider
 * Walkers spawn from a large circle and diffuse inward.
 * As they approach the cluster, they stick on first contact.
 * Adaptive: spawn closer as cluster grows to keep efficiency.
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>

#define SIZE 513
#define C (SIZE/2)
#define TARGET 15000
#define MAX(a,b) ((a)>(b)?(a):(b))
#define MIN(a,b) ((a)<(b)?(a):(b))

static char cluster[SIZE][SIZE];
static char dr[8] = {-1,-1,-1,0,0,1,1,1};
static char dc[8] = {-1,0,1,-1,1,-1,0,1};

static int hit_cluster(int r, int c) {
    for (int d = 0; d < 8; d++) {
        int nr = r + dr[d], nc = c + dc[d];
        if (nr >= 0 && nr < SIZE && nc >= 0 && nc < SIZE && cluster[nr][nc])
            return 1;
    }
    return 0;
}

int main() {
    srand(42);
    memset(cluster, 0, sizeof(cluster));
    cluster[C][C] = 1;

    int sticky = 0;
    int spawn_r = 200;  // adaptive spawn radius
    clock_t t0 = clock();

    for (int i = 0; i < TARGET; i++) {
        double theta = ((double)rand()/RAND_MAX) * 2.0 * M_PI;
        int r = C + (int)(spawn_r * cos(theta));
        int c = C + (int)(spawn_r * sin(theta));

        for (int w = 0; w < 100000; w++) {
            if (r < 0 || r >= SIZE || c < 0 || c >= SIZE) break;

            if (hit_cluster(r, c)) {
                cluster[r][c] = 1;
                sticky++;
                goto next;
            }

            int d = rand() % 8;
            r += dr[d];
            c += dc[d];
        }

    next:;
        // Shrink spawn radius as cluster grows
        spawn_r = MAX(5, (int)(sqrt(sticky + 1) * 1.8));

        if (i % 2000 == 0) {
            double t = (clock()-t0)/(double)CLOCKS_PER_SEC;
            printf("step %d/%d, sticky: %d, spawn_r: %d, %.1fs\n",
                   i, TARGET, sticky, spawn_r, t);
        }
    }

    printf("Total: %d, time: %.1fs\n",
           sticky+1, (clock()-t0)/(double)CLOCKS_PER_SEC);
    return 0;
}
