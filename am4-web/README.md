# Get started

1. Install Rust with [`rustup`](https://rustup.rs/).
2. Install [wasm-pack](https://rustwasm.github.io/wasm-pack/installer/). This will glue JS with wasm.
3. Build the `am4-wasm` library, which will output to `./pkg`
```sh
wasm-pack build
```
4. Run the dev server
```sh
pnpm run dev
```

## Resources
https://github.com/shadanan/vite-rust-wasm
https://github.com/Menci/vite-plugin-wasm
