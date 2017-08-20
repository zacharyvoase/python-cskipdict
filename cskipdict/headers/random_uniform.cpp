#include <cstdint>
#include <random>
#include "random_uniform.h"

extern "C" uint32_t random_uniform(uint32_t max_plus_one) {
	std::random_device rd;  //Will be used to obtain a seed for the random number engine
	std::mt19937 gen(rd()); //Standard mersenne_twister_engine seeded with rd()
	std::uniform_int_distribution<uint32_t> dis(0, max_plus_one - 1);
	return dis(gen);
}
