cmake_minimum_required(VERSION 2.8.12)
project(music_infobox)

add_subdirectory(pybind11)
pybind11_add_module(music_infobox src/example.cpp src/example.h src/example.cpp src/utilities.h src/utilities.cpp)
