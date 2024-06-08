import { openDB, IDBPDatabase } from 'idb';
import { get_ac_filename, get_ap_filename, /*get_dem0_filename, get_dem1_filename, get_dist_filename*/ } from '../pkg/am4_wasm';
import { populate_aircrafts, populate_airports, search_airport } from '../pkg/am4_wasm';

class Idb {
    private database: IDBPDatabase;

    constructor(db: IDBPDatabase) {
        this.database = db;
    }

    // connect to the database and ensure that `am4help/data` object store exists
    static async connect(): Promise<Idb> {
        const db = await openDB('am4help', 1, {
            upgrade(db) {
                if (!db.objectStoreNames.contains('data')) {
                    db.createObjectStore('data');
                }
            },
        });
        return new Idb(db);
    }

    private async getBlob(k: string): Promise<Blob> {
        return this.database.transaction('data').objectStore('data').get(k);
    }

    private async writeBlob(k: string, v: Blob) {
        const tx = this.database.transaction('data', 'readwrite');
        await tx.objectStore('data').put(v, k);
    }

    async clear() {
        const tx = this.database.transaction('data', 'readwrite');
        await tx.objectStore('data').clear();
    }

    // Load a binary file from the IndexedDb. If the blob is not found*, 
    // fetch it from the server and cache it in the IndexedDb.
    // not found: `Response`* -> `Blob`* -> IndexedDb -> `Blob` -> `ArrayBuffer` -> `Vec<u8>`
    // set_progress: (msg: LoadDbProgress) => void
    public async getBytes(k: string, fallbackUrl: string): Promise<Uint8Array> {
        console.debug(`idb(read): ${k}`);
        const b = await this.getBlob(k);
        if (b) {
            return new Uint8Array(await b.arrayBuffer());
        } else {
            console.debug(`idb: empty, fetch: ${k}`);
            const response = await fetch(fallbackUrl);
            if (!response.ok) throw new Error(`failed to fetch: ${k}`);
            const blob = await response.blob();
            console.debug(`idb(write): ${k}`);
            await this.writeBlob(k, blob);
            return new Uint8Array(await blob.arrayBuffer());
        }
    }

    // /// Load the flat distances from the indexeddb. If the blob is not found*,
    // /// generate it from the slice of airports and cache it in the indexeddb.
    // /// not found: `&[Airport]`* -> `Distances`* (return this) -> `Blob`* -> IndexedDb
    // /// found: IndexedDb -> `Blob` -> `ArrayBuffer` -> `Distances`
    // async fn get_distances(&self, aps: &[Airport], set_progress: &dyn Fn(LoadDbProgress)) -> Result<Distances, GenericError> {
    //     let k = DIST_FILENAME;
    //     set_progress(LoadDbProgress::IDBRead(k.to_string()));
    //     match self.get(k).await? {
    //         Some(jsb) => {
    //             set_progress(LoadDbProgress::Parsing(k.to_string()));
    //             let ab = JsFuture::from(jsb.dyn_into::<Blob>()?.array_buffer()).await?;
    //             let bytes = Uint8Array::new(&ab).to_vec();
    //             Ok(Distances::from_bytes(&bytes).unwrap())
    //         },
    //         None => {
    //             set_progress(LoadDbProgress::Parsing(k.to_string()));
    //             let distances = Distances::from_airports(aps);
    //             let b = distances.to_bytes().unwrap();

    //             // https://github.com/rustwasm/wasm-bindgen/issues/1693
    //             // effectively, this is `new Blob([new Uint8Array(b)], {type: 'application/octet-stream'})`
    //             let ja = Array::new();
    //             ja.push(&Uint8Array::from(b.as_slice()).buffer());
    //             let mut opts = BlobPropertyBag::new();
    //             opts.type_("application/octet-stream");
    //             let blob = Blob::new_with_u8_array_sequence_and_options(&ja, &opts)?;
    //             let _ = self.write(k, &blob).await;
    //             Ok(distances)
    //         }
    //     }
    // }
}

export const getCoreData = async () => {
    const idb = await Idb.connect();

    const aps = await idb.getBytes(get_ap_filename(), `assets/data/${get_ap_filename()}`);
    console.log("refcell(ap): populate");
    populate_airports(aps);

    const acs = await idb.getBytes(get_ac_filename(), `assets/data/${get_ac_filename()}`);
    console.log("refcell(ac): populate");
    populate_aircrafts(acs);

    let res = search_airport("HKG");
    console.log(res.toJSON());

    // set_progress(LoadDbProgress::Parsing("distances".to_string()));
    // let distances = self.get_distances(airports.data(), set_progress).await ?;
    // log!("distances: {}", distances.data().len());

    // const dem0 = await idb.getBlob(`data/${get_dem0_filename()}`);
    // const dem1 = await idb.getBlob(`data/${get_dem1_filename()}`);
}