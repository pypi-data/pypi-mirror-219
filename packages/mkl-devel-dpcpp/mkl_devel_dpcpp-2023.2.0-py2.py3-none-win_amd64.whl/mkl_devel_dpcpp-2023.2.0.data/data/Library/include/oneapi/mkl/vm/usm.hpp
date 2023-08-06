/* -== file: usm.hpp ==- */
/*******************************************************************************
* Copyright 2019-2023 Intel Corporation.
*
* This software and the related documents are Intel copyrighted  materials,  and
* your use of  them is  governed by the  express license  under which  they were
* provided to you (License).  Unless the License provides otherwise, you may not
* use, modify, copy, publish, distribute,  disclose or transmit this software or
* the related documents without Intel's prior written permission.
*
* This software and the related documents  are provided as  is,  with no express
* or implied  warranties,  other  than those  that are  expressly stated  in the
* License.
*******************************************************************************/

#ifndef ONEAPI_MKL_VM_USM_HPP
#define ONEAPI_MKL_VM_USM_HPP 1

#include <complex>
#include <cstdint>
#include <exception>

#include <sycl/sycl.hpp>

#include "oneapi/mkl/types.hpp"

#include "oneapi/mkl/vm/decls.hpp"

namespace oneapi {
namespace mkl {
namespace vm {

// abs:
// abs: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
abs(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
abs(sycl::queue& queue, std::int64_t n, const float* a, float* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
abs(sycl::queue& queue, std::int64_t n, const double* a, double* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
abs(sycl::queue& queue, std::int64_t n, const std::complex<float>* a, float* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
abs(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
    double* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// abs: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
abs(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
    sycl::half* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
abs(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
abs(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
abs(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
    float* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
abs(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
    double* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// acos:
// acos: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
acos(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acos(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acos(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acos(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
     std::complex<float>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acos(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
     std::complex<double>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// acos: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
acos(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acos(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acos(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acos(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
     std::complex<float>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acos(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
     std::complex<double>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// acosh:
// acosh: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
acosh(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acosh(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acosh(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acosh(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
      std::complex<float>* y, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acosh(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
      std::complex<double>* y, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// acosh: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
acosh(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acosh(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acosh(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acosh(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
      std::complex<float>* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acosh(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
      std::complex<double>* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// acospi:
// acospi: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
acospi(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acospi(sycl::queue& queue, std::int64_t n, const float* a, float* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acospi(sycl::queue& queue, std::int64_t n, const double* a, double* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// acospi: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
acospi(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
       sycl::half* y, oneapi::mkl::slice sy,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acospi(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
acospi(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// add:
// add: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
add(sycl::queue& queue, std::int64_t n, const sycl::half* a,
    const sycl::half* b, sycl::half* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
add(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
    float* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
add(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
    double* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
add(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
    const std::complex<float>* b, std::complex<float>* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
add(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
    const std::complex<double>* b, std::complex<double>* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// add: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
add(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
    const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
add(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, const float* b,
    oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
add(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, const double* b,
    oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
add(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
    const std::complex<float>* b, oneapi::mkl::slice sb, std::complex<float>* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
add(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
    const std::complex<double>* b, oneapi::mkl::slice sb,
    std::complex<double>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// arg:
// arg: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
arg(sycl::queue& queue, std::int64_t n, const std::complex<float>* a, float* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
arg(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
    double* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// arg: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
arg(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
    float* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
arg(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
    double* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// asin:
// asin: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
asin(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
asin(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
asin(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
asin(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
     std::complex<float>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
asin(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
     std::complex<double>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// asin: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
asin(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
asin(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
asin(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
asin(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
     std::complex<float>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
asin(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
     std::complex<double>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// asinh:
// asinh: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
asinh(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
asinh(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
asinh(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
asinh(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
      std::complex<float>* y, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
asinh(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
      std::complex<double>* y, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// asinh: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
asinh(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
asinh(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
asinh(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
asinh(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
      std::complex<float>* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
asinh(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
      std::complex<double>* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// asinpi:
// asinpi: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
asinpi(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
asinpi(sycl::queue& queue, std::int64_t n, const float* a, float* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
asinpi(sycl::queue& queue, std::int64_t n, const double* a, double* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// asinpi: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
asinpi(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
       sycl::half* y, oneapi::mkl::slice sy,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
asinpi(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
asinpi(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// atan:
// atan: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
atan(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
     std::complex<float>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
     std::complex<double>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// atan: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
atan(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
     std::complex<float>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
     std::complex<double>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// atan2:
// atan2: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
atan2(sycl::queue& queue, std::int64_t n, const sycl::half* a,
      const sycl::half* b, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan2(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
      float* y, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan2(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
      double* y, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// atan2: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
atan2(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan2(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, const float* b,
      oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan2(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
      const double* b, oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// atan2pi:
// atan2pi: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
atan2pi(sycl::queue& queue, std::int64_t n, const sycl::half* a,
        const sycl::half* b, sycl::half* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan2pi(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
        float* y, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan2pi(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
        double* y, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// atan2pi: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
atan2pi(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
        const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
        oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan2pi(sycl::queue& queue, const float* a, oneapi::mkl::slice sa,
        const float* b, oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atan2pi(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
        const double* b, oneapi::mkl::slice sb, double* y,
        oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// atanh:
// atanh: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
atanh(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
atanh(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
atanh(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
atanh(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
      std::complex<float>* y, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
atanh(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
      std::complex<double>* y, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// atanh: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
atanh(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
atanh(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
atanh(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
atanh(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
      std::complex<float>* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
atanh(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
      std::complex<double>* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// atanpi:
// atanpi: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
atanpi(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atanpi(sycl::queue& queue, std::int64_t n, const float* a, float* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atanpi(sycl::queue& queue, std::int64_t n, const double* a, double* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// atanpi: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
atanpi(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
       sycl::half* y, oneapi::mkl::slice sy,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atanpi(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
atanpi(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// cbrt:
// cbrt: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
cbrt(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
cbrt(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
cbrt(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// cbrt: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
cbrt(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
cbrt(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
cbrt(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// cdfnorm:
// cdfnorm: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
cdfnorm(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cdfnorm(sycl::queue& queue, std::int64_t n, const float* a, float* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cdfnorm(sycl::queue& queue, std::int64_t n, const double* a, double* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<double> const& eh = {});

// cdfnorm: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
cdfnorm(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
        sycl::half* y, oneapi::mkl::slice sy,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cdfnorm(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
        oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cdfnorm(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
        oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<double> const& eh = {});

// cdfnorminv:
// cdfnorminv: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
cdfnorminv(sycl::queue& queue, std::int64_t n, const sycl::half* a,
           sycl::half* y, std::vector<sycl::event> const& depends = {},
           oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
           oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cdfnorminv(sycl::queue& queue, std::int64_t n, const float* a, float* y,
           std::vector<sycl::event> const& depends = {},
           oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
           oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cdfnorminv(sycl::queue& queue, std::int64_t n, const double* a, double* y,
           std::vector<sycl::event> const& depends = {},
           oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
           oneapi::mkl::vm::error_handler<double> const& eh = {});

// cdfnorminv: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
cdfnorminv(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
           sycl::half* y, oneapi::mkl::slice sy,
           std::vector<sycl::event> const& depends = {},
           oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
           oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cdfnorminv(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
           oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
           oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
           oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cdfnorminv(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
           double* y, oneapi::mkl::slice sy,
           std::vector<sycl::event> const& depends = {},
           oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
           oneapi::mkl::vm::error_handler<double> const& eh = {});

// ceil:
// ceil: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
ceil(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
ceil(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
ceil(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// ceil: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
ceil(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
ceil(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
ceil(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// cis:
// cis: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
cis(sycl::queue& queue, std::int64_t n, const float* a, std::complex<float>* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cis(sycl::queue& queue, std::int64_t n, const double* a,
    std::complex<double>* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// cis: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
cis(sycl::queue& queue, const float* a, oneapi::mkl::slice sa,
    std::complex<float>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cis(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
    std::complex<double>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// conj:
// conj: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
conj(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
     std::complex<float>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
conj(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
     std::complex<double>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// conj: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
conj(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
     std::complex<float>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
conj(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
     std::complex<double>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// copysign:
// copysign: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
copysign(sycl::queue& queue, std::int64_t n, const sycl::half* a,
         const sycl::half* b, sycl::half* y,
         std::vector<sycl::event> const& depends = {},
         oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
copysign(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
         float* y, std::vector<sycl::event> const& depends = {},
         oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
copysign(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
         double* y, std::vector<sycl::event> const& depends = {},
         oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// copysign: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
copysign(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
         const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
         oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
         oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
copysign(sycl::queue& queue, const float* a, oneapi::mkl::slice sa,
         const float* b, oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
         std::vector<sycl::event> const& depends = {},
         oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
copysign(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
         const double* b, oneapi::mkl::slice sb, double* y,
         oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
         oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// cos:
// cos: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
cos(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cos(sycl::queue& queue, std::int64_t n, const float* a, float* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cos(sycl::queue& queue, std::int64_t n, const double* a, double* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cos(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
    std::complex<float>* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cos(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
    std::complex<double>* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// cos: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
cos(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
    sycl::half* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cos(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cos(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cos(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
    std::complex<float>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cos(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
    std::complex<double>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// cosd:
// cosd: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
cosd(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cosd(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cosd(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// cosd: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
cosd(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cosd(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cosd(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// cosh:
// cosh: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
cosh(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cosh(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cosh(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cosh(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
     std::complex<float>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cosh(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
     std::complex<double>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// cosh: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
cosh(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cosh(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cosh(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cosh(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
     std::complex<float>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cosh(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
     std::complex<double>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// cospi:
// cospi: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
cospi(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cospi(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cospi(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});

// cospi: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
cospi(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cospi(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
cospi(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});

// div:
// div: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
div(sycl::queue& queue, std::int64_t n, const sycl::half* a,
    const sycl::half* b, sycl::half* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
div(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
    float* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
div(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
    double* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
div(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
    const std::complex<float>* b, std::complex<float>* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
div(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
    const std::complex<double>* b, std::complex<double>* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// div: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
div(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
    const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
div(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, const float* b,
    oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
div(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, const double* b,
    oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
div(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
    const std::complex<float>* b, oneapi::mkl::slice sb, std::complex<float>* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
div(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
    const std::complex<double>* b, oneapi::mkl::slice sb,
    std::complex<double>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// erf:
// erf: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
erf(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
erf(sycl::queue& queue, std::int64_t n, const float* a, float* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
erf(sycl::queue& queue, std::int64_t n, const double* a, double* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// erf: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
erf(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
    sycl::half* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
erf(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
erf(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// erfc:
// erfc: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
erfc(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
erfc(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
erfc(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// erfc: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
erfc(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
erfc(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
erfc(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// erfcinv:
// erfcinv: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
erfcinv(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
erfcinv(sycl::queue& queue, std::int64_t n, const float* a, float* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
erfcinv(sycl::queue& queue, std::int64_t n, const double* a, double* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<double> const& eh = {});

// erfcinv: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
erfcinv(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
        sycl::half* y, oneapi::mkl::slice sy,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
erfcinv(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
        oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
erfcinv(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
        oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<double> const& eh = {});

// erfcx:
// erfcx: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
erfcx(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
erfcx(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
erfcx(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// erfcx: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
erfcx(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
erfcx(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
erfcx(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// erfinv:
// erfinv: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
erfinv(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
erfinv(sycl::queue& queue, std::int64_t n, const float* a, float* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
erfinv(sycl::queue& queue, std::int64_t n, const double* a, double* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// erfinv: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
erfinv(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
       sycl::half* y, oneapi::mkl::slice sy,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
erfinv(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
erfinv(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// exp:
// exp: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
exp(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp(sycl::queue& queue, std::int64_t n, const float* a, float* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp(sycl::queue& queue, std::int64_t n, const double* a, double* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
    std::complex<float>* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
    std::complex<double>* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// exp: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
exp(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
    sycl::half* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
    std::complex<float>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
    std::complex<double>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// exp10:
// exp10: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
exp10(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp10(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp10(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});

// exp10: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
exp10(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp10(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp10(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});

// exp2:
// exp2: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
exp2(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp2(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp2(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// exp2: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
exp2(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp2(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
exp2(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// expint1:
// expint1: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
expint1(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
expint1(sycl::queue& queue, std::int64_t n, const float* a, float* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
expint1(sycl::queue& queue, std::int64_t n, const double* a, double* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<double> const& eh = {});

// expint1: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
expint1(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
        sycl::half* y, oneapi::mkl::slice sy,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
expint1(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
        oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
expint1(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
        oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<double> const& eh = {});

// expm1:
// expm1: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
expm1(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
expm1(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
expm1(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});

// expm1: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
expm1(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
expm1(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
expm1(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});

// fdim:
// fdim: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
fdim(sycl::queue& queue, std::int64_t n, const sycl::half* a,
     const sycl::half* b, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
fdim(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
     float* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
fdim(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
     double* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// fdim: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
fdim(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
fdim(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, const float* b,
     oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
fdim(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
     const double* b, oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// floor:
// floor: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
floor(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
floor(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
floor(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// floor: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
floor(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
floor(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
floor(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// fmax:
// fmax: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
fmax(sycl::queue& queue, std::int64_t n, const sycl::half* a,
     const sycl::half* b, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
fmax(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
     float* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
fmax(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
     double* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// fmax: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
fmax(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
fmax(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, const float* b,
     oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
fmax(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
     const double* b, oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// fmin:
// fmin: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
fmin(sycl::queue& queue, std::int64_t n, const sycl::half* a,
     const sycl::half* b, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
fmin(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
     float* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
fmin(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
     double* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// fmin: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
fmin(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
fmin(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, const float* b,
     oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
fmin(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
     const double* b, oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// fmod:
// fmod: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
fmod(sycl::queue& queue, std::int64_t n, const sycl::half* a,
     const sycl::half* b, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
fmod(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
     float* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
fmod(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
     double* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// fmod: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
fmod(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
fmod(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, const float* b,
     oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
fmod(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
     const double* b, oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// frac:
// frac: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
frac(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
frac(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
frac(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// frac: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
frac(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
frac(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
frac(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// hypot:
// hypot: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
hypot(sycl::queue& queue, std::int64_t n, const sycl::half* a,
      const sycl::half* b, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
hypot(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
      float* y, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
hypot(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
      double* y, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// hypot: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
hypot(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
hypot(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, const float* b,
      oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
hypot(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
      const double* b, oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// inv:
// inv: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
inv(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
inv(sycl::queue& queue, std::int64_t n, const float* a, float* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
inv(sycl::queue& queue, std::int64_t n, const double* a, double* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});

// inv: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
inv(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
    sycl::half* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
inv(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
inv(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});

// invcbrt:
// invcbrt: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
invcbrt(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
invcbrt(sycl::queue& queue, std::int64_t n, const float* a, float* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
invcbrt(sycl::queue& queue, std::int64_t n, const double* a, double* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<double> const& eh = {});

// invcbrt: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
invcbrt(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
        sycl::half* y, oneapi::mkl::slice sy,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
invcbrt(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
        oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
invcbrt(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
        oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<double> const& eh = {});

// invsqrt:
// invsqrt: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
invsqrt(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
invsqrt(sycl::queue& queue, std::int64_t n, const float* a, float* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
invsqrt(sycl::queue& queue, std::int64_t n, const double* a, double* y,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<double> const& eh = {});

// invsqrt: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
invsqrt(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
        sycl::half* y, oneapi::mkl::slice sy,
        std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
invsqrt(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
        oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
invsqrt(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
        oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
        oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
        oneapi::mkl::vm::error_handler<double> const& eh = {});

// lgamma:
// lgamma: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
lgamma(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
lgamma(sycl::queue& queue, std::int64_t n, const float* a, float* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
lgamma(sycl::queue& queue, std::int64_t n, const double* a, double* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// lgamma: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
lgamma(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
       sycl::half* y, oneapi::mkl::slice sy,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
lgamma(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
lgamma(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// linearfrac:
// linearfrac: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
linearfrac(sycl::queue& queue, std::int64_t n, const sycl::half* a,
           const sycl::half* b, sycl::half c, sycl::half d, sycl::half e,
           sycl::half f, sycl::half* y,
           std::vector<sycl::event> const& depends = {},
           oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
           oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
linearfrac(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
           float c, float d, float e, float f, float* y,
           std::vector<sycl::event> const& depends = {},
           oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
           oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
linearfrac(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
           double c, double d, double e, double f, double* y,
           std::vector<sycl::event> const& depends = {},
           oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
           oneapi::mkl::vm::error_handler<double> const& eh = {});

// linearfrac: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
linearfrac(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
           const sycl::half* b, oneapi::mkl::slice sb, sycl::half c,
           sycl::half d, sycl::half e, sycl::half f, sycl::half* y,
           oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
           oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
           oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
linearfrac(sycl::queue& queue, const float* a, oneapi::mkl::slice sa,
           const float* b, oneapi::mkl::slice sb, float c, float d, float e,
           float f, float* y, oneapi::mkl::slice sy,
           std::vector<sycl::event> const& depends = {},
           oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
           oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
linearfrac(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
           const double* b, oneapi::mkl::slice sb, double c, double d, double e,
           double f, double* y, oneapi::mkl::slice sy,
           std::vector<sycl::event> const& depends = {},
           oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
           oneapi::mkl::vm::error_handler<double> const& eh = {});

// ln:
// ln: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
ln(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
   std::vector<sycl::event> const& depends = {},
   oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
   oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
ln(sycl::queue& queue, std::int64_t n, const float* a, float* y,
   std::vector<sycl::event> const& depends = {},
   oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
   oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
ln(sycl::queue& queue, std::int64_t n, const double* a, double* y,
   std::vector<sycl::event> const& depends = {},
   oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
   oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
ln(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
   std::complex<float>* y, std::vector<sycl::event> const& depends = {},
   oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
   oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
ln(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
   std::complex<double>* y, std::vector<sycl::event> const& depends = {},
   oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
   oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// ln: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
ln(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
   sycl::half* y, oneapi::mkl::slice sy,
   std::vector<sycl::event> const& depends = {},
   oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
   oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
ln(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
   oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
   oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
   oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
ln(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
   oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
   oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
   oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
ln(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
   std::complex<float>* y, oneapi::mkl::slice sy,
   std::vector<sycl::event> const& depends = {},
   oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
   oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
ln(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
   std::complex<double>* y, oneapi::mkl::slice sy,
   std::vector<sycl::event> const& depends = {},
   oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
   oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// log10:
// log10: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
log10(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log10(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log10(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log10(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
      std::complex<float>* y, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log10(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
      std::complex<double>* y, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// log10: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
log10(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log10(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log10(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log10(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
      std::complex<float>* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log10(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
      std::complex<double>* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// log1p:
// log1p: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
log1p(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log1p(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log1p(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});

// log1p: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
log1p(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log1p(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log1p(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});

// log2:
// log2: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
log2(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log2(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log2(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// log2: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
log2(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log2(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
log2(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// logb:
// logb: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
logb(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
logb(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
logb(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// logb: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
logb(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
logb(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
logb(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// maxmag:
// maxmag: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
maxmag(sycl::queue& queue, std::int64_t n, const sycl::half* a,
       const sycl::half* b, sycl::half* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
maxmag(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
       float* y, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
maxmag(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
       double* y, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// maxmag: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
maxmag(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
       const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
maxmag(sycl::queue& queue, const float* a, oneapi::mkl::slice sa,
       const float* b, oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
maxmag(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
       const double* b, oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// minmag:
// minmag: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
minmag(sycl::queue& queue, std::int64_t n, const sycl::half* a,
       const sycl::half* b, sycl::half* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
minmag(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
       float* y, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
minmag(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
       double* y, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// minmag: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
minmag(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
       const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
minmag(sycl::queue& queue, const float* a, oneapi::mkl::slice sa,
       const float* b, oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
minmag(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
       const double* b, oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// modf:
// modf: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
modf(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     sycl::half* z, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
modf(sycl::queue& queue, std::int64_t n, const float* a, float* y, float* z,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
modf(sycl::queue& queue, std::int64_t n, const double* a, double* y, double* z,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// modf: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
modf(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy, sycl::half* z, oneapi::mkl::slice sz,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
modf(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, float* z, oneapi::mkl::slice sz,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
modf(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, double* z, oneapi::mkl::slice sz,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// mul:
// mul: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
mul(sycl::queue& queue, std::int64_t n, const sycl::half* a,
    const sycl::half* b, sycl::half* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
mul(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
    float* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
mul(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
    double* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
mul(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
    const std::complex<float>* b, std::complex<float>* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
mul(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
    const std::complex<double>* b, std::complex<double>* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// mul: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
mul(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
    const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
mul(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, const float* b,
    oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
mul(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, const double* b,
    oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
mul(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
    const std::complex<float>* b, oneapi::mkl::slice sb, std::complex<float>* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
mul(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
    const std::complex<double>* b, oneapi::mkl::slice sb,
    std::complex<double>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// mulbyconj:
// mulbyconj: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
mulbyconj(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
          const std::complex<float>* b, std::complex<float>* y,
          std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
mulbyconj(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
          const std::complex<double>* b, std::complex<double>* y,
          std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// mulbyconj: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
mulbyconj(sycl::queue& queue, const std::complex<float>* a,
          oneapi::mkl::slice sa, const std::complex<float>* b,
          oneapi::mkl::slice sb, std::complex<float>* y, oneapi::mkl::slice sy,
          std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
mulbyconj(sycl::queue& queue, const std::complex<double>* a,
          oneapi::mkl::slice sa, const std::complex<double>* b,
          oneapi::mkl::slice sb, std::complex<double>* y, oneapi::mkl::slice sy,
          std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// nearbyint:
// nearbyint: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
nearbyint(sycl::queue& queue, std::int64_t n, const sycl::half* a,
          sycl::half* y, std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
nearbyint(sycl::queue& queue, std::int64_t n, const float* a, float* y,
          std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
nearbyint(sycl::queue& queue, std::int64_t n, const double* a, double* y,
          std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// nearbyint: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
nearbyint(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
          sycl::half* y, oneapi::mkl::slice sy,
          std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
nearbyint(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
          oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
nearbyint(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
          oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// nextafter:
// nextafter: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
nextafter(sycl::queue& queue, std::int64_t n, const sycl::half* a,
          const sycl::half* b, sycl::half* y,
          std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
nextafter(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
          float* y, std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
nextafter(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
          double* y, std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<double> const& eh = {});

// nextafter: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
nextafter(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
          const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
          oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
nextafter(sycl::queue& queue, const float* a, oneapi::mkl::slice sa,
          const float* b, oneapi::mkl::slice sb, float* y,
          oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
nextafter(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
          const double* b, oneapi::mkl::slice sb, double* y,
          oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<double> const& eh = {});

// pow:
// pow: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
pow(sycl::queue& queue, std::int64_t n, const sycl::half* a,
    const sycl::half* b, sycl::half* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
pow(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
    float* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
pow(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
    double* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
pow(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
    const std::complex<float>* b, std::complex<float>* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
pow(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
    const std::complex<double>* b, std::complex<double>* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// pow: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
pow(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
    const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
pow(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, const float* b,
    oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
pow(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, const double* b,
    oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
pow(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
    const std::complex<float>* b, oneapi::mkl::slice sb, std::complex<float>* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
pow(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
    const std::complex<double>* b, oneapi::mkl::slice sb,
    std::complex<double>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// pow2o3:
// pow2o3: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
pow2o3(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
pow2o3(sycl::queue& queue, std::int64_t n, const float* a, float* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
pow2o3(sycl::queue& queue, std::int64_t n, const double* a, double* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// pow2o3: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
pow2o3(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
       sycl::half* y, oneapi::mkl::slice sy,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
pow2o3(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
pow2o3(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// pow3o2:
// pow3o2: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
pow3o2(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
pow3o2(sycl::queue& queue, std::int64_t n, const float* a, float* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
pow3o2(sycl::queue& queue, std::int64_t n, const double* a, double* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// pow3o2: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
pow3o2(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
       sycl::half* y, oneapi::mkl::slice sy,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
pow3o2(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
pow3o2(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// powr:
// powr: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
powr(sycl::queue& queue, std::int64_t n, const sycl::half* a,
     const sycl::half* b, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
powr(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
     float* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
powr(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
     double* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// powr: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
powr(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
powr(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, const float* b,
     oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
powr(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
     const double* b, oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// powx:
// powx: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
powx(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half b,
     sycl::half* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
powx(sycl::queue& queue, std::int64_t n, const float* a, float b, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
powx(sycl::queue& queue, std::int64_t n, const double* a, double b, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
powx(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
     std::complex<float> b, std::complex<float>* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
powx(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
     std::complex<double> b, std::complex<double>* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// powx: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
powx(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half b, sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
powx(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float b,
     float* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
powx(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double b,
     double* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
powx(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
     std::complex<float> b, std::complex<float>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
powx(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
     std::complex<double> b, std::complex<double>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// remainder:
// remainder: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
remainder(sycl::queue& queue, std::int64_t n, const sycl::half* a,
          const sycl::half* b, sycl::half* y,
          std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
remainder(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
          float* y, std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
remainder(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
          double* y, std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<double> const& eh = {});

// remainder: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
remainder(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
          const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
          oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
remainder(sycl::queue& queue, const float* a, oneapi::mkl::slice sa,
          const float* b, oneapi::mkl::slice sb, float* y,
          oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
remainder(sycl::queue& queue, const double* a, oneapi::mkl::slice sa,
          const double* b, oneapi::mkl::slice sb, double* y,
          oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
          oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
          oneapi::mkl::vm::error_handler<double> const& eh = {});

// rint:
// rint: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
rint(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
rint(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
rint(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// rint: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
rint(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
rint(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
rint(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// round:
// round: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
round(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
round(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
round(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// round: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
round(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
round(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
round(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// sin:
// sin: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
sin(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sin(sycl::queue& queue, std::int64_t n, const float* a, float* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sin(sycl::queue& queue, std::int64_t n, const double* a, double* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sin(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
    std::complex<float>* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sin(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
    std::complex<double>* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// sin: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
sin(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
    sycl::half* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sin(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sin(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sin(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
    std::complex<float>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sin(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
    std::complex<double>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// sincos:
// sincos: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
sincos(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
       sycl::half* z, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sincos(sycl::queue& queue, std::int64_t n, const float* a, float* y, float* z,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sincos(sycl::queue& queue, std::int64_t n, const double* a, double* y,
       double* z, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// sincos: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
sincos(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
       sycl::half* y, oneapi::mkl::slice sy, sycl::half* z,
       oneapi::mkl::slice sz, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sincos(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
       oneapi::mkl::slice sy, float* z, oneapi::mkl::slice sz,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sincos(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
       oneapi::mkl::slice sy, double* z, oneapi::mkl::slice sz,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// sincospi:
// sincospi: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
sincospi(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
         sycl::half* z, std::vector<sycl::event> const& depends = {},
         oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
         oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sincospi(sycl::queue& queue, std::int64_t n, const float* a, float* y, float* z,
         std::vector<sycl::event> const& depends = {},
         oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
         oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sincospi(sycl::queue& queue, std::int64_t n, const double* a, double* y,
         double* z, std::vector<sycl::event> const& depends = {},
         oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
         oneapi::mkl::vm::error_handler<double> const& eh = {});

// sincospi: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
sincospi(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
         sycl::half* y, oneapi::mkl::slice sy, sycl::half* z,
         oneapi::mkl::slice sz, std::vector<sycl::event> const& depends = {},
         oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
         oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sincospi(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
         oneapi::mkl::slice sy, float* z, oneapi::mkl::slice sz,
         std::vector<sycl::event> const& depends = {},
         oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
         oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sincospi(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
         oneapi::mkl::slice sy, double* z, oneapi::mkl::slice sz,
         std::vector<sycl::event> const& depends = {},
         oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
         oneapi::mkl::vm::error_handler<double> const& eh = {});

// sind:
// sind: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
sind(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sind(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sind(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// sind: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
sind(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sind(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sind(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// sinh:
// sinh: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
sinh(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sinh(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sinh(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sinh(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
     std::complex<float>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sinh(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
     std::complex<double>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// sinh: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
sinh(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sinh(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sinh(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sinh(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
     std::complex<float>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sinh(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
     std::complex<double>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// sinpi:
// sinpi: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
sinpi(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sinpi(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sinpi(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});

// sinpi: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
sinpi(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sinpi(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sinpi(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});

// sqr:
// sqr: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
sqr(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
sqr(sycl::queue& queue, std::int64_t n, const float* a, float* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
sqr(sycl::queue& queue, std::int64_t n, const double* a, double* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// sqr: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
sqr(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
    sycl::half* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
sqr(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
sqr(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// sqrt:
// sqrt: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
sqrt(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sqrt(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sqrt(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sqrt(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
     std::complex<float>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sqrt(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
     std::complex<double>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// sqrt: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
sqrt(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sqrt(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sqrt(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sqrt(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
     std::complex<float>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sqrt(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
     std::complex<double>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// sub:
// sub: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
sub(sycl::queue& queue, std::int64_t n, const sycl::half* a,
    const sycl::half* b, sycl::half* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sub(sycl::queue& queue, std::int64_t n, const float* a, const float* b,
    float* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sub(sycl::queue& queue, std::int64_t n, const double* a, const double* b,
    double* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sub(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
    const std::complex<float>* b, std::complex<float>* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sub(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
    const std::complex<double>* b, std::complex<double>* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// sub: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
sub(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
    const sycl::half* b, oneapi::mkl::slice sb, sycl::half* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sub(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, const float* b,
    oneapi::mkl::slice sb, float* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sub(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, const double* b,
    oneapi::mkl::slice sb, double* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sub(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
    const std::complex<float>* b, oneapi::mkl::slice sb, std::complex<float>* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
sub(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
    const std::complex<double>* b, oneapi::mkl::slice sb,
    std::complex<double>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// tan:
// tan: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
tan(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tan(sycl::queue& queue, std::int64_t n, const float* a, float* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tan(sycl::queue& queue, std::int64_t n, const double* a, double* y,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tan(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
    std::complex<float>* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tan(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
    std::complex<double>* y, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// tan: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
tan(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
    sycl::half* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tan(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tan(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
    oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<double> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tan(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
    std::complex<float>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<float>> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tan(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
    std::complex<double>* y, oneapi::mkl::slice sy,
    std::vector<sycl::event> const& depends = {},
    oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
    oneapi::mkl::vm::error_handler<std::complex<double>> const& eh = {});

// tand:
// tand: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
tand(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tand(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tand(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// tand: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
tand(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tand(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tand(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
     oneapi::mkl::vm::error_handler<double> const& eh = {});

// tanh:
// tanh: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
tanh(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
tanh(sycl::queue& queue, std::int64_t n, const float* a, float* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
tanh(sycl::queue& queue, std::int64_t n, const double* a, double* y,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
tanh(sycl::queue& queue, std::int64_t n, const std::complex<float>* a,
     std::complex<float>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
tanh(sycl::queue& queue, std::int64_t n, const std::complex<double>* a,
     std::complex<double>* y, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// tanh: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
tanh(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
     sycl::half* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
tanh(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
tanh(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
     oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
tanh(sycl::queue& queue, const std::complex<float>* a, oneapi::mkl::slice sa,
     std::complex<float>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
tanh(sycl::queue& queue, const std::complex<double>* a, oneapi::mkl::slice sa,
     std::complex<double>* y, oneapi::mkl::slice sy,
     std::vector<sycl::event> const& depends = {},
     oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// tanpi:
// tanpi: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
tanpi(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tanpi(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tanpi(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});

// tanpi: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
tanpi(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tanpi(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tanpi(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
      oneapi::mkl::vm::error_handler<double> const& eh = {});

// tgamma:
// tgamma: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
tgamma(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tgamma(sycl::queue& queue, std::int64_t n, const float* a, float* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tgamma(sycl::queue& queue, std::int64_t n, const double* a, double* y,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// tgamma: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
tgamma(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
       sycl::half* y, oneapi::mkl::slice sy,
       std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<sycl::half> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tgamma(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<float> const& eh = {});
ONEAPI_MKL_VM_EXPORT sycl::event
tgamma(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
       oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
       oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined,
       oneapi::mkl::vm::error_handler<double> const& eh = {});

// trunc:
// trunc: indexing: linear
ONEAPI_MKL_VM_EXPORT sycl::event
trunc(sycl::queue& queue, std::int64_t n, const sycl::half* a, sycl::half* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
trunc(sycl::queue& queue, std::int64_t n, const float* a, float* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
trunc(sycl::queue& queue, std::int64_t n, const double* a, double* y,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

// trunc: indexing: strided
ONEAPI_MKL_VM_EXPORT sycl::event
trunc(sycl::queue& queue, const sycl::half* a, oneapi::mkl::slice sa,
      sycl::half* y, oneapi::mkl::slice sy,
      std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
trunc(sycl::queue& queue, const float* a, oneapi::mkl::slice sa, float* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);
ONEAPI_MKL_VM_EXPORT sycl::event
trunc(sycl::queue& queue, const double* a, oneapi::mkl::slice sa, double* y,
      oneapi::mkl::slice sy, std::vector<sycl::event> const& depends = {},
      oneapi::mkl::vm::mode mode = oneapi::mkl::vm::mode::not_defined);

} // namespace vm
} // namespace mkl
} // namespace oneapi
#endif // ifndef ONEAPI_MKL_VM_USM_HPP
