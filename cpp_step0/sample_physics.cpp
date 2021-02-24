#include "physics.h"
#include "renderer-sapp.h"

#include <cstdlib>
#include <cstdint>
#include <cstdio>
#include <random>

PhysicsSystem ps;

void update_physics(double dt, std::vector<math::Matrix4f> &object_tfs) {
    printf("dt = %f\n", dt*1000);
    ps.update(float(dt));
    // update object transforms
    object_tfs.resize(ps.objects.size());
    for (uint32_t i = 0; i < ps.objects.size(); i++) {
        const auto &obj = ps.objects[i];
        float heading = std::atan2(obj.vel.y, obj.vel.x);
        object_tfs[i] = {obj.radius*std::cos(heading), -obj.radius*std::sin(heading), 0, obj.pos.x,
                         obj.radius*std::sin(heading), obj.radius*std::cos(heading), 0, obj.pos.y,
                          0,0,1, 0,
                          0,0,0,1};
    }
}

template <typename T> T rand_range(T v1, T v2) {
    return v1 + T(double(rand()) / RAND_MAX * (v2 - v1));
}

int main(int argc, char *argv[]) {
    srand(12345678);
    auto obj1 = PhysicsObject(1.0, 1.0, {0, 0}, {3, 0});
    auto obj2 = PhysicsObject(2.0, 0.5, {10, 0.5}, {-2, 0});
    ps.add_object(obj1);
    ps.add_object(obj2);
    // add a bunch of randomly placed objects
    for (uint32_t i=0; i<1500; i++) {
        ps.add_object(PhysicsObject(rand_range(0.5f,2.0f), rand_range(0.5f,1.5f), 
                    math::Vector2f(rand_range(-100.0f, 100.0f), rand_range(-100.0f, 100.0f)), 
                    math::Vector2f(rand_range(-5.0f, 5.0f), rand_range(-5.0f, 5.0f)) ));
    }

    start_renderer(update_physics);
    return 0;
}
