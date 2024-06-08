pub use am4::aircraft::{db::Aircrafts, Aircraft};
use am4::airport::db::AirportSearchError;
pub use am4::airport::{db::Airports, Airport};
use std::cell::RefCell;
use wasm_bindgen::prelude::*;
use web_sys::js_sys::Uint8Array;
// use serde_wasm_bindgen;

#[wasm_bindgen]
pub fn init() {
    console_error_panic_hook::set_once();
}

thread_local! {
    static AIRCRAFTS: RefCell<Option<Aircrafts>> = RefCell::new(None);
    static AIRPORTS: RefCell<Option<Airports>> = RefCell::new(None);
}

#[wasm_bindgen]
pub fn populate_aircrafts(arr: Uint8Array) {
    let aircrafts = Aircrafts::from_bytes(&(arr.to_vec())).unwrap();
    AIRCRAFTS.with(|a| *a.borrow_mut() = Some(aircrafts));
}

#[wasm_bindgen]
pub fn populate_airports(arr: Uint8Array) {
    let airports = Airports::from_bytes(&(arr.to_vec())).unwrap();
    AIRPORTS.with(|a| *a.borrow_mut() = Some(airports));
}

// js doesn't really allow returning a borrowed ref, so we have to clone
#[wasm_bindgen]
pub fn search_airport(s: &str) -> Result<Airport, AirportSearchError> {
    AIRPORTS.with(|a| {
        let airports = a.borrow();
        let airports = airports.as_ref().expect("airports not populated");
        airports.search(s).map(|a| a.clone())
    })
}
