/**
 * @file
 * Helper macros for logging.
 *
 * This file defines some useful macros for logging.
 *
 * @author Thilo Schmitt
 */

#ifndef tas_log_hpp
#define tas_log_hpp

#include <iomanip>
#include <armadillo>

/*!
 * @brief Remove the path part of a file name.
 *
 * @param s File name with path
 * @return File name without path
 */
std::string removePath(std::string s)
{
    size_t found;
    found = s.find_last_of("/\\");
    return s.substr(found+1);
}

/*!
 * @brief Gives the dimension of an armadillo matrix object.
 *
 * @param m Armadillo matrix.
 */
std::string size_of_show( arma::mat m ) {
    std::ostringstream out;
    out << " [" << m.n_rows << "x" << m.n_cols << "]";
    return out.str();
}

/*!
 * @brief Gives the dimension of an armadillo matrix object.
 *
 * @param m Armadillo matrix.
 */
std::string size_of_show( arma::umat m ) {
    std::ostringstream out;
    out << " [" << m.n_rows << "x" << m.n_cols << "]";
    return out.str();
}

/*!
 * @brief Gives the dimension of an armadillo matrix object.
 *
 * @param m Armadillo matrix.
 */
std::string size_of_show( arma::fmat m ) {
    std::ostringstream out;
    out << " [" << m.n_rows << "x" << m.n_cols << "]";
    return out.str();
}

/*!
 * @brief Gives the dimension of an armadillo matrix object.
 *
 * @param m Armadillo matrix.
 */
std::string size_of_show( arma::imat m ) {
    std::ostringstream out;
    out << " [" << m.n_rows << "x" << m.n_cols << "]";
    return out.str();
}

/*!
 * @brief Returns empty string for a double/float value.
 *
 * @param f A double/float value.
 */
std::string size_of_show( double f ) {
    return "";
}

/*!
 * @brief Gives the length of a string.
 *
 * @param s A string.
 */
std::string size_of_show( std::string s ) {
    std::ostringstream out;
    out << " [" << s.length() << "]";
    return out.str();
}

/*!
 * @brief Print error message and exit the program.
 *
 * @param s Stream containing the error message.
 */
#define TASERR(s) std::cerr << "(ERR): " << std::setw(18) << removePath(__FILE__) << ":" << std::setw(4) << __LINE__ << " " << s << std::endl; exit(-1);

/*!
 * @brief Print a warning message.
 *
 * @param s Stream containing the error message.
 */
#define TASWRN(s) std::cerr << "(WRN): " << std::setw(18) << removePath(__FILE__) << ":" << std::setw(4) << __LINE__ << " " << s << std::endl;

/*!
 * @brief Print an info message.
 *
 * @param s Stream containing the error message.
 */
#define INFO(s) std::cerr << "(INF): " << std::setw(18) << removePath(__FILE__) << ":" << std::setw(4) << __LINE__ << " " << s << std::endl;

/*!
 * @brief Helper macro to print armadillo objects
 *
 * Shows the dimension of the objects.
 *
 * @warning SHOW will only print messages if DEB_SHOW macro is defined. To always print a message use SHOW2.
 *
 * @param s Stream containing a description of the object.
 * @param v Armadillo object.
 */
#ifdef DEB_SHOW
#define SHOW(s, v) std::cout << "SHOWING: " << s << size_of_show(v) << " from file " << removePath(__FILE__) << ":"<< __LINE__ << std::endl; std::cout << v << std::endl;
#endif

#ifndef DEB_SHOW
    #define SHOW(s, v)
#endif

/*!
 * @brief Helper macro to print armadillo objects
 *
 * Shows the dimension of the objects.
 *
 * @param s Stream containing a description of the object.
 * @param v Armadillo object.
 */
#define SHOW2(s, v) std::cout << "SHOWING: " << s << size_of_show(v) << " from file " << removePath(__FILE__) << ":"<< __LINE__ << std::endl; std::cout << v << std::endl;

#endif
