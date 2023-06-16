#pragma once
#include <duckdb.hpp>

struct PaxDemand {
    uint16_t y;
    uint16_t j;
    uint16_t f;

    PaxDemand();
    PaxDemand(uint16_t y, uint16_t j, uint16_t f);
    PaxDemand(const duckdb::DataChunk& chunk, idx_t row);
};

struct CargoDemand {
    uint32_t l;
    uint32_t h;

    CargoDemand();
    CargoDemand(uint32_t l, uint32_t h);
    CargoDemand(uint16_t y, uint16_t j);
    CargoDemand(const duckdb::DataChunk& chunk, idx_t row);
    CargoDemand(const PaxDemand& pax_demand);
};