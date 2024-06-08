pub mod airport;
pub mod utils;

pub mod campaign;
pub mod ticket;
pub mod user;

pub mod aircraft;

pub mod route; // under development

// to keep track of changes for data files in `../data`
#[macro_export]
macro_rules! ac_version {
    () => {
        "0"
    };
}
pub const AC_FILENAME: &str = concat!("aircrafts-v", ac_version!(), ".bin");

#[macro_export]
macro_rules! ap_version {
    () => {
        "0"
    };
}
pub const AP_FILENAME: &str = concat!("airports-v", ap_version!(), ".bin");
// distances are generated from the airports
pub const DIST_FILENAME: &str = concat!("distances-v", ap_version!(), ".bin");

#[macro_export]
macro_rules! demand_version {
    () => {
        "0"
    };
}
pub const DEM0_FILENAME: &str = concat!("demands0-v", demand_version!(), ".bin");
pub const DEM1_FILENAME: &str = concat!("demands1-v", demand_version!(), ".bin");

#[cfg(feature = "wasm")]
use wasm_bindgen::prelude::*;

#[cfg_attr(feature = "wasm", wasm_bindgen)]
pub fn get_ac_filename() -> String {
    AC_FILENAME.to_string()
}

#[cfg_attr(feature = "wasm", wasm_bindgen)]
pub fn get_ap_filename() -> String {
    AP_FILENAME.to_string()
}

#[cfg_attr(feature = "wasm", wasm_bindgen)]
pub fn get_dem0_filename() -> String {
    DEM0_FILENAME.to_string()
}

#[cfg_attr(feature = "wasm", wasm_bindgen)]
pub fn get_dem1_filename() -> String {
    DEM1_FILENAME.to_string()
}

#[cfg_attr(feature = "wasm", wasm_bindgen)]
pub fn get_dist_filename() -> String {
    DIST_FILENAME.to_string()
}

#[cfg_attr(feature = "wasm", wasm_bindgen)]
pub fn get_version() -> String {
    env!("CARGO_PKG_VERSION").to_string()
}
