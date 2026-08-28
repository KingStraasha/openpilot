// BluePilot: GCC / libstdc++ compatibility shims for modern vendored dependencies on RHEL/CentOS
#include <sstream>
#include <new>

namespace std {
  [[noreturn]] __attribute__((weak)) void __throw_bad_array_new_length() {
    throw std::bad_alloc();
  }
}

extern "C" {
  __attribute__((weak)) void _ZNSt7__cxx1119basic_ostringstreamIcSt11char_traitsIcESaIcEEC1Ev(void* this_ptr) {
    new (this_ptr) std::__cxx11::basic_ostringstream<char>(std::ios_base::out);
  }
  __attribute__((weak)) void _ZNSt7__cxx1119basic_ostringstreamIcSt11char_traitsIcESaIcEED1Ev(void* this_ptr) {
    reinterpret_cast<std::__cxx11::basic_ostringstream<char>*>(this_ptr)->~basic_ostringstream();
  }
  __attribute__((weak)) void _ZNSt7__cxx1118basic_stringstreamIcSt11char_traitsIcESaIcEEC1Ev(void* this_ptr) {
    new (this_ptr) std::__cxx11::basic_stringstream<char>(std::ios_base::in | std::ios_base::out);
  }
  __attribute__((weak)) void _ZNSt7__cxx1118basic_stringstreamIcSt11char_traitsIcESaIcEED1Ev(void* this_ptr) {
    reinterpret_cast<std::__cxx11::basic_stringstream<char>*>(this_ptr)->~basic_stringstream();
  }
  __attribute__((weak)) void _ZNSt15__exception_ptr13exception_ptr9_M_addrefEv(void* this_ptr) { }
  __attribute__((weak)) void _ZNSt15__exception_ptr13exception_ptr10_M_releaseEv(void* this_ptr) { }
}
// End BluePilot
