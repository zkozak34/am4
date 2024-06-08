import { createEffect, createRenderEffect, createSignal } from 'solid-js';
import './App.scss';

import { init } from "../pkg/am4_wasm";
import Nav from './components/Nav';

import { getCoreData } from './db';

enum LoadDbProgress {
  IDBConnect,
  IDBRead,
  IDBWrite,
  Fetching,
  Parsing,
  Loaded,
  Err,
}

const App = () => {
  let [progress, setProgress] = createSignal<LoadDbProgress>(LoadDbProgress.IDBConnect);

  createRenderEffect(() => { init() }) // init wasm before any rendering

  createEffect(async () => {

    setProgress(LoadDbProgress.IDBRead);
    await getCoreData();

    //         match Idb::connect().await.unwrap().init_db(&|msg| set_progress.set(msg)).await {
    //             Ok(db) => {
    //                 database.set_value(Some(db));
    //                 set_progress.set(LoadDbProgress::Loaded);
    //             }
    //             Err(e) => set_progress.set(LoadDbProgress::Err(e)),
    //         }

    setProgress(LoadDbProgress.Loaded);

    init();
  })

  // let database = store_value::<Option<Database>>(None);

  // provide_context(database);

  // view! {
  //     <div id="app">
  //         <Header progress/>
  //         <main>
  //             <Show when=move || progress.get() == LoadDbProgress::Loaded>
  //                 <ACSearch/>
  //                 <APSearch/>
  //             </Show>
  //         </main>
  //     </div>
  // }

  return (
    <>
      <Nav />
      <main>
        {progress()}
      </main>
    </>
  )
}

export default App;