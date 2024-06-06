use am4::aircraft::db::Aircrafts;
use am4::airport::db::Airports;
use am4::route::db::Routes;
use once_cell::sync::Lazy;
use std::fs::File;
use std::io::Read;

pub fn get_bytes(path: &str) -> Result<Vec<u8>, std::io::Error> {
    let mut file = File::open(path)?;
    let mut buffer = Vec::<u8>::new();
    file.read_to_end(&mut buffer)?;
    Ok(buffer)
}

#[allow(dead_code)]
pub static AIRCRAFTS: Lazy<Aircrafts> =
    Lazy::new(|| Aircrafts::from_bytes(&get_bytes("./data/aircrafts.bin").unwrap()).unwrap());

#[allow(dead_code)]
pub static AIRPORTS: Lazy<Airports> =
    Lazy::new(|| Airports::from_bytes(&get_bytes("./data/airports.bin").unwrap()).unwrap());

#[allow(dead_code)]
pub static ROUTES: Lazy<Routes> =
    Lazy::new(|| Routes::from_bytes(&get_bytes("./data/routes.bin").unwrap()).unwrap());