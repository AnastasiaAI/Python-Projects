#include "texture.h"
#include "CGL/color.h"

#include <cmath>
#include <algorithm>

namespace CGL {

Color Texture::sample(const SampleParams &sp) {
  // Parts 5 and 6: Fill this in.
  // Should return a color sampled based on the psm and lsm parameters given
	if (sp.lsm == LevelSampleMethod::L_ZERO)
	{
		return (sp.psm == PixelSampleMethod::P_NEAREST) ? sample_nearest(sp.p_uv, 0) : sample_bilinear(sp.p_uv, 0);
	}
	else if (sp.lsm == LevelSampleMethod::L_NEAREST)
	{
		float uLevel = 0.f;
		float vLevel = 0.f;
		get_level(sp, uLevel, vLevel);
		float mapmapLevel = max(uLevel, vLevel);
		int mipmap = (int)round(mapmapLevel);
		return (sp.psm == PixelSampleMethod::P_NEAREST) ? sample_nearest(sp.p_uv, mipmap) : sample_bilinear(sp.p_uv, mipmap);
	}
	else if (sp.lsm == LevelSampleMethod::L_LINEAR)
	{
		float uLevel = 0.f;
		float vLevel = 0.f;
		get_level(sp, uLevel, vLevel);
		float mapmapLevel = max(uLevel, vLevel);
		int mipmapl = floor(mapmapLevel);
		int mipmaph = ceil(mapmapLevel);
		float mk = mapmapLevel - (double)mipmapl;
		Color colorl = (sp.psm == PixelSampleMethod::P_NEAREST) ? sample_nearest(sp.p_uv, mipmapl) : sample_bilinear(sp.p_uv, mipmapl);
		Color colorh = (sp.psm == PixelSampleMethod::P_NEAREST) ? sample_nearest(sp.p_uv, mipmaph) : sample_bilinear(sp.p_uv, mipmaph);

		return mk * colorl + (1. - mk) * colorh;
	}

	else if (sp.lsm == LevelSampleMethod::L_ANISOTROPIC_NEAREST)
	{
		float uLevel = 0.f;
		float vLevel = 0.f;
		get_level(sp, uLevel, vLevel);
		int ripULevelRound = (int)round(uLevel);
		int ripVLevelRound = (int)round(vLevel);
		return (sp.psm == PixelSampleMethod::P_NEAREST) ? sample_nearest(sp.p_uv, ripULevelRound, ripVLevelRound, true) : sample_bilinear(sp.p_uv, ripULevelRound, ripVLevelRound, true);
	}
	else if (sp.lsm == LevelSampleMethod::L_ANISOTROPIC_LINEAR)
	{
		float uLevel = 0.f;
		float vLevel = 0.f;
		get_level(sp, uLevel, vLevel);
		int ripULevelL = (int)floor(uLevel);
		int ripULevelH = (int)ceil(uLevel);
		int ripVLevelL = (int)floor(vLevel);
		int ripVLevelH = (int)ceil(vLevel);
		float ruk = (double)uLevel - ripULevelL;
		float rvk = (double)vLevel - ripVLevelL;
		Color colorul = (sp.psm == PixelSampleMethod::P_NEAREST) ? sample_nearest(sp.p_uv, ripULevelL, ripVLevelL, true) : sample_bilinear(sp.p_uv, ripULevelL, ripVLevelL, true);
		Color colorvl = (sp.psm == PixelSampleMethod::P_NEAREST) ? sample_nearest(sp.p_uv, ripULevelL, ripVLevelL, true) : sample_bilinear(sp.p_uv, ripULevelL, ripVLevelL, true);
		Color coloruh = (sp.psm == PixelSampleMethod::P_NEAREST) ? sample_nearest(sp.p_uv, ripULevelH, ripVLevelH, true) : sample_bilinear(sp.p_uv, ripULevelH, ripVLevelH, true);
		Color colorvh = (sp.psm == PixelSampleMethod::P_NEAREST) ? sample_nearest(sp.p_uv, ripULevelH, ripVLevelH, true) : sample_bilinear(sp.p_uv, ripULevelH, ripVLevelH, true);

		return (ruk * colorul + (1. - ruk) * coloruh) * 0.5 + (rvk * colorvl + (1. - rvk) * colorvh) * 0.5;
	}

	return Color();
}

void Texture::get_level(const SampleParams &sp, float & out_uLevel, float & out_vLevel) {
  // Optional helper function for Parts 5 and 6

	Vector2D duvdx = sp.p_dx_uv - sp.p_uv;
	Vector2D duvdy = sp.p_dy_uv - sp.p_uv;

	const double dudx = duvdx.x;
	const double dvdx = duvdx.y;
	const double dudy = duvdy.x;
	const double dvdy = duvdy.y;

	double pw = width * sqrt(dudx * dudx + dudy * dudy); 
	double ph = height * sqrt(dudx * dudx + dudy * dudy);
	
	const float bias = 0.5;
	out_uLevel = log2(pw) + bias;
	out_vLevel = log2(ph) + bias;
}

// Returns the nearest sample given a particular level and set of uv coords
Color Texture::sample_nearest(Vector2D uv, int levelU, int levelV, bool isRipMap) {
  // Optional helper function for Parts 5 and 6
  // Feel free to ignore or create your own

	const RipLevel & rip = ripmap[levelU][(isRipMap) ? levelV  : levelU];
	const std::vector<unsigned char> & texels = rip.texels;

	const size_t w = rip.width;
	const size_t h = rip.height;

	const size_t nX = round((size_t)(((double)w) * uv.x));
	const size_t nY = round((size_t)(((double)h) * uv.y));

	const size_t n = (w * nY + nX) * 3;

	Color color;
	color.r = texels[n + 0] / 255.f;
	color.g = texels[n + 1] / 255.f;
	color.b = texels[n + 2] / 255.f;

  return color;
}

// Returns the bilinear sample given a particular level and set of uv coords
Color Texture::sample_bilinear(Vector2D uv, int levelU, int levelV, bool isRipMap) {
  // Optional helper function for Parts 5 and 6
  // Feel free to ignore or create your own

	const RipLevel & rip = ripmap[levelU][(isRipMap) ? levelV : levelU];

	const std::vector<unsigned char> & texels = rip.texels;

	const size_t w = rip.width;
	const size_t h = rip.height;

	double nXd = (double)w * uv.x;
	double nYd = (double)h * uv.y;

	const size_t nX0 = floor((size_t)(nXd));
	const size_t nY0 = floor((size_t)(nYd));

	const size_t nX1 = (nX0 < w - 1) ? nX0 + 1 : nX0;
	const size_t nY1 = (nY0 < h - 1) ? nY0 + 1 : nY0;

	const double kX = nXd - nX0;
	const double kY = nYd - nY0;


	Color colorXY0;
	Color colorXY1;
	Color color;

	const size_t n00 = (w * nY0 + nX0) * 3;
	const size_t n01 = (w * nY0 + nX1) * 3;
	const size_t n10 = (w * nY1 + nX0) * 3;
	const size_t n11 = (w * nY1 + nX1) * 3;
		
	colorXY0.r = kX * texels[n00 + 0] / 255.f + (1. - kX) * texels[n01 + 0] / 255.f;
	colorXY0.g = kX * texels[n00 + 1] / 255.f + (1. - kX) * texels[n01 + 1] / 255.f;
	colorXY0.b = kX * texels[n00 + 2] / 255.f + (1. - kX) * texels[n01 + 2] / 255.f;

	colorXY1.r = kX * texels[n10 + 0] / 255.f + (1. - kX) * texels[n11 + 0] / 255.f;
	colorXY1.g = kX * texels[n10 + 1] / 255.f + (1. - kX) * texels[n11 + 1] / 255.f;
	colorXY1.b = kX * texels[n10 + 2] / 255.f + (1. - kX) * texels[n11 + 2] / 255.f;

	color = (colorXY0 + colorXY1) * 0.5;

	return color;
}



/****************************************************************************/



inline void uint8_to_float(float dst[3], unsigned char *src) {
  uint8_t *src_uint8 = (uint8_t *)src;
  dst[0] = src_uint8[0] / 255.f;
  dst[1] = src_uint8[1] / 255.f;
  dst[2] = src_uint8[2] / 255.f;
}

inline void float_to_uint8(unsigned char *dst, float src[3]) {
  uint8_t *dst_uint8 = (uint8_t *)dst;
  dst_uint8[0] = (uint8_t)(255.f * max(0.0f, min(1.0f, src[0])));
  dst_uint8[1] = (uint8_t)(255.f * max(0.0f, min(1.0f, src[1])));
  dst_uint8[2] = (uint8_t)(255.f * max(0.0f, min(1.0f, src[2])));
}

void Texture::generate_mips(int startLevel) {

  // make sure there's a valid texture
  if (startLevel >= ripmap.size()) {
    std::cerr << "Invalid start level";
  }

  // allocate sublevels
  int baseWidth = ripmap[startLevel][startLevel].width;
  int baseHeight = ripmap[startLevel][startLevel].height;
  int numSubLevels = (int)(log2f((float)max(baseWidth, baseHeight)));

  numSubLevels = min(numSubLevels, kMaxMipLevels - startLevel - 1);
  ripmap.resize(startLevel + numSubLevels + 1);
  for (auto & rip : ripmap)
  {
	  rip.resize(startLevel + numSubLevels + 1);
  }

  int width = baseWidth;
  for (int i = 0; i <= numSubLevels; i++) {

	  int height = baseHeight;
	  for (int j = 0; j <= numSubLevels; j++) {

		  RipLevel &level = ripmap[startLevel + i][startLevel + j];
		  level.width = width;
		  level.height = height;

		  if (!(i == 0 && j == 0))
		  {
			  level.texels = vector<unsigned char>(3 * width * height);
		  }
		  
		  // handle odd size texture by rounding down
		  height = max(1, height / 2);
		  //assert (height > 0);
	  }


	  width = max(1, width / 2);
	  //assert (width > 0);
  }

  // create mips
  int subLevels = numSubLevels - (startLevel + 1);
  for (int ripLevelU = startLevel; ripLevelU < startLevel + subLevels + 1; ripLevelU++) {
	  for (int ripLevelV = startLevel; ripLevelV < startLevel + subLevels + 1; ripLevelV++) {

		  if (ripLevelU == startLevel && ripLevelV == startLevel)
		  {
			  continue;
		  }
		  
		  
		  RipLevel &prevLevel = (ripLevelV == startLevel) ? ripmap[ripLevelU - 1][ripLevelV] : ripmap[ripLevelU][ripLevelV - 1];
		  RipLevel &currLevel = ripmap[ripLevelU][ripLevelV];

		  int prevLevelPitch = prevLevel.width * 3; // 32 bit RGB
		  int currLevelPitch = currLevel.width * 3; // 32 bit RGB

		  unsigned char *prevLevelMem;
		  unsigned char *currLevelMem;

		  currLevelMem = (unsigned char *)&currLevel.texels[0];
		  prevLevelMem = (unsigned char *)&prevLevel.texels[0];

		  float wDecimal, wNorm, wWeight[3];
		  int wSupport;
		  float hDecimal, hNorm, hWeight[3];
		  int hSupport;

		  float result[3];
		  float input[3];

		  // conditional differentiates no rounding case from round down case
		  if (prevLevel.width & 1) {
			  wSupport = 3;
			  wDecimal = 1.0f / (float)currLevel.width;
		  }
		  else {
			  wSupport = 2;
			  wDecimal = 0.0f;
		  }

		  // conditional differentiates no rounding case from round down case
		  if (prevLevel.height & 1) {
			  hSupport = 3;
			  hDecimal = 1.0f / (float)currLevel.height;
		  }
		  else
		  {
			  hSupport = 2;
			  hDecimal = 0.0f;
		  }

		  wNorm = 1.0f / (2.0f + wDecimal);
		  hNorm = 1.0f / (2.0f + hDecimal);

		  // case 1: reduction only in horizontal size
		  if (currLevel.height == prevLevel.height) {
			  for (int j = 0; j < currLevel.height; j++) {
				  for (int i = 0; i < currLevel.width; i++) {
					  wWeight[0] = wNorm * (1.0f - wDecimal * i);
					  wWeight[1] = wNorm * 1.0f;
					  wWeight[2] = wNorm * wDecimal * (i + 1);

					  result[0] = result[1] = result[2] = 0.0f;


					  for (int k = 0; k < wSupport; k++) {
						  float weight =  wWeight[k];
						  uint8_to_float(input, prevLevelMem +
							  prevLevelPitch * (j)+
							  3 * (2 * i + k));
						  result[0] += weight * input[0];
						  result[1] += weight * input[1];
						  result[2] += weight * input[2];
					  }

					  // convert back to format of the texture
					  float_to_uint8(currLevelMem + currLevelPitch * j + 3 * i, result);
				  }
			  }
		  }
		  // case 2: reduction only in vertical size (horizontal size is 1)
		  else if (currLevel.width == prevLevel.width) {
			  for (int j = 0; j < currLevel.height; j++) {
				  hWeight[0] = hNorm * (1.0f - hDecimal * j);
				  hWeight[1] = hNorm;
				  hWeight[2] = hNorm * hDecimal * (j + 1);

				  for (int i = 0; i < currLevel.width; i++) {
					  result[0] = result[1] = result[2] = 0.0f;


					  for (int k = 0; k < hSupport; k++) {
							  float weight = hWeight[k];
							  uint8_to_float(input, prevLevelMem +
								  prevLevelPitch * (2 * j + k) +
								  3 * (i));
							  result[0] += weight * input[0];
							  result[1] += weight * input[1];
							  result[2] += weight * input[2];
						  }

					  // convert back to format of the texture
					  float_to_uint8(currLevelMem + currLevelPitch * j + 3 * i, result);
				  }
			  }

			 
		  }
		  // case 3: reduction in both horizontal and vertical size
		  else {

			  for (int j = 0; j < currLevel.height; j++) {
				  hWeight[0] = hNorm * (1.0f - hDecimal * j);
				  hWeight[1] = hNorm;
				  hWeight[2] = hNorm * hDecimal * (j + 1);

				  for (int i = 0; i < currLevel.width; i++) {
					  wWeight[0] = wNorm * (1.0f - wDecimal * i);
					  wWeight[1] = wNorm * 1.0f;
					  wWeight[2] = wNorm * wDecimal * (i + 1);

					  result[0] = result[1] = result[2] = 0.0f;

					  // convolve source image with a trapezoidal filter.
					  // in the case of no rounding this is just a box filter of width 2.
					  // in the general case, the support region is 3x3.
					  for (int jj = 0; jj < hSupport; jj++)
						  for (int ii = 0; ii < wSupport; ii++) {
							  float weight = hWeight[jj] * wWeight[ii];
							  uint8_to_float(input, prevLevelMem +
								  prevLevelPitch * (2 * j + jj) +
								  3 * (2 * i + ii));
							  result[0] += weight * input[0];
							  result[1] += weight * input[1];
							  result[2] += weight * input[2];
						  }

					  // convert back to format of the texture
					  float_to_uint8(currLevelMem + currLevelPitch * j + 3 * i, result);
				  }
			  }
		  }
	  }
  }
}

}
