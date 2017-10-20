#include <cmath>
#include <iostream>

#define CATCH_CONFIG_MAIN  // This tells Catch to provide a main() - only do this in one cpp file
#include "catch.hpp"

#include "../src/main.hpp"

TEST_CASE( "test the calculate_sirup_level function", "[main]" ) {
    float level = calculate_sirup_level(1, 10);
    std::cout<<level<<'\n';
    
    REQUIRE(81 == calculate_sirup_level(1, 10));
    REQUIRE(76 == calculate_sirup_level(1, 5));
    REQUIRE(69 == calculate_sirup_level(1, 3 ));
    REQUIRE(85 == calculate_sirup_level(1, 20));
    REQUIRE(65 == calculate_sirup_level(4, 9));
}

