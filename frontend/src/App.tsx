import React from 'react';
import logo from './images/cb_logo.jpg';
import './App.css';

function App() {
    return (
        <section className="section is-medium">
            <div className="columns is-centered">
                <div className="column is-two-thirds">

                    <div className='section is-small columns is-centered image'>
                        <figure className="image">
                            <img src={logo} className="" alt="logo" />
                        </figure>
                    </div>

                    <div className="columns is-centered">
                        <div className="field has-addons">
                            <div className="control">
                                <input className="input" type="text" placeholder="" />
                            </div>
                            <div className="control">
                                <a className="button is-info">
                                    Cerca
                                </a>
                            </div>
                        </div>
                    </div>

                </div>
            </div>
        </section>
    );
}

export default App;
