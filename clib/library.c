
void cube_vertices(float* buffer, int x, int y, int z, float n, int fill) {
    float qn = n / 8 * fill;

    float array[72] = {x - n, y + qn, z - n, x - n, y + qn, z + n, x + n, y + qn, z + n, x + n, y + qn, z - n,
        x - n, y - n, z - n, x + n, y - n, z - n, x + n, y - n, z + n, x - n, y - n, z + n,
        x - n, y - n, z - n, x - n, y - n, z + n, x - n, y + n, z + n, x - n, y + n, z - n,
        x + n, y - n, z + n, x + n, y - n, z - n, x + n, y + n, z - n, x + n, y + n, z + n,
        x - n, y - n, z + n, x + n, y - n, z + n, x + n, y + n, z + n, x - n, y + n, z + n,
        x + n, y - n, z - n, x - n, y - n, z - n, x - n, y + n, z - n, x + n, y + n, z - n}; // 12*6

    for (int i = 0; i < 72; ++i) {
        buffer[i] = array[i];
    }
}


void cube_vertices_x(float* buffer, int x, int y, int z, float n) {

    float array[72] = {x, y - n, z - n, x, y - n, z + n, x, y + n, z + n, x, y + n, z - n,
        x, y - n, z + n, x, y - n, z - n, x, y + n, z - n, x, y + n, z + n,
        x - n, y - n, z, x + n, y - n, z, x + n, y + n, z, x - n, y + n, z,
        x + n, y - n, z, x - n, y - n, z, x - n, y + n, z, x + n, y + n, z,
    };

    for (int i = 0; i < 72; ++i) {
        buffer[i] = array[i];
    }
}

void tex_coord(float* buffer, int x, int y, int n) {

    float m = 1.0 / n;
    float dx = x * m;
    float dy = y * m;w
    float array[8] = {dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m};

    for (int i = 0; i < 8; ++i) {
        buffer[i] = array[i];
    }

}