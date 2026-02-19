// mandelbrot.cpp
#include <complex>
#include <cstdint>

extern "C" __declspec(dllexport)
int mandelbrot_iter(double a, double b, int max_iter)
{
    std::complex<double> c(a, b);
    std::complex<double> z(0, 0);

    int n = 0;
    while (std::abs(z) <= 2.0 && n < max_iter) {
        z = z*z + c;
        n++;
    }
    return n;
}
