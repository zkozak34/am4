pub mod db;

use rkyv::{Archive as Ra, Deserialize as Rd, Serialize as Rs};
use serde::{Deserialize, Serialize};
use std::str::FromStr;
use thiserror::Error;

#[cfg(feature = "wasm")]
use wasm_bindgen::prelude::*;

#[derive(Debug, Clone, Deserialize, Serialize, PartialEq, Ra, Rd, Rs)]
#[archive(check_bytes)]
#[cfg_attr(feature = "wasm", wasm_bindgen(getter_with_clone, inspectable))]
pub struct Airport {
    pub id: ApId,
    pub name: ApName,
    pub fullname: String,
    pub country: String,
    pub continent: String,
    pub iata: Iata,
    pub icao: Icao,
    pub location: Point,
    pub rwy: u16,
    pub market: u8,
    pub hub_cost: u32,
    pub rwy_codes: Vec<String>,
}

#[derive(Debug, Clone, Deserialize, Serialize, PartialEq, Eq, Hash, Ra, Rd, Rs)]
#[archive(check_bytes)]
#[cfg_attr(feature = "wasm", wasm_bindgen)]
pub struct ApId(pub u16);

impl FromStr for ApId {
    type Err = AirportError;

    fn from_str(id: &str) -> Result<Self, Self::Err> {
        id.parse::<u16>().map(Self).map_err(AirportError::InvalidID)
    }
}

#[derive(Debug, Clone, Deserialize, Serialize, PartialEq, Eq, Hash, Ra, Rd, Rs)]
#[archive(check_bytes)]
#[cfg_attr(feature = "wasm", wasm_bindgen(getter_with_clone))]
pub struct ApName(pub String);

impl FromStr for ApName {
    type Err = AirportError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.len() {
            1..=40 => Ok(Self(s.to_string())), // actual 36
            _ => Err(AirportError::InvalidName),
        }
    }
}

#[derive(Debug, Clone, Deserialize, Serialize, PartialEq, Eq, Hash, Ra, Rd, Rs)]
#[archive(check_bytes)]
#[cfg_attr(feature = "wasm", wasm_bindgen(getter_with_clone))]
pub struct Iata(pub String);

impl FromStr for Iata {
    type Err = AirportError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.len() {
            3 => Ok(Self(s.to_string())),
            _ => Err(AirportError::InvalidIata),
        }
    }
}

#[derive(Debug, Clone, Deserialize, Serialize, PartialEq, Eq, Hash, Ra, Rd, Rs)]
#[archive(check_bytes)]
#[cfg_attr(feature = "wasm", wasm_bindgen(getter_with_clone))]
pub struct Icao(pub String);

impl FromStr for Icao {
    type Err = AirportError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.len() {
            4 => Ok(Self(s.to_string())),
            _ => Err(AirportError::InvalidIcao),
        }
    }
}

#[derive(Debug, Clone, Deserialize, Serialize, PartialEq, Ra, Rd, Rs)]
#[archive(check_bytes)]
#[cfg_attr(feature = "wasm", wasm_bindgen)]
pub struct Point {
    pub lng: f32,
    pub lat: f32,
}

#[derive(Debug, Error)]
pub enum AirportError {
    #[error("Invalid airport ID: {0}")]
    InvalidID(#[source] std::num::ParseIntError),
    #[error("Invalid name: must be between 1 and 50 characters")]
    InvalidName,
    #[error("Invalid IATA code: must be 3 characters")]
    InvalidIata,
    #[error("Invalid ICAO code: must be 4 characters")]
    InvalidIcao,
}

#[cfg(feature = "wasm")]
impl From<AirportError> for JsValue {
    fn from(err: AirportError) -> JsValue {
        JsValue::from_str(&format!("{}", err))
    }
}
