#include "transforms.h"

#include "CGL/matrix3x3.h"
#include "CGL/vector2D.h"
#include "CGL/vector3D.h"

namespace CGL {

Vector2D operator*(const Matrix3x3 &m, const Vector2D &v) {
	Vector3D mv = m * Vector3D(v.x, v.y, 1);
	return Vector2D(mv.x / mv.z, mv.y / mv.z);
}

Matrix3x3 translate(float dx, float dy) {
	// Part 3: Fill this in.
	Matrix3x3 m;
	m[2][0] = dx;
	m[2][1] = dy;
	return m;
}

Matrix3x3 scale(float sx, float sy) {
	// Part 3: Fill this in.
	Matrix3x3 m;
	m[0][0] = sx;
	m[1][1] = sy;
	return m;
}

inline float degToRad(const float rad)
{
	return  rad * PI / 180.f;
}

// The input argument is in degrees counterclockwise
Matrix3x3 rotate(float deg) {
	// Part 3: Fill this in.
	Matrix3x3 m;
	m[0][0] = cos(degToRad(deg));
	m[0][1] = -sin(degToRad(deg));
	m[1][0] = sin(degToRad(deg));
	m[1][1] = cos(degToRad(deg));
	return m;
}

Matrix3x3 rotateViewport(float deg) {
	// Part 3: Fill this in.
	Matrix3x3 m;
	m[0][0] = cos(degToRad(deg));
	m[0][1] = -sin(degToRad(deg));
	m[1][0] = sin(degToRad(deg));
	m[1][1] = cos(degToRad(deg));
	return m;
}

}
