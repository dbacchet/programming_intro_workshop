#pragma once

#include "vmath.h"

#include <vector>

struct PhysicsObject {
    float mass = 1.0f;
    float radius = 1.0f;
    math::Vector2f pos = {0, 0};
    math::Vector2f vel = {0, 0};
    math::Vector2f acc = {0, 0};

    PhysicsObject(float mass_ = 1.0f, float radius_ = 1.0f, const math::Vector2f &pos_ = math::Vector2f(),
                  const math::Vector2f &vel_ = math::Vector2f())
    : mass(mass_)
    , radius(radius_)
    , pos(pos_)
    , vel(vel_) {}
};

class PhysicsSystem {
public:
    void add_object(const PhysicsObject &po) {
        objects.push_back(po);
    }
    
    void update(float dt) {
        // reset ephemeral state
        for (auto &obj : objects) {
            obj.acc = math::Vector2f();
        }
        // collisions
        // here
        // integrate dynamics
        for (auto &obj : objects) {
            obj.vel += obj.acc * dt;
            if (math::length2(obj.vel)>25) {
                obj.vel = obj.vel * 0.9f;
            }
            obj.pos += obj.vel*dt;
            if (obj.pos.x>100) obj.pos.x = -100;
            if (obj.pos.y>100) obj.pos.y = -100;
            if (obj.pos.x<-100) obj.pos.x = 100;
            if (obj.pos.y<-100) obj.pos.y = 100;
        }
    }

    std::vector<PhysicsObject> objects;
};
