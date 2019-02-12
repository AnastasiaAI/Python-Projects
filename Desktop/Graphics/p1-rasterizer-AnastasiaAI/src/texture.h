#ifndef CGL_TEXTURE_H
#define CGL_TEXTURE_H

#include <vector>
#include "CGL/CGL.h"
#include "CGL/color.h"
#include "CGL/vector2D.h"

#include <iostream>
using namespace std;

namespace CGL {

typedef enum PixelSampleMethod { P_NEAREST = 0, P_LINEAR = 1 } PixelSampleMethod;
typedef enum LevelSampleMethod { L_ZERO = 0, L_NEAREST = 1, L_LINEAR = 2, L_ANISOTROPIC_NEAREST = 3, L_ANISOTROPIC_LINEAR = 4} LevelSampleMethod;

struct SampleParams {
  Vector2D p_uv;
  Vector2D p_dx_uv, p_dy_uv;
  PixelSampleMethod psm;
  LevelSampleMethod lsm;
};

static const int kMaxMipLevels = 14;

struct RipLevel {
	size_t width;
	size_t height;
  // RGB color values
  std::vector<unsigned char> texels;

  Color get_texel(int tx, int ty);
};

struct Texture {
  size_t width;
  size_t height;
  std::vector<std::vector<RipLevel>> ripmap;

  void init(const vector<unsigned char>& pixels, const size_t& w, const size_t& h) {
    width = w; height = h;

    // A fancy C++11 feature. emplace_back constructs the element in place,
    // and in this case it uses the new {} list constructor syntax.
	ripmap.emplace_back(std::vector<RipLevel>(1,RipLevel{width, height, pixels}));

    generate_mips();
  }

  // Generates up to kMaxMipLevels of mip maps. Level 0 contains
  // the unfiltered original pixels.
  void generate_mips(int startLevel = 0);

  Color sample(const SampleParams &sp);
  void get_level(const SampleParams &sp, float & out_uLevel, float & out_vLevel);

  Color sample_nearest(Vector2D uv, int levelU = 0, int levelV = 0, bool isRipMap = false);

  Color sample_bilinear(Vector2D uv, int levelU = 0, int levelV = 0, bool isRipMap = false);
};

}

#endif // CGL_TEXTURE_H
