#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <filesystem>
#include <memory>
#include <string>
#include <vector>

#include "book.h"
#include "filemanager.h"
#include "library.h"

namespace py = pybind11;

PYBIND11_MODULE(bibliotheque_py, m) {
    m.doc() = "Module Python minimal pour charger et consulter la bibliothèque.";

    py::class_<Book>(m, "Book")
        .def_property_readonly("title", &Book::getTitle)
        .def_property_readonly("author", &Book::getAuthor)
        .def_property_readonly("isbn", &Book::getISBN)
        .def_property_readonly("available", &Book::getAvailability)
        .def_property_readonly("borrower_id", &Book::getBorrowerId)
        .def("to_string", &Book::toString)
        .def("__repr__", [](const Book& book) {
            return "<Book " + book.getISBN() + ">";
        });

    py::class_<Library, std::unique_ptr<Library>>(m, "Library")
        .def("all_books", [](Library& library) {
            std::vector<Book> books;
            for (Book* book : library.getAllBooks()) {
                books.push_back(*book);
            }
            return books;
        })
        .def_property_readonly("total_books", &Library::getTotalBooks)
        .def_property_readonly("available_count", &Library::getAvailableBookCount)
        .def_property_readonly("checked_out_count", &Library::getCheckedOutBookCount)
        .def_property_readonly("users_count", [](Library& library) {
            return library.getAllUsers().size();
        });

    m.def("load_library", [](const std::string& dataDir) {
        auto library = std::make_unique<Library>();
        const std::filesystem::path directory(dataDir);
        FileManager fileManager(
            (directory / "books.txt").string(),
            (directory / "users.txt").string());
        fileManager.loadLibraryData(*library);
        return library;
    }, py::arg("data_dir"), "Charge les livres et les utilisateurs depuis un répertoire de données.");
}
