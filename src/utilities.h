#include "pybind/include/pybind11/pybind11.h"
#include <iostream>

bool call_home(pybind11::object site,std::string user_name);
void print_dict(pybind11::dict dict);
bool equal_case_insensitive(const std::string& s1, const std::string& s2);
