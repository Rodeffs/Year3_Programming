// файл Global.cpp
////////////////////////////////////////
//Реализация глобальных функций
#include "stdafx.h"
#include "global.h"
#include <math.h>

CPoint Transform(const CPoint &point,
	       const CPoint &point0, double ang, int a, int b)
{
   CPoint res;
   	//Перевод в радианы
	ang=ang*atan(1.0)/45.0;
   res.x=(int)floor(point0.x+(point.x-point0.x)*cos(ang)-(point.y-point0.y)*sin(ang)+a+0.5);
   res.y=(int)floor(point0.y+(point.x-point0.x)*sin(ang)+(point.y-point0.y)*cos(ang)+b+0.5);
   return res;
};

double ZFunction(double x, double y)
{
	return (x*x+y*y)/10000;
};