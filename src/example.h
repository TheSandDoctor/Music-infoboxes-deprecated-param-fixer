/**
 Copyright (C) 2018 Kyle Wilson <majorjohn1@mail.com>
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights to
 use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
 of the Software, and to permit persons to whom the Software is furnished to do
 so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
 */
#include <pybind11/pybind11.h>
#include <pybind11/embed.h>
#include "utilities.h"

#include <iostream>
#include <string>
#include <string.h>
#include <stdio.h>
#include <sys/types.h>

#define CAT_MODULE_STRING_ERRORS "[[Category:Music infoboxes with Module:String errors{{!}}"
#define BOT_USER "DeprecatedFixerBot"

/**
 * See example.cpp for comments.
 */

namespace py = pybind11;
using namespace std;
#include <sys/stat.h>
namespace Helpers {
    py::str get_valid_filename(string s) {
        py::object re = py::module::import("re");
        py::object s1 = py::str(s).attr("strip")().attr("replace")(' ','_');
        return re.attr("sub")("r'(?u)[^-\w.]'","",py::str(s1));
    }
    /**
     * @brief Reverses a python list
     * @param list List to revert
     * @return void
     */
    const void reverseList(py::list list) {
        list.attr("reverse")();
    }
    const void makeDir(const char* directory) {
        int dir_err = mkdir(directory, S_IRWXU | S_IRWXG | S_IROTH | S_IXOTH);
        if (-1 == dir_err)
        {
            printf("Error creating directory!n");
            //exit(1);
        }
    }
    const void createWriteFile(const char* file_name, const char *contents) {
        FILE * pFile;
        pFile = fopen(file_name, "w"); // write-only
        fwrite(contents,sizeof(char),sizeof(contents),pFile);
        fclose(pFile);
       // free(pFile);
    }
    //TODO: Needs fixing
    const void createWriteFile2(string file_name) {
        py::object pathlib = py::module::import("pathlib");
        if(pathlib.attr("Path")("./errors").attr("is_dir")() == Py_False)
            pathlib.attr("Path")("./errors").attr("mkdir")();    // create dir
        py::print("FF");
        py::str title = get_valid_filename(file_name);
        py::print(title);
      //  py::exec(R"");
      //  py::object ob;
        //py::object text_file = ob.attr("open")("./errors/err " + string(title) + ".txt",'w');
        
    }
};

bool pageInList(std::string page_name,py::list list);
string template_figure_type(string temp);
py::str process(string text);
bool bContent_changed = false;
bool getContentChanged();

bool revert(string page_name,py::object site);
//py::list gen_cat_to_avoid(py::object site);
