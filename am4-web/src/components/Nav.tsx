import './Nav.scss';
import { get_version } from '../../pkg/am4_wasm';

const Nav = () => {
    return <header role="banner">
        <div id="global-nav">
            <a href="https://cathaypacific8747.github.io/am4/" target="_blank">
                <img src="/assets/img/logo-64.webp" alt="logo" height="32" width="32" />
            </a>
            <div>
                <span id="name">AM4Help</span>
                <span id="version">" v" {get_version()}</span>
            </div>
            {/* <div id="db-progress">{prog_str}</div> */}
        </div>
        <div id="local-bar">
            <nav>
                <ul>
                    <li>
                        <b>
                            <a href="/">Home</a>
                        </b>
                    </li>
                    <li>
                        <a href="https://cathaypacific8747.github.io/am4/formulae/">
                            Formulae
                        </a>
                    </li>
                    {/* <li
                        id="clear-cache"
                        on:click=move |ev| {
                        clear_db.dispatch(ev);
                            }
                        >
                    "Clear Cache"
                    </li> */}
                </ul>
            </nav>
        </div>
    </header >;
}

export default Nav;