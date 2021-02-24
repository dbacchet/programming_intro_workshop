#include "physics.h"
#include "renderer-sapp.h"

#include <cstdlib>
#include <cstdint>
#include <cstdio>

PhysicsSystem ps;

void update_physics(double dt, std::vector<math::Matrix4f> &object_tfs) {
    ps.update(float(dt));
    // update object transforms
    object_tfs.resize(ps.objects.size());
    for (uint32_t i = 0; i < ps.objects.size(); i++) {
        const auto &obj = ps.objects[i];
        float heading = std::atan2(obj.vel.y, obj.vel.x);
        object_tfs[i] = {std::cos(heading), -std::sin(heading), 0, obj.pos.x,
                         std::sin(heading), std::cos(heading), 0, obj.pos.y,
                          0,0,1, 0,
                          0,0,0,1};
    }
}

int main(int argc, char *argv[]) {
    printf("pippo\n");
    auto obj1 = PhysicsObject(1.0, 1.0, {0, 0}, {3, 0});
    auto obj2 = PhysicsObject(2.0, 0.5, {10, 0.5}, {-2, 0});
    ps.add_object(obj1);
    ps.add_object(obj2);

    start_renderer(update_physics);
    return 0;
}
