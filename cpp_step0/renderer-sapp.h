#pragma once

// callback executed at every frame
typedef void (*frame_callback)(double dt);

void start_renderer(frame_callback callback=nullptr);
