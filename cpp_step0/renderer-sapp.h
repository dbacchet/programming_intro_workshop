#pragma once

#include "vmath_types.h"
#include <vector>

// callback executed at every frame
typedef void (*frame_callback)(double dt, std::vector<math::Matrix4f> &object_tfs);

void start_renderer(frame_callback callback=nullptr);
